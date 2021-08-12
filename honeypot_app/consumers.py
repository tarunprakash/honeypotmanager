"""
Websocket consumer for live log viewer
"""

import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import StopConsumer


class LogConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('logGroup', self.channel_name)
        await self.accept()

    async def disconnect(self, event):
        await self.channel_layer.group_discard('logGroup', self.channel_name)
        raise StopConsumer()

    async def send_message(self, res):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))