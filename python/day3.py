import math
import re
from utils import read_data

data = read_data(3, production=True)

def part_1() -> int:
  pattern = r'mul\((\d+),(\d+)\)'
  total_value: int = 0
  for row in data:
    for value_pair in re.findall(pattern, row):
      total_value += math.prod([int(x) for x in value_pair])
  return total_value

def part_2() -> int:
  pattern = r'mul\((\d+),(\d+)\)|don\'t\(\)|do\(\)'
  total_value: int = 0
  do_active = True
  for row in data:
    for match in re.finditer(pattern, row):
      if do_active and match.group(0).startswith('mul'):
        total_value += int(match.group(1)) * int(match.group(2))
      elif match.group(0).startswith('do()'):
        do_active = True
      elif match.group(0).startswith('don\'t()'):
        do_active = False
  return total_value

if __name__ == '__main__':
  print(part_1())
  print(part_2())