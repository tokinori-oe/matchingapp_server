from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from SearchForLover.consumers import RequestConsumer

websocket_urlpatterns = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("request_path/39/", RequestConsumer.as_asgi()), #ここの数字を一般化する
    ]),
})