import itertools
import math
from random import choice
from typing import Generator, Callable, Optional

from action import Action, ACTIONS
import results


StrategyActions_T = Generator[Action, Action, None]
Strategy_T = Callable[[], StrategyActions_T]


# ------------------------------ ALL STRATEGIES ------------------------------ #

def tit_for_tat() -> StrategyActions_T:
	enemy_action = yield Action.DEAL
	while True:
		enemy_action = yield enemy_action


def tit_for_two_tats() -> StrategyActions_T:
	steal_cnt = 0
	enemy_action = yield Action.DEAL
	while True:
		if enemy_action == Action.DEAL:
			steal_cnt = 0
		else:
			steal_cnt += 1

		enemy_action = yield Action.DEAL if steal_cnt < 2 else Action.STEAL


def coin_flip() -> StrategyActions_T:
	while True:
		yield choice(ACTIONS)


def saint() -> StrategyActions_T:
	while True:
		yield Action.DEAL


def greedy() -> StrategyActions_T:
	while True:
		yield Action.STEAL


def liar() -> StrategyActions_T:
	yield Action.DEAL
	yield from greedy()


def vindictive() -> StrategyActions_T:
	enemy_action = yield Action.DEAL
	while enemy_action == Action.DEAL:
		enemy_action = yield Action.DEAL
	yield from greedy()


def undef_stat() -> StrategyActions_T:
	total_steals = 0
	deals_in_a_row = 0
	# Start with DEAL
	enemy_action = yield Action.DEAL
	for rounds_past in itertools.count(start=1):
		if enemy_action == Action.STEAL:
			# Immediate reaction on STEAL.
			total_steals += 1
			deals_in_a_row = 0
			enemy_action = yield Action.STEAL
		else:
			# If opponent apologizes - return to DEAL.
			# More he was STEALing in the past - longer he has to apologize.
			deals_in_a_row += 1
			# Let's denote
			# s = total_steals / rounds_past
			# General formula is:
			# apology_threshold = k * ln(1 / (1 - s))
			# with k = 2 / ln(2), so that apology_threshold equals 2 when
			# s is 50%.
			apology_threshold = 2 * math.log2(rounds_past / (rounds_past - total_steals))
			enemy_action = yield Action.STEAL if deals_in_a_row < apology_threshold else Action.DEAL


def undef_simple() -> StrategyActions_T:
	my_score, enemy_score = 0, 0
	while True:
		my_action = Action.STEAL if my_score < enemy_score else Action.DEAL
		enemy_action = yield my_action
		my_p, enemy_p = results.get_round_results(my_action, enemy_action)
		my_score += my_p
		enemy_score += enemy_p


def main():
	...


if __name__ == "__main__":
	main()
