from dataclasses import dataclass
import heapq
import math
from typing import TypeAlias
from utils import read_data

import sys
sys.setrecursionlimit(2000)


Point2D: TypeAlias = tuple[int, int]


@dataclass
class Maze:
  walls: set[Point2D]
  start: Point2D
  end: Point2D
  height: int
  width: int

  def is_valid_location(self, location: Point2D):
    x, y = location
    if not (0 < x < self.width) or not (0 < y < self.height):
      return False
    return location not in self.walls
  

def dijkstra_with_turn_cost(maze: Maze, turn_cost: int = 0) -> tuple[int, list[Point2D]]:
  directions: list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Down, Right, Up, Left

  pq: list[tuple[int, Point2D, list[Point2D], Point2D]] = [(0, maze.start, [], (1, 0))]
  visited: set[Point2D] = set()

  while pq:
    cost, location, path, last_direction = heapq.heappop(pq)

    if location in visited:
        continue

    visited.add(location)
    path = path + [location]

    # If we reach the destination, return the cost and path
    if location == maze.end:
        return cost, path

    for direction in directions:
        nx, ny = location[0] + direction[0], location[1] + direction[1]
        new_location = (nx, ny)

        if maze.is_valid_location(new_location) and (new_location, direction) not in visited:
            # Calculate the cost: 1 for a step, 1000 if the direction changes
            turn_cost = 1000 if last_direction and last_direction != direction else 0
            heapq.heappush(pq, (cost + turn_cost + 1, new_location, path, direction))

  # If no path is found
  return 0, list()


def dijkstra_find_all_paths(maze: Maze, turn_cost: int = 0) -> list[list[Point2D]]:
  directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Down, Right, Up, Left

  # Priority queue: (current cost, current position, current path, last direction)
  pq: list[tuple[int, Point2D, list[Point2D], Point2D]] = [(0, maze.start, [maze.start], (1, 0))]
  all_paths: list[list[Point2D]] = []
  min_cost_to_end = math.inf

  visited: dict[tuple[Point2D, Point2D], int] = {}  # Tracks the cost to (location, direction)

  while pq:
    cost, location, path, last_direction = heapq.heappop(pq)

    # If cost exceeds current minimum to the end, skip
    if cost > min_cost_to_end:
      continue

    # If we reach the end, check the cost. Only add if new minimal cost
    if location == maze.end:
      if cost < min_cost_to_end:
        min_cost_to_end = cost
        all_paths.clear()
      all_paths.append(path)
      continue

    # Explore all directions
    for direction in directions:
      nx, ny = location[0] + direction[0], location[1] + direction[1]
      new_location = (nx, ny)

      if maze.is_valid_location(new_location):
        additional_cost = 1000 if last_direction and last_direction != direction else 0
        total_cost = cost + 1 + additional_cost

        # Only proceed if new cost is equal to or better than a previous visit
        if (new_location, direction) not in visited or total_cost <= visited[(new_location, direction)]:
          visited[(new_location, direction)] = total_cost
          heapq.heappush(pq, (total_cost, new_location, path + [new_location], direction))

  return all_paths


def part_1(data: list[str]) -> int:
  start: Point2D = (0, 0)
  end: Point2D = (0, 0)
  walls: set[Point2D] = set()
  for y, row in enumerate(data):
    for x, val in enumerate(row):
      if val == '#':
        walls.add((x, y))
      elif val == 'S':
        start = (x, y)
      elif val == 'E':
        end = (x, y)
  
  maze = Maze(walls=walls, start=start, end=end, height=len(data), width=len(data[0]))
  cost, path = dijkstra_with_turn_cost(maze, turn_cost=1000)

  return cost


def part_2(data: list[str]) -> int:
  start: Point2D = (0, 0)
  end: Point2D = (0, 0)
  walls: set[Point2D] = set()
  for y, row in enumerate(data):
    for x, val in enumerate(row):
      if val == '#':
        walls.add((x, y))
      elif val == 'S':
        start = (x, y)
      elif val == 'E':
        end = (x, y)
  
  maze = Maze(walls=walls, start=start, end=end, height=len(data), width=len(data[0]))
  paths = dijkstra_find_all_paths(maze, turn_cost=1000)

  seats: set[Point2D] = set()
  for path in paths:
    seats.update(path)
  return len(seats)


if __name__ == '__main__':
  import time 

  data = read_data(16, production=True)
  start_time = time.perf_counter()
  answer_part_1 = part_1(data)
  end_time = time.perf_counter()
  print(f"Part 1 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

  start_time = time.perf_counter()
  answer_part_1 = part_2(data)
  end_time = time.perf_counter()
  print(f"Part 2 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")
