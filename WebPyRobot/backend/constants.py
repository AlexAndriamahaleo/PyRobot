import json


class NotificationMessage(object):

    def __init__(self, msg_type='notification', msg_class='success', msg_content='', **kwargs):
        self.msg_type = msg_type
        self.msg_class = msg_class
        self.msg_content = msg_content
        self.data = kwargs

    def as_dict(self):
        result = {
            'msg_type': self.msg_type,
            'msg_class': self.msg_class,
            'msg_content': self.msg_content
        }
        for k, v in self.data.items():
            result[k] = v
        return result

    def dumps(self):
        return json.dumps(self.as_dict())


DEBUG = 10
INFO = 20
SUCCESS = 25
WARNING = 30
ERROR = 40

MESSAGE_LEVEL_CLASSES = {

}