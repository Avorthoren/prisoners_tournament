from typing import Sequence, TYPE_CHECKING

from action import Action
import config
from utils import dict_set_default

if TYPE_CHECKING:
	from strategy import Strategy_T

Match_T = Sequence[tuple[Action, Action]]


def play_match(s1: 'Strategy_T', s2: 'Strategy_T', rounds: int) -> Match_T:
	# Prepare
	match = []
	sa1, sa2 = s1(), s2()
	# Process first moves.
	actions = next(sa1), next(sa2)
	match.append(actions)
	# Do the rest.
	for _ in range(rounds-1):
		# Pass last move of the second player to the first one and vice versa.
		actions = sa1.send(actions[1]), sa2.send(actions[0])
		match.append(actions)

	return match


# {strategy_pair_names: all_their_matches, ...}
Tournament_T = dict[tuple[str, str], Sequence[Match_T]]


def play_tournament(
	strategies: Sequence['Strategy_T'],
	repeat: int = config.TOTAL_MATCHES,
	play_itself: bool = False
) -> Tournament_T:
	"""Compete strategies in a tournament.

	Each strategy plays each other.
	If `play_itself` - each strategy will also play with itself.
	Number of rounds is defined ~randomly~ by `config.get_total_rounds`, but
	equal for every pair of strategies.
	Everything above will be repeated `repeat` times.

	Returns detailed results for each match.
	"""
	size = len(strategies)
	name_counters = {}
	names = []
	# Each strategy can appear multiple times in `strategies`, but we have to
	# separate their results, so we add indices to names.
	for s in strategies:
		if (cnt := name_counters.get(s.__name__)) is None:
			names.append(s.__name__)
			name_counters[s.__name__] = 1
		else:
			names.append(f"{s.__name__}{cnt}")
			name_counters[s.__name__] += 1

	tournament = {}
	for _ in range(repeat):
		total_rounds = config.get_total_rounds()
		for i in range(size if play_itself else size-1):
			s1 = strategies[i]
			for j in range(i if play_itself else i+1, size):
				s2 = strategies[j]
				match = play_match(s1, s2, total_rounds)
				pair_names = names[i], names[j]
				dict_set_default(tournament, pair_names, list).append(match)

	return tournament
