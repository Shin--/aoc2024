from collections import defaultdict
from dataclasses import dataclass, field
from itertools import combinations
from utils import read_data


@dataclass
class InstallationsMap:
  height: int
  width: int
  antennas: defaultdict[str, set[tuple[int, int]]] = field(default_factory=lambda: defaultdict(set))
  antinodes: defaultdict[str, set[tuple[int, int]]] = field(default_factory=lambda: defaultdict(set))

  @property
  def unique_antinodes(self) -> set[tuple[int, int]]:
    unique_antinodes: set[tuple[int, int]] = set()
    for antinodes in self.antinodes.values():
      unique_antinodes.update(antinodes)
    return unique_antinodes

  def is_valid_antinode(self, antinode: tuple[int, int]) -> bool:
    x, y = antinode
    return 0 <= x < self.width and 0 <= y < self.height
  
  def add_antinode(self, antinode: tuple[int, int], antenna_type: str) -> bool:
    if self.is_valid_antinode(antinode):
      self.antinodes[antenna_type].add(antinode)
      return True
    return False


def init_installations_map(data) -> InstallationsMap:
  installations_map = InstallationsMap(height=len(data), width=len(data[0]))
  for y, row in enumerate(data):
    for x, val in enumerate(row):
      if val != '.':
        installations_map.antennas[val].add((x, y))
  return installations_map


def part_1(data) -> int:
  installations_map = init_installations_map(data)
  for antenna_type, antennas in installations_map.antennas.items():
    antenna_pairs = set(combinations(antennas, 2))
    for antenna_pair in antenna_pairs:
      a1, a2 = antenna_pair
      vector = (a2[0] - a1[0], a2[1] - a1[1])
      antinode1 = (a1[0] - vector[0], a1[1] - vector[1])
      antinode2 = (a2[0] + vector[0], a2[1] + vector[1])
      installations_map.add_antinode(antinode1, antenna_type)
      installations_map.add_antinode(antinode2, antenna_type)
  return len(installations_map.unique_antinodes)


def part_2(data):
  installations_map = init_installations_map(data)
  for antenna_type, antennas in installations_map.antennas.items():
    antenna_pairs = set(combinations(antennas, 2))
    for antenna_pair in antenna_pairs:  
      for i in range(1, installations_map.width):
        a1, a2 = antenna_pair
        vector = ((a2[0] - a1[0]) * i, (a2[1] - a1[1]) * i)
        antinode1 = (a1[0] - vector[0], a1[1] - vector[1])
        antinode2 = (a2[0] + vector[0], a2[1] + vector[1])
        if i == 1:
          installations_map.add_antinode(a1, antenna_type)
          installations_map.add_antinode(a2, antenna_type)
        antinodes_added = [installations_map.add_antinode(antinode1, antenna_type), installations_map.add_antinode(antinode2, antenna_type)]
        if not any(antinodes_added):
          break
  return len(installations_map.unique_antinodes)


if __name__ == '__main__':
  import time
  data = read_data(8, production=True)

  start_time = time.perf_counter()
  answer_part_1 = part_1(data)
  end_time = time.perf_counter()
  print(f"Part 1 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

  start_time = time.perf_counter()
  answer_part_2 = part_2(data)
  end_time = time.perf_counter()
  print(f"Part 2 - {answer_part_2} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")
