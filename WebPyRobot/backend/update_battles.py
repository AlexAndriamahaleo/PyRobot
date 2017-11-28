import sys, os, django
sys.path.append("./") #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebPyRobot.development")
django.setup()

from backend.models import BattleHistory, UserProfile


def finish_battles():
    print (BattleHistory.objects.update(is_finished=True))


def update_level():
    print (UserProfile.objects.update(level=0))

if __name__ == "__main__":
    # finish_battles()
    update_level()