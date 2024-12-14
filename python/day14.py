from collections import defaultdict
from dataclasses import dataclass, field
import math
from typing import Optional, TypeAlias
from utils import read_data


Point2D: TypeAlias = tuple[int, int]
Vector = Point2D
Square = tuple[Point2D, Point2D]


@dataclass
class Area:
  height: int
  width: int
  height_middle: int = field(init=False)
  width_middle: int = field(init=False)

  def __post_init__(self):
    self.height_middle = self.height // 2
    self.width_middle = self.width // 2


@dataclass
class Robot:
  location: Point2D
  velocity: Vector
  area: Area

  @property
  def is_in_middle(self) -> bool:
    x, y = self.location
    return x == self.area.width_middle or y == self.area.height_middle
  
  def get_square(self) -> Optional[str]:
    if self.is_in_middle:
      return None
    x, y = self.location
    if x < self.area.width_middle:
      if y < self.area.height_middle:
        return 'top-left'
      return 'bottom-left'
    else:
      if y < self.area.height_middle:
        return 'top-right'
      return 'bottom-right'
    
  
  def get_location(self, seconds: int) -> Point2D:
    location_x, location_y = self.location
    vx, vy = self.velocity
    new_location_x = (location_x + (vx * seconds)) % self.area.width
    new_location_y = (location_y + (vy * seconds)) % self.area.height
    return new_location_x, new_location_y
    

  def move(self, seconds=1):
    self.location = self.get_location(seconds)


def get_robots(data: list[str], area: Area) -> list[Robot]:
  robots: list[Robot] = list()
  for row in data:
    p_str, v_str = row.split(" ")
    px, py = p_str.split("p=")[1].split(",")
    vx, vy = v_str.split("v=")[1].split(",")
    robots.append(Robot(location=(int(px), int(py)), velocity=(int(vx), int(vy)), area=area))
  return robots


def part_1(data: list[str], width: int, height: int) -> int:
  robots = get_robots(data, Area(height=height, width=width))
  robots_in_squares: defaultdict[str, int] = defaultdict(int)
  for robot in robots:
    robot.move(100)
    robot_square = robot.get_square()
    if robot_square:
      robots_in_squares[robot_square] += 1

  return math.prod(robot_count for robot_count in robots_in_squares.values())



def part_2(data: list[str], width: int, height: int) -> int: 
  robots = get_robots(data, Area(height=height, width=width))

  def get_tree_crown(point: Point2D) -> set[Point2D]:
    tree_crown: set[Point2D] = set()
    x, y = point
    tree_crown.add(point)                 # The idea here is to start with X, then X*X, X***X etc.
    for i in range(1, 4):
      tree_crown.add((x - i, y + i))      # Add left tree branches
      tree_crown.add((x + i, y + i))      # Add right tree branches
    return tree_crown
  
  for i in range(100000):
    robot_locations: set[Point2D] = set()
    for robot in robots:
      robot_locations.add(robot.get_location(seconds=i))
    
    for location in robot_locations:
      tree_crown = get_tree_crown(location)
      if len(robot_locations & tree_crown) == len(tree_crown):
        return i

  # robot_locations: set[Point2D] = set()
  # for robot in robots:
  #   robot_locations.add(robot.get_location(seconds=6752))
  # print_robots(robot_locations)


  # From when I got really frustrated, after debuggin for almost 2h. I set the height to 107...
  # fig, ax = plt.subplots()
  # ax.set_xlim(0, width)
  # ax.set_ylim(height, 0)
  # for i in range(86, 10000, 101):
  #   ax.clear()
  #   ax.invert_yaxis()
  #   for robot in robots:
  #     x, y = robot.get_location(seconds=i)
  #     ax.plot(x, y, 'go')
  #   ax.text(0.5, 11, f"Seconds: {i}", fontsize=16)
  #   output_file = f"python/day14_images/seconds-{i}.png"
  #   plt.savefig(output_file)
  #   print(f"Saved: {output_file}")

  return 0


if __name__ == '__main__':
  import time 

  width = 101
  height = 103

  data = read_data(14, production=True)
  start_time = time.perf_counter()
  answer_part_1 = part_1(data, width, height)
  end_time = time.perf_counter()
  print(f"Part 1 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

  start_time = time.perf_counter()
  answer_part_1 = part_2(data, width, height)
  end_time = time.perf_counter()
  print(f"Part 2 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

