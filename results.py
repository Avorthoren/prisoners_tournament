from __future__ import annotations
import dataclasses
import operator
from typing import Self, TYPE_CHECKING

from action import Action
from config import DEAL_POINTS, STEAL_POINTS, DEAL_ON_STEAL_POINTS, STEAL_ON_DEAL_PINTS
from utils import dict_set_default

if TYPE_CHECKING:
	from play import Match_T, Tournament_T


def get_round_results(a1: Action, a2: Action) -> tuple[int, int]:
	if a1 == Action.DEAL and a2 == Action.DEAL:
		return DEAL_POINTS, DEAL_POINTS
	elif a1 == Action.STEAL and a2 == Action.STEAL:
		return STEAL_POINTS, STEAL_POINTS
	elif a1 == Action.DEAL and a2 == Action.STEAL:
		return DEAL_ON_STEAL_POINTS, STEAL_ON_DEAL_PINTS
	elif a1 == Action.STEAL and a2 == Action.DEAL:
		return STEAL_ON_DEAL_PINTS, DEAL_ON_STEAL_POINTS
	else:
		raise RuntimeError(f"Unhandled player actions pair: {a1}, {a2}")


def get_match_results(match: Match_T) -> tuple[int, int, int]:
	score1, score2 = 0, 0
	for a1, a2 in match:
		p1, p2 = get_round_results(a1, a2)
		score1 += p1
		score2 += p2

	return score1, score2, len(match)


def show_match(match: Match_T) -> None:
	for i, (action1, action2) in enumerate(match):
		print(action1.bin(), action2.bin(), "|", get_round_results(action1, action2))


@dataclasses.dataclass
class PlayerResults:
	name: str
	score: int = 0
	total_rounds: int = 0

	def effectiveness(self) -> float:
		return self.score / (self.total_rounds * DEAL_POINTS)

	# def __add__(self, other: Self) -> Self:
	# 	return self.__class__(self.score + other.score, self.total_rounds + other.total_rounds)
	#
	# def __iadd__(self, other: Self) -> Self:
	# 	self.score += other.score
	# 	self.total_rounds += other.total_rounds
	# 	return self


# {player_name: player_results, ...}
TournamentResults_T = dict[str, PlayerResults]


def get_tournament_results(tournament: Tournament_T) -> TournamentResults_T:
	results = {}
	for (name1, name2), matches in tournament.items():
		player1_results = dict_set_default(results, name1, PlayerResults, name=name1)
		player2_results = dict_set_default(results, name2, PlayerResults, name=name2)
		for match in matches:
			score1, score2, total_rounds = get_match_results(match)
			player1_results.score += score1
			player1_results.total_rounds += total_rounds
			player2_results.score += score2
			player2_results.total_rounds += total_rounds

	return results


def get_tournament_results_str(results: TournamentResults_T, precision: int) -> str:
	sorted_results = sorted(results.values(), key=operator.attrgetter('score'), reverse=True)
	max_name_len = 1
	max_int_effectiveness_len = 1
	max_score_len = 1
	for result in sorted_results:
		if (name_len := len(result.name)) > max_name_len:
			max_name_len = name_len

		if (int_effectiveness_len := len(str(int(result.effectiveness())))) > max_int_effectiveness_len:
			max_int_effectiveness_len = int_effectiveness_len

		if (score_len := len(str(result.score))) > max_score_len:
			max_score_len = score_len
	max_effectiveness_len = max_int_effectiveness_len + 1 + precision

	# ___name: ___1.xxxx (___123/999)
	return "\n".join(
		f"{result.name.ljust(max_name_len)}: {result.effectiveness():{max_effectiveness_len}.{precision}f}"
		f" ({result.score:{max_score_len}}/{result.total_rounds})"
		for result in sorted_results
	)


def main():
	...


if __name__ == "__main__":
	main()
