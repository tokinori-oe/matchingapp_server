from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from SearchForLover.consumers import RequestConsumer

websocket_urlpatterns = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("request_path/(?P<receiver>\d+)/$", RequestConsumer.as_asgi()),
    ]),
})