from django.contrib import admin
from endpoints.models import Endpoint, DLAlgorithm, DLAlgorithmStatus, DLRequest

# Register your models here.

admin.site.register(Endpoint)
admin.site.register(DLAlgorithm)
admin.site.register(DLAlgorithmStatus)
admin.site.register(DLRequest)