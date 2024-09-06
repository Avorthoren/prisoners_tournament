import random

RANDOM_STATE = None
if RANDOM_STATE is None:
	RANDOM_STATE = random.getstate()
else:
	random.setstate(RANDOM_STATE)

# If both did "DEAL" they get:
DEAL_POINTS = 3
# If both did "STEAL" they get:
STEAL_POINTS = 1
# If player did "DEAL" while another did "STEAL" first one gets:
DEAL_ON_STEAL_POINTS = 0
# If player did "STEAL" while another did "DEAL" first one gets:
STEAL_ON_DEAL_PINTS = 5

# Each pair of players will play this amount of matches.
TOTAL_MATCHES = 100

_MIN_ROUNDS = 50
_MAX_ROUNDS = 1000
_RANDOM_GENERATOR = random.randint


def get_total_rounds() -> int:
	"""Generate number of rounds in a match."""
	return _RANDOM_GENERATOR(_MIN_ROUNDS, _MAX_ROUNDS)

