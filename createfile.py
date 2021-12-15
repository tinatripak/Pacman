import time
from player import Player
from copy import deepcopy
import sys
result = []
width = 20

start_matrix = list(map(lambda line: list(
        map(lambda x: int(x), line[:-1])), open("level.txt", "r")))
results = []
pacman = Player(
    1, 1, width, deepcopy(start_matrix), {
        "w": len(start_matrix[0]),
        "h": len(start_matrix),
        "№train": 1000
    })


def filewithresults(player):
    log_file = open('C:/Users/Кристина/Desktop/pacman/logs/' + str(player.general_record_time) + '-l-' + str(
        player.params['width']) + '-m-' + str(
        player.params['height']) + '-x-' + str(player.params['num_training']) + '.log', 'a')

    log_file.write("%4d: крок: %5d, час виконання: %4f, поінти: %12f, e: %10f," %
                   (player.numeps, player.local_cnt, time.time() - player.s, player.ep_rew, player.params['eps']))
    log_file.write(" Q: %10f, статус: %r \n" % (
        (max(player.Q_global, default=float('nan')), result[1])))

    sys.stdout.write("%4d: крок: %5d, час виконання: %4f, поінти: %12f, e: %10f," %
                     (player.numeps, player.local_cnt, time.time() - player.s, player.ep_rew, player.params['eps']))
    sys.stdout.write(" Q: %10f, статус: %r \n" % (
        (max(player.Q_global, default=float('nan')), result[1])))
