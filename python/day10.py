from typing import Optional
from utils import read_data


def go_hike(
    data: list[list[int]],
    location: tuple[int, int], 
    peaks: Optional[set[tuple[int, int]]] = None, 
    paths: Optional[list[tuple[int, int]]] = None
) -> tuple[set[tuple[int, int]], list[tuple[int, int]]]:
  def _get_height(x: int, y: int) -> int:
    return data[y][x]
  
  def _validate_location(location: tuple[int, int], height) -> bool:
    try:
      x, y = location
      if x >= 0 and y >= 0:
        return _get_height(*location) == height + 1
    except IndexError:
      pass
    return False
  
  if peaks is None:
    peaks = set()
  if paths is None:
    paths = list()

  up = (location[0], location[1] - 1)
  right = (location[0] + 1, location[1])
  down = (location[0], location[1] + 1)
  left = (location[0] - 1, location[1])
  current_height = data[location[1]][location[0]]
  for new_location in list(filter(lambda location: _validate_location(location, current_height), [up, right, down, left])):
    if _get_height(*new_location) == 9:
      peaks.add(new_location)
      paths.append(new_location)
    elif type(new_location) == tuple:
      go_hike(data, new_location, peaks, paths)
  return peaks, paths



def part_1_and_2(data: list[str]) -> tuple[int, int]:
  data_int = [[int(x) for x in row] for row in data]
  overall_score = 0
  paths_count = 0
  for y, row in enumerate(data_int):
    for x, val in enumerate(row):
      if val == 0:
        peaks, paths = go_hike(data_int, (x, y))
        overall_score += len(peaks)
        paths_count += len(paths)
  return overall_score, paths_count


if __name__ == '__main__':
  import time 

  data = read_data(10, production=True)
  start_time = time.perf_counter()
  answer_part_1, answer_part_2 = part_1_and_2(data)
  end_time = time.perf_counter()
  print(f"Part 1 - {answer_part_1} | Part 2 - {answer_part_2} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")
