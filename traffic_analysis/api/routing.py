from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/api/traffic', consumers.NetworkTrafficHandlerTaksConsumer.as_asgi()),
]