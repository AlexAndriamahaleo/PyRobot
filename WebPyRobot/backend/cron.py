import datetime
from .models import Championship

def OneMinuteJob():
    now = datetime.datetime.now()
    print(str(now), " - OneMinuteJob -> Test CronJob for DB")
    pass


def TenMinuteJob():
    now = datetime.datetime.now()
    print(str(now), " - TenMinuteJob -> Test CronJob for DB")
    pass


def displayDataChampionship():
    now = datetime.datetime.now()
    print(str(now), " - Display Championship Objects")
    # championships = Championship.objects.all()
    championships = Championship.objects.exclude(pk=Championship.objects.get(pk=1).pk).exclude(pk=Championship.objects.get(pk=2).pk)
    for championship in championships:
        if championship.get_players().count() == 0:
            old_championship = championship.name
            try:
                championship.delete()
                print(">>> No players in %s [DELETED]" % old_championship)
            except:
                print("ERROR ON DELETE - %s" % old_championship)
        else:
            print("> Players in %s : %s" % (championship.name, championship.get_players().count()))
