# Tested for python 3.12.1
import config
import play
import results
import strategy
import utils


def main_tournament():
	strategies = (
		strategy.tit_for_tat,
		strategy.tit_for_two_tats,
		strategy.coin_flip,
		strategy.tit_for_tat,
		strategy.tit_for_two_tats,
		strategy.coin_flip,
		strategy.saint,
		strategy.greedy,
		strategy.liar,
		strategy.vindictive,
		strategy.undef_stat,
		strategy.undef_simple
	)
	tournament = play.play_tournament(strategies)
	tournament_results = results.get_tournament_results(tournament)
	print(f"RANDOM_STATE = {utils.random_state_pretty_str(config.RANDOM_STATE)}")
	print()
	print(results.get_tournament_results_str(tournament_results, precision=4))


def test_match(s1: strategy.Strategy_T, s2: strategy.Strategy_T):
	match = play.play_match(s1, s2, rounds=10)
	results.show_match(match)
	score1, score2, total_rounds = results.get_match_results(match)
	print(f"Score is {score1} to {score2} over {total_rounds} rounds")


def main():
	main_tournament()
	# test_match(strategy.coin_flip, strategy.liar)


if __name__ == "__main__":
	main()
