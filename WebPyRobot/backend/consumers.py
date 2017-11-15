import re
import json
import logging
import traceback

from channels import Group
from channels.sessions import channel_session


def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    message.reply_channel.send({
        "text": message.content['text'],
    })


log = logging.getLogger(__name__)


@channel_session
def ws_connect(message):
    try:
        prefix = message['path'].strip('/').strip()
        if prefix == '':
            log.debug('invalid ws path=%s', message['path'])
            return
        message.channel_session['label'] = prefix
        Group(prefix, channel_layer=message.channel_layer).add(message.reply_channel)
        message.reply_channel.send({"accept": True})
    except:
        log.debug('invalid ws path=%s', message['path'])
        return



@channel_session
def ws_receive(message):
    label = message.channel_session['label']
    Group(label, channel_layer=message.channel_layer).send({'text': message['text']})
    # # Look up the room from the channel session, bailing if it doesn't exist
    # try:
    #     label = message.channel_session['room']
    #     room = Room.objects.get(label=label)
    # except KeyError:
    #     log.debug('no room in channel_session')
    #     return
    # except Room.DoesNotExist:
    #     log.debug('recieved message, buy room does not exist label=%s', label)
    #     return
    #
    # # Parse out a chat message from the content text, bailing if it doesn't
    # # conform to the expected message format.
    # try:
    #     data = json.loads(message['text'])
    # except ValueError:
    #     log.debug("ws message isn't json text=%s", text)
    #     return
    #
    # if set(data.keys()) != set(('handle', 'message')):
    #     log.debug("ws message unexpected format data=%s", data)
    #     return
    #
    # if data:
    #     log.debug('chat message room=%s handle=%s message=%s',
    #               room.label, data['handle'], data['message'])
    #     m = room.messages.create(**data)
    #
    #     # See above for the note about Group
    #     Group('chat-' + label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})


@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['label']
        Group(label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except:
        traceback.print_exc()