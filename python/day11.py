from collections import defaultdict
from utils import read_data


def transform_stones(stones: defaultdict[int, int]) -> defaultdict:
    new_stones: defaultdict[int, int] = defaultdict(int)

    for stone, index in stones.items():
        if stone == 0:
            new_stones[1] += stones[0]
        elif len(str(stone)) % 2 == 0:
            str_stone = str(stone)
            stone1, stone2 = int(str_stone[:len(str_stone) // 2]), int(str_stone[len(str_stone) // 2:])
            new_stones[stone1] += stones[stone]
            new_stones[stone2] += stones[stone]
        else:
            new_stones[stone * 2024] += stones[stone]

    return new_stones


def blink_n_times(stones: defaultdict[int, int], blinks: int) -> defaultdict[int, int]:
  for blink in range(blinks):
    stones = transform_stones(stones)
  return stones
    
   

def part_1(data) -> int:
  stones: defaultdict[int, int] = defaultdict(int)
  for row in data:
    stone_row = [int(x) for x in row.split(' ')]
    for stone in stone_row:
       stones[stone] += 1
    stones = blink_n_times(stones, 25)
  return sum(stones.values())


def part_2(data) -> int:
  stones: defaultdict[int, int] = defaultdict(int)
  for row in data:
    stone_row = [int(x) for x in row.split(' ')]
    for stone in stone_row:
       stones[stone] += 1
    stones = blink_n_times(stones, 75)
  return sum(stones.values())


if __name__ == '__main__':
  import time 

  data = read_data(11, production=True)
  start_time = time.perf_counter()
  answer_part_1 = part_1(data)
  end_time = time.perf_counter()
  print(f"Part 1 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

  start_time = time.perf_counter()
  answer_part_1 = part_2(data)
  end_time = time.perf_counter()
  print(f"Part 2 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

