"""
WSGI config for api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

application = get_wsgi_application()

import inspect
from endpoints.model.registry import DLRegistry
from endpoints.model.model import model_Lead

try:
    registry = DLRegistry() # create DL registry
   
    Model = model_Lead()
    # add to DL registry
    registry.add_algorithm(endpoint_name="model_Lead",
                            algorithm_object=Model,
                            algorithm_name="model_Lead",
                            algorithm_status="production",
                            algorithm_version="0.0.1",
                            owner="antony",
                            algorithm_description="edxrf spectral data analysis",
                            algorithm_code=inspect.getsource(model_Lead))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))
