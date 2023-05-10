from django.urls import path, include
from rest_framework.routers import DefaultRouter

from endpoints.views import EndpointViewSet
from endpoints.views import DLAlgorithmViewSet
from endpoints.views import DLAlgorithmStatusViewSet
from endpoints.views import DLRequestViewSet
from endpoints.views import PredictView

router = DefaultRouter(trailing_slash=False)
router.register(r"endpoints", EndpointViewSet, basename="endpoints")
router.register(r"dlalgorithms", DLAlgorithmViewSet, basename="dlalgorithms")
router.register(r"dlalgorithmstatuses", DLAlgorithmStatusViewSet, basename="dlalgorithmstatuses")
router.register(r"dlrequests", DLRequestViewSet, basename="dlrequests")


from endpoints import views
urlpatterns = [
    path(r"", include(router.urls)),
    path('<str:endpoint_name>/predict', PredictView.as_view(), name="predict"),
]