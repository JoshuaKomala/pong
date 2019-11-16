from collections import deque
from typing import Iterable

from data_structures.circle import Circle
from models.player import Player

BYE = Player(name="BYE")


def round_robin(n):
    """
    https://en.wikipedia.org/wiki/Round-robin_tournament

    Generator for a round-robin schedule for n players.
    If n is odd, a dummy player will be introduced as player (n+1).
    Each iteration will yield a list of tuple matchups (p1, p2).
    """
    if n < 2:
        print("No round robin exists for schedule with less than two players")
        return

    # normalize to even amount of players
    n = n if n % 2 == 0 else n + 1

    # construct rotatable circle with everyone but first player
    circle = Circle(range(2, n+1))

    for _ in range(n-1):
        round = []

        # fix the first player in the circle
        circle.insert_head(1)

        for i in range(n//2):
            p1, p2 = circle[i], circle[n-1-i]  # play the person "opposite" of you in the circle
            matchup = min(p1, p2), max(p1, p2)
            round.append(matchup)

        yield round

        # rotate everyone else but the first player
        circle.remove_head()
        circle.rotate()


def construct_matchups(round, players):
    """
    Given the current round of seed matchups, construct a list of player matchups.

    @round (List[tuple]): tuples of two numbers. Lower number means higher seeded (higher ranked)
    @players (List[Player])
    """
    seeded_players = sorted(players, key=lambda p: -p.rating)  # sort players highest to lowest
    matchups = []
    for (p1, p2) in round:
        if 0 <= p1 - 1 < len(seeded_players):
            player1 = seeded_players[p1-1]
            p1_seed = p1
        else:
            player1 = BYE
            p1_seed = '-'
        if 0 <= p2 - 1 < len(seeded_players):
            player2 = seeded_players[p2-1]
            p2_seed = p2
        else:
            player2 = BYE
            p2_seed = '-'
        matchups.append(((player1, p1_seed), (player2, p2_seed)))
    return matchups
