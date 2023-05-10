from rest_framework import viewsets
from rest_framework import mixins

from endpoints.models import Endpoint
from endpoints.serializer import EndpointSerializer

from endpoints.models import DLAlgorithm
from endpoints.serializer import DLAlgorithmSerializer

from endpoints.models import DLAlgorithmStatus
from endpoints.serializer import DLAlgorithmStatusSerializer

from endpoints.models import DLRequest
from endpoints.serializer import DLRequestSerializer

from django.db import transaction
from rest_framework.exceptions import APIException

import json
from numpy.random import rand
from rest_framework import views, status
from rest_framework.response import Response
from endpoints.model.registry import DLRegistry
from api.wsgi import registry



class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):
        algorithm_status = self.request.query_params.get("status","production")
        algorithm_version = self.request.query_params.get("version")

        algs = DLAlgorithm.objects.filter(parent_endpoint__name = endpoint_name,
                                            status__status = algorithm_status, status__active=True)
        
        if algorithm_version is not None:
            algs = algs.filter(version= algorithm_version)


        if len(algs) == 0:
            return Response({"status": "Error", "message": "DL algorithm is not available"},
                status=status.HTTP_400_BAD_REQUEST,)
        
        if len(algs) != 1 and algorithm_status != "testing":
            return Response(
                {"status": "Error", "message": "DL algorithm selection is ambiguous. Please specify algorithm version."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        alg_index = 0
        if algorithm_status == "testing":
            alg_index = 0 if rand() < 0.5 else 1

        algorithm_object = registry.endpoints[algs[alg_index].id]
        prediction = algorithm_object.model_prediction(request.data)

        label = prediction["label"] if "label" in prediction else "error"
        dl_request = DLRequest(
            input_data = json.dumps(request.data),
            full_response = prediction,
            response = label,
            feedback = "",
            parent_dlalgorithm = algs[alg_index],
        )

        dl_request.save()
        prediction["request_id"] = dl_request.id

        return Response(prediction)

class EndpointViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()


class DLAlgorithmViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = DLAlgorithmSerializer
    queryset = DLAlgorithm.objects.all()


def deactivate_other_statuses(instance):
    old_statuses = DLAlgorithmStatus.objects.filter(parent_dlalgorithm = instance.parent_dlalgorithm,
                                                        created_at__lt=instance.created_at,
                                                        active=True)
    for i in range(len(old_statuses)):
        old_statuses[i].active = False
    DLAlgorithmStatus.objects.bulk_update(old_statuses, ["active"])

class DLAlgorithmStatusViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.CreateModelMixin
):
    serializer_class = DLAlgorithmStatusSerializer
    queryset = DLAlgorithmStatus.objects.all()
    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                # set active=False for other statuses
                deactivate_other_statuses(instance)

        except Exception as e:
            raise APIException(str(e))

class DLRequestViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.UpdateModelMixin
):
    serializer_class = DLRequestSerializer
    queryset = DLRequest.objects.all()
