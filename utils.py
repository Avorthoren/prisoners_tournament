from types import NoneType
from typing import Any, Callable, Hashable


def dict_set_default(
	d: dict,
	key: Hashable,
	default_factory: Callable,
	*args,
	**kwargs
) -> Any:
	"""Optimized version of dict.setdefault.

	Sometimes you want to use list/dict/set (or even more complex objects)
	as default value. Regular approach will create a lot of 'dead' objects
	before calling dict.setdefault.
	Current function solves this problem by passing factory instead, and
	creating objects only on demand.

	Additional args and kwargs will be passed to factory.
	"""
	if key in d:
		return d[key]

	default = default_factory(*args, **kwargs)
	d[key] = default
	return default


RandomState_T = tuple[int, tuple[int, ...], NoneType]


def random_state_pretty_str(random_state: RandomState_T, max_row_len: int = 120, indent: str = "\t") -> str:
	max_row_len -= len(indent)

	lines = [f"({random_state[0]}, ("]
	cur_len = 0
	numbers = []
	for n in random_state[1]:
		n_str = str(n)
		if cur_len + len(n_str) > max_row_len:
			lines.append(indent + ", ".join(numbers))
			cur_len = 0
			numbers = []

		numbers.append(n_str)
		cur_len += len(n_str)
	lines.append(f"), {random_state[2]})")

	return "\n".join(lines)


def _test(a: str, b: int):
	print(a, b)


def main():
	d = {}
	dict_set_default(d, 1, _test, "asd", "bfg")


if __name__ == "__main__":
	main()
