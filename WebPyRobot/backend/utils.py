from django.conf import settings
from math import *


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
    Calculate gaining points and money of a user. If winner level is the same as loser, points = 5, money=300
    If winner level is higher than loser, points = 1 or 2, money = 150 or 200
    If winner level is lower than loser, points = 5 + (loser's level - winner's level)*5, money = 300 + 50*dif
    It means winner get bonus of 5 points for each lower level
    :param win: level of winner
    :param lose: level of loser
    :return: points, money
    """
    if win < lose:
        dif = lose - win
        return (10 + 7 * dif), (300 + 50 * dif)
    elif win == lose:
        return 10, 300
    else:
        dif = win - lose
        if dif < 3:
            return 4, 200
        return 2, 150


def calcul_difference_elo_pts(win_points, lose_points):
    diff = win_points - lose_points
    print("win pts %s - lose pts %s" % (win_points, lose_points))

    if abs(diff) > settings.ELO_PTS_MAX_DIFF and diff < 0:
        return -settings.ELO_PTS_MAX_DIFF
    elif abs(diff) > settings.ELO_PTS_MAX_DIFF and diff > 0:
        return settings.ELO_PTS_MAX_DIFF
    else:
        return diff


def probability_award(D):
    if D < 0:  # launcher WIN
        prob_win = 1 / (1 + pow(10, (-D / 400)))
        prob_lose = 1 / (1 + pow(10, (D / 400)))
        print("probability launcher win %s - %s" % (prob_win, prob_lose))
    else:  # launcher LOSE
        prob_win = 1 / (1 + pow(10, (D / 400)))
        prob_lose = 1 / (1 + pow(10, (-D / 400)))
        print("probability launcher lose %s - %s" % (prob_win, prob_lose))

    return prob_win, prob_lose


def calcul_coefficient_K(player):
    print("Début: ", player.points, player.coeff_K)

    if player.nb_games <= 30:
        player.nb_games += 1

    elif player.points < 2400:

        if player.coeff_K != 20:
            player.coeff_K = 20

        player.nb_games += 1

    else:

        if player.coeff_K != 10:
            player.coeff_K = 10

        player.nb_games += 1

    player.save()
    print("Fin: ", player.points, player.coeff_K)
    return player.coeff_K


def award_battle(winner, loser, mode):
    """
    Increase players points, money, level, tank hp if possible
    :param winner: UserProfile of winner
    :param loser: UserProfile of loser
    :param mode: yes [VERSUS] - no [CHAMPIONNAT]
    :return: void
    """
    w_points, w_money = calc_user_level(winner.level, loser.level)

    if mode == 'no':
        winner.points += w_points

    if winner.points >= winner.next_level_exp:
        winner.level += 1
        winner.calc_next_level_exp()
        tank = winner.get_tank()
        # tank.hp_value += 10
        tank.save()
    winner.money += w_money
    winner.save()

    if mode == 'no':
        loser.points += 2

    if loser.points >= loser.next_level_exp:
        loser.level += 1
        loser.calc_next_level_exp()
        tank = loser.get_tank()
        # tank.hp_value += 10
        tank.save()
    loser.money += 100
    loser.save()


def award_battle_elo(winner, loser, mode):
    """
    Increase players points (based on ELO)
    :param winner: UserProfile of winner
    :param loser: UserProfile of loser
    :param mode: yes [ENTRAINEMENT] - no [CHAMPIONNAT]
    :return: void
    """

    if mode == 'no':
        difference = calcul_difference_elo_pts(winner.points, loser.points)
        print("ELO points différence: %s" % difference)

        p_D_win, p_D_lose = probability_award(difference)
        print("Probability win %s - lose %s" % (p_D_win, p_D_lose))

        player_K_win = calcul_coefficient_K(winner)
        player_K_lose = calcul_coefficient_K(loser)
        print("Coefficient K win %s - lose %s" % (player_K_win, player_K_lose))

        new_pts_win = trunc(winner.points + player_K_win * (settings.ELO_PTS_AWARD_WIN - p_D_win))
        new_pts_lose = trunc(loser.points + player_K_lose * (settings.ELO_PTS_AWARD_LOSE - p_D_lose))

        if new_pts_lose < 0:
            # new_pts_lose = loser.points
            new_pts_lose = loser.points + 10*(player_K_win * (settings.ELO_PTS_AWARD_WIN - p_D_win))/100


        print("New points win %s (%s) - lose %s (%s)" % (new_pts_win, player_K_win * (settings.ELO_PTS_AWARD_WIN - p_D_win), new_pts_lose, player_K_lose * (settings.ELO_PTS_AWARD_LOSE - p_D_lose)))

        winner.points = new_pts_win
        loser.points = new_pts_lose

        winner.save()
        loser.save()
