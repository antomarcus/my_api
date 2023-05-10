from endpoints.models import Endpoint
from endpoints.models import DLAlgorithm
from endpoints.models import DLAlgorithmStatus


class DLRegistry:
    def __init__(self):
        self.endpoints = {}

    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name,
                    algorithm_status, algorithm_version, owner,
                    algorithm_description, algorithm_code):
        # get endpoint
        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name, owner=owner)

        # get algorithm
        database_object, algorithm_created = DLAlgorithm.objects.get_or_create(
                name=algorithm_name,
                description=algorithm_description,
                version=algorithm_version,
                code=algorithm_code,
                owner=owner,
                parent_endpoint=endpoint)
        if algorithm_created:
            status = DLAlgorithmStatus(status = algorithm_status,
                                        created_by = owner,
                                        parent_dlalgorithm = database_object,
                                        active = True)
            status.save()

        # add to registry
        self.endpoints[database_object.id] = algorithm_object