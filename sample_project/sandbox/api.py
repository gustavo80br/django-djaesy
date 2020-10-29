from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

channel_layer = get_channel_layer()


class UpdateTrackerStatus(APIView):

    def get(self, request):

        async_to_sync(channel_layer.group_send)(
            "chat_lobby",
            {
                'type': 'chat_message',
                'message': ''
            },
        )

        return Response(data='', status=status.HTTP_200_OK)
