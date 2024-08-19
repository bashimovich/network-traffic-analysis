from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
channel_layer = get_channel_layer()

@shared_task
def network_traffic_handler_task():
    async_to_sync(channel_layer.group_send)('traffic_hander_group', {'type':'network_traffic_handler', "task": True})
