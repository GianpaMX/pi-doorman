import logging
import time

from firebase_admin import messaging

log = logging.getLogger(__name__)


class NotificationGateway:
    def __init__(self, firebase_app):
        self.firebase_app = firebase_app

    def send(self, token):
        message = messaging.Message(
            data={
                'time': str(int(time.time() * 1000)),
            },
            token=token,
        )

        log.info('send:%s', token)
        response = messaging.send(message)
        log.info('response:%s', response)
