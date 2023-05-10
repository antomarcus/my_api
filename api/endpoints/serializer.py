from rest_framework import serializers
from endpoints.models import Endpoint
from endpoints.models import DLAlgorithm
from endpoints.models import DLAlgorithmStatus
from endpoints.models import DLRequest

class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ("id", "name", "owner", "created_at")
        fields = read_only_fields

class DLAlgorithmSerializer(serializers.ModelSerializer):

    current_status = serializers.SerializerMethodField(read_only=True)

    def get_current_status(self, dlalgorithm):
        return DLAlgorithmStatus.objects.filter(parent_dlalgorithm=dlalgorithm).latest('created_at').status

    class Meta:
        model = DLAlgorithm
        read_only_fields = ("id", "name", "description", "code","version", "owner", "created_at",
                            "parent_endpoint", "current_status")
        fields = read_only_fields

class DLAlgorithmStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DLAlgorithmStatus
        read_only_fields = ("id", "active")
        fields = ("id", "active", "status", "created_by", "created_at","parent_dlalgorithm")

class DLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DLRequest
        read_only_fields = ("id","input_data",
            "full_response","response","created_at",
            "parent_dlalgorithm",
        )
        fields =  ("id","input_data","full_response","response","feedback","created_at","parent_dlalgorithm",)