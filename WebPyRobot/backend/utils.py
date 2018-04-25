from django.conf import settings


def validate_ai_script(text):
    """
    Verify input AI script. False if the script contains not allowed keywords like "import", "exec"
    :param text: String
    :return: True/False
    """
    if text.strip() == "":
        return False
    for line in text.splitlines():
        if any(kw in line for kw in settings.NOT_ALLOWED_KW):
            return False
    return True


def calc_user_level(win, lose):
    """
    Calculate gaining exp and money of a user. If winner level is the same as loser, exp = 5, money=300
    If winner level is higher than loser, exp = 1 or 2, money = 150 or 200
    If winner level is lower than loser, exp = 5 + (loser's level - winner's level)*5, money = 300 + 50*dif
    It means winner get bonus of 5 exp for each lower level
    :param win: level of winner
    :param lose: level of loser
    :return: exp, money
    """
    if win < lose:
        dif = lose - win
        return (5 + 5*dif), (300 + 50*dif)
    elif win == lose:
        return 5, 300
    else:
        dif = win - lose
        if dif < 3:
            return 2, 200
        return 1, 150

def award_battle(winner, loser):
    """
    Increase players exp, money, level, tank hp if possible
    :param winner: UserProfile of winner
    :param loser: UserProfile of loser
    :return: void
    """
    w_exp, w_money = calc_user_level(winner.level, loser.level)
    winner.exp += w_exp
    if winner.exp >= winner.next_level_exp:
        winner.level += 1
        winner.calc_next_level_exp()
        tank = winner.get_tank()
        # tank.hp_value += 10
        tank.save()
    winner.money += w_money
    winner.save()

    loser.exp += 1
    if loser.exp >= loser.next_level_exp:
        loser.level += 1
        loser.calc_next_level_exp()
        tank = loser.get_tank()
        # tank.hp_value += 10
        tank.save()
    loser.money += 100
    loser.save()

