import json
import logging
import traceback

from django.contrib.auth.models import User

from channels import Group
from channels.sessions import channel_session

from .utils import award_battle_elo


def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    message.reply_channel.send({
        "text": message.content['text'],
    })


log = logging.getLogger(__name__)


@channel_session
def ws_connect(message):
    """
    Starting websocket connection
    """
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
    """
    Handle data received from clients
    """
    try:
        try:
            data = json.loads(message['text'])
        except ValueError:
            log.debug("ws message isn't json")
            return

        mode = data.get('is_versus')

        # Battle data from the frontend side
        if data.get('msg_type') == "battle_step":
            username = data.get("username")
            try:
                user = User.objects.get(username=username)
            except:
                log.error(traceback.format_exc())
                log.error("User not found %s" % username)
                return
            battle = user.userprofile.get_running_battle()

            # Battle finished
            if data.get("finished") == "yes":
                battle.is_finished = True
                battle.save()
                if battle.is_victorious:
                    award_battle_elo(battle.user.userprofile, battle.opponent.userprofile, mode)
                else:
                    award_battle_elo(battle.opponent.userprofile, battle.user.userprofile, mode)
                return

            if battle != None:
                step = int(data.get("step", 0))
                battle.step = step
                battle.player_x = data.get('player_x', 0)
                battle.player_y = data.get('player_y', 0)
                battle.opponent_y = data.get('opponent_y', 0)
                battle.opponent_x = data.get('opponent_x', 0)
                battle.save()
        else:
            label = message.channel_session['label']
            Group(label, channel_layer=message.channel_layer).send({'text': message['text']})
    except:
        log.error(traceback.format_exc())
        log.error(message['text'])


@channel_session
def ws_disconnect(message):
    """
    Ends websocket connection
    """
    try:
        label = message.channel_session['label']
        Group(label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except:
        traceback.print_exc()
