from typing import Literal
from utils import read_data


def find_operators(values: list[int], goal: int, operators: list[Literal['+', '*', '||']], previous_value: int = 0) -> bool:
  if not values:
    if goal == previous_value:
      return True
    else:
      return False
  value = values.pop(0)
  possible_operators: list[bool] = list()
  for operator in operators:
    if operator == '+':
      possible_operators.append(find_operators(values.copy(), goal, operators, previous_value + value))
    elif operator == '*':
      possible_operators.append(find_operators(values.copy(), goal, operators, previous_value * value))
    else:
      possible_operators.append(find_operators(values.copy(), goal, operators, int(str(previous_value) + str(value))))
  return any(possible_operators)


def part_1(data: list[str]) -> int:
  results_sum = 0
  for row in data:
    result, values = row.split(': ')
    int_values = [int(x) for x in values.split(' ')]
    if find_operators(int_values.copy(), int(result), operators=['*', '+']):
      results_sum += int(result)
  return results_sum


def part_2(data: list[str]) -> int:
  results_sum = 0
  for row in data:
    result, values = row.split(': ')
    int_values = [int(x) for x in values.split(' ')]
    if find_operators(int_values.copy(), int(result), operators=['*', '+', '||']):
      results_sum += int(result)
  return results_sum


if __name__ == '__main__':
  data = read_data(7, production=True)
  print("Part 1 -", part_1(data))
  print("Part 2 -", part_2(data))