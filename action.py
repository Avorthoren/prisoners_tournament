from enum import Enum


class Action(Enum):
	DEAL = 0
	STEAL = 1

	def bin(self) -> int:
		return 0 if self == Action.DEAL else 1


ACTIONS = tuple(Action)
