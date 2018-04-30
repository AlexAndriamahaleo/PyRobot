import django
import os
import sys
from ..backend.models import BattleHistory, UserProfile


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebPyRobot.development")
django.setup()


def finish_battles():
    print(BattleHistory.objects.update(is_finished=True))


def update_level():
    print(UserProfile.objects.update(level=0))


if __name__ == "__main__":
    # finish_battles()
    update_level()
