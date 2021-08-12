from django.conf.urls import url
from honeypot_app.consumers import LogConsumer

websocket_urlpatterns = [
    url('log', LogConsumer.as_asgi()),
]