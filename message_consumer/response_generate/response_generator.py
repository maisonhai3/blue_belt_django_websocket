from asyncio import sleep
from random import random

from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def generate_text_response(message: str) -> str:
    sleep(random())
    return message


@app.task
def generate_media_response(message: str) -> str:
    sleep(random())
    return message


@app.task
def generate_video_response(message: str) -> str:
    sleep(random())
    return message


class ResponseGenerator:
    def __init__(self):
        self.default_text_message = "This is a default text message"
        self.default_media_message = "This is a default media message"
        self.default_video_message = "This is a default video message"

    def generate_response(self, message_type) -> str:
        if message_type == "text":
            return generate_text_response.delay(self.default_text_message)
        if message_type == "media":
            return generate_media_response.delay(self.default_media_message)
        if message_type == "video":
            return generate_video_response.delay(self.default_video_message)
        return "Invalid message type"
