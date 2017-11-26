import sys, os, django
sys.path.append("./") #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebPyRobot.development")
django.setup()

from backend.models import BattleHistory


def finish_battles():
    print (BattleHistory.objects.update(is_finished=True))


if __name__ == "__main__":
    finish_battles()
