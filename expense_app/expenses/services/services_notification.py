from pyfcm import FCMNotification

class NotificationService:
    def __init__(self, api_key):
        self.client = FCMNotification(api_key=api_key)

    def send(self, token, title, message):
        self.client.notify_single_device(
            registration_id=token,
            message_title=title,
            message_body=message
        )
