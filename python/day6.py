from collections import defaultdict
import copy
from dataclasses import dataclass, field
from shutil import move
from textwrap import fill
from typing import Dict, Literal, NewType, Optional, Set, Tuple
from xmlrpc.client import boolean
from utils import read_data


ObstacleGrid = NewType('ObstacleGrid', Dict[str, defaultdict[int, list[Tuple[int, int]]]])
Directions = Literal['up', 'right', 'down', 'left']

@dataclass
class Coordinates:
  x: int
  y: int

@dataclass
class Obstacle(Coordinates):
  pass

@dataclass
class Guard(Coordinates):
  direction: Directions
  area: Coordinates
  visited_locations: Set[Tuple[int, int]] = field(default_factory=set)
  reached_obstacles: Set[Tuple[int, int]] = field(default_factory=set)

  def __post_init__(self):
    self.visited_locations.add((self.x, self.y))

  @property
  def has_left_area(self) -> bool:
    if self.x < 0 or self.x >= self.area.x:
      return True
    if self.y < 0 or self.y >= self.area.y:
      return True
    return False
    
  def get_next_obstacle(self, obstacle_grid: ObstacleGrid) -> Obstacle | None:
    if self.direction in ['up', 'down']:
      obstacles_ahead = [
        (ox, oy) for ox, oy in obstacle_grid['x'][self.x]
        if (oy < self.y if self.direction == 'up' else oy > self.y)
      ]
      obstacles_ahead.sort(key=lambda obstacle: abs(obstacle[1] - self.y))
    else:
      obstacles_ahead = [
        (ox, oy) for ox, oy in obstacle_grid['y'][self.y]
        if (ox < self.x if self.direction == 'left' else ox > self.x)
      ]
      obstacles_ahead.sort(key=lambda obstacle: abs(obstacle[0] - self.x))
    if obstacles_ahead:
      return Obstacle(*obstacles_ahead[0])
    return None
  
  def get_visited_locations(self, start: Coordinates, end: Coordinates, direction: Literal['x', 'y']) -> Set[Tuple[int, int]]:
    visited_locations = set()
    if direction == 'x':
      min_val = min(start.x, end.x)
      max_val = max(start.x, end.x)
      for x in range(min_val, max_val):
        visited_locations.add((x, start.y))
    else:
      min_val = min(start.y, end.y)
      max_val = max(start.y, end.y)
      for y in range(min_val, max_val):
        visited_locations.add((start.x, y))
    return visited_locations
  
  def move_to_obstacle(self, obstacle: Obstacle) -> Set[Tuple[int, int]]:
    visited_locations = set()
    if self.direction == 'up':
      visited_locations = self.get_visited_locations(start=Coordinates(self.x, self.y), end=Coordinates(self.x, obstacle.y + 1), direction='y')
      self.y = obstacle.y + 1
      self.direction = 'right'
    elif self.direction == 'right':
      visited_locations = self.get_visited_locations(start=Coordinates(self.x, self.y), end=Coordinates(obstacle.x, self.y), direction='x')
      self.x = obstacle.x - 1
      self.direction = 'down'
    elif self.direction == 'down':
      visited_locations = self.get_visited_locations(start=Coordinates(self.x, self.y), end=Coordinates(self.x, obstacle.y), direction='y')
      self.y = obstacle.y - 1
      self.direction = 'left'
    elif self.direction == 'left':
      visited_locations = self.get_visited_locations(start=Coordinates(self.x, self.y), end=Coordinates(obstacle.x + 1, self.y), direction='x')
      self.x = obstacle.x + 1
      self.direction = 'up'
    return visited_locations
  
  def leave_area(self) -> Set[Tuple[int, int]]:
    if self.direction == 'up':
      return self.move_to_obstacle(Obstacle(x=self.x, y=-2))
    if self.direction == 'right':
      return self.move_to_obstacle(Obstacle(x=self.area.x + 1, y=self.y))
    if self.direction == 'down':
      return self.move_to_obstacle(Obstacle(x=self.x, y=self.area.y + 1))
    if self.direction == 'left':
      return self.move_to_obstacle(Obstacle(x=-2, y=self.y))

  def move(self, obstacle_grid: ObstacleGrid) -> int:
    next_obstacle = self.get_next_obstacle(obstacle_grid)
    initial_position = Coordinates(self.x, self.y)
    if not next_obstacle:
      visited_locations = self.leave_area()
    else:
      visited_locations = self.move_to_obstacle(next_obstacle)
    self.visited_locations.update(visited_locations)
    return int(((self.x - initial_position.x)**2 + (self.y - initial_position.y)**2)**0.5)


def part_1(obstacle_grid: ObstacleGrid, guard: Guard):
  while not guard.has_left_area:
    guard.move(obstacle_grid)
  print("Part 1:", len(guard.visited_locations))


def part_2(obstacle_grid: ObstacleGrid, guard: Guard):
  loop_obstacles: Set[Tuple[int, int]] = set()
  for y_pos in range(guard.area.y):
    y_obstacles = obstacle_grid['y'].get(y_pos, list())
    for x_pos in range(guard.area.x):
      obstacle = (x_pos, y_pos)
      if obstacle not in y_obstacles:
        tmp_obstacle_grid = copy.deepcopy(obstacle_grid)
        tmp_obstacle_grid['x'][x_pos].append(obstacle)
        tmp_obstacle_grid['y'][y_pos].append(obstacle)
        tmp_guard = Guard(x=guard.x, y=guard.y, direction=guard.direction, area=guard.area)
        stuck_count = 0
        while True and not tmp_guard.has_left_area:
          location_count_before = len(tmp_guard.visited_locations)
          tmp_guard.move(tmp_obstacle_grid)
          if location_count_before == len(tmp_guard.visited_locations):
            stuck_count += 1
          else:
            stuck_count = 0
          if stuck_count >= 3:
            loop_obstacles.add(obstacle)
            break
  print("Part 2:", len(loop_obstacles))

# obstacles: (7, 9) - (3, 8) - (1, 8) - (7, 7) - (6, 7) - (3, 6)

if __name__ == '__main__':
  import time
  obstacle_grid: ObstacleGrid = ObstacleGrid({
    'x': defaultdict(list),
    'y': defaultdict(list),
  })
  
  symbol_to_direction: dict[str, Directions] = {'^': 'up', '>': 'right', 'v': 'down', '<': 'left'}
  data = read_data(6, production=True)
  guard_1: Optional[Guard] = None
  guard_2: Optional[Guard] = None
  for y, row in enumerate(data):
    for x, val in enumerate(row):
      if val == '.':
        continue
      if val == '#':
        obstacle_grid['x'][x].append((x, y))
        obstacle_grid['y'][y].append((x, y))
      elif val in symbol_to_direction.keys():
        guard_1 = Guard(x=x, y=y, direction=symbol_to_direction[val], area=Coordinates(x=len(row), y=len(data)))
        guard_2 = Guard(x=x, y=y, direction=symbol_to_direction[val], area=Coordinates(x=len(row), y=len(data)))

  if guard_1:
    start = time.perf_counter()
    part_1(obstacle_grid, guard_1)
    print(f"Execution Time: {time.perf_counter() - start:.6f} seconds")
  if guard_2:
    start = time.perf_counter()
    part_2(obstacle_grid, guard_2)
    print(f"Execution Time: {time.perf_counter() - start:.6f} seconds")