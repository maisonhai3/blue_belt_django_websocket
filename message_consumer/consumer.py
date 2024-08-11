import json
from datetime import datetime

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from message_consumer.client_manament.client_manager import ClientManager
from message_consumer.response_generate.response_generator import ResponseGenerator


class MessageConsumer(AsyncWebsocketConsumer):
    client_manager = None
    response_generator = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_manager = ClientManager(self)
        self.response_generator = ResponseGenerator()

    async def connect(self):
        if not self.client_manager.is_allowed_to_connect():
            await self.close()
            return

        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'Hello World!'
        }))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message_type = text_data_json["type"]
        if message_type not in ["text", "media", "video"]:
            return await self.send(text_data=json.dumps({"message": "Invalid message type"}))

        text = text_data_json["text"]
        media = text_data_json["media"]
        timezone = text_data_json["timezone"]  # Example: "UTC+7"

        if not await self._is_in_reply_time(message_type, timezone):
            return await self.send(text_data=json.dumps({"message": "Not in reply time"}))

        response = self.response_generator.generate_response(message_type)
        await self.send(text_data=json.dumps({"message": response}))

    @staticmethod
    async def _is_in_reply_time(message_type, timezone):
        now = datetime.now(timezone)
        mid_night = 24

        if message_type == "text" and 5 <= now.hour <= mid_night:
            return True
        if message_type == "media" and 8 <= now.hour <= mid_night:
            return True
        if message_type == "video" and 20 <= now.hour <= mid_night:
            return True

        return False
