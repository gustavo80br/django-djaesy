from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import alerts
import sandbox

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            sandbox.routing.websocket_urlpatterns +
            alerts.routing.websocket_urlpatterns
        ),
    ),
})
