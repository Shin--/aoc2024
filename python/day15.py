from dataclasses import dataclass
from turtle import width
from typing import Literal, Optional, Sequence, TypeAlias, cast
from utils import read_data

Location: TypeAlias = tuple[int, int]
Vector = Location
Direction = Literal['^', '>', 'v', '<']
WideBox = tuple[Location, Location]


@dataclass
class WarehouseBase:
  length: int
  width: int
  robot: Location
  walls: set[Location]


@dataclass
class Warehouse(WarehouseBase):
  boxes: set[Location]

  def is_location_inside_warehouse(self, location: Location) -> bool:
    x, y = location
    return 0 < x <= self.width - 1 and 0 < y <= self.length - 1
  
  def get_locations_ahead(self, direction_v: Vector) -> set[Location]:
    direction_vx, direction_vy = direction_v
    steps = 0
    locations_ahead: set[Location] = set()

    while True:
      steps += 1
      robot_x, robot_y = self.robot
      location_ahead = (robot_x + direction_vx * steps, robot_y + direction_vy * steps)
      if not self.is_location_inside_warehouse(location_ahead):
        break
      if location_ahead in self.walls:
        break
      locations_ahead.add(location_ahead)

    return locations_ahead
  
  def can_move(self, locations: set[Location]) -> bool:
    if len(locations) == 0:
      return False
    return len(locations) != len(locations & self.boxes)
  
  def get_boxes_to_move(self, boxes: set[Location], direction_v: Vector) -> set[Location]:
    boxes_to_move: set[Location] = set()
    direction_vx, direction_vy = direction_v
    box = (self.robot[0] + direction_vx, self.robot[1] + direction_vy)
    while box in boxes:
      boxes_to_move.add(box)
      box = (box[0] + direction_vx, box[1] + direction_vy)
    return boxes_to_move
  
  def move_boxes(self, boxes: set[Location], direction_v: Vector):
    direction_vx, direction_vy = direction_v
    moved_boxes: list[Location] = list()
    for box in boxes:
      self.boxes.remove(box)
      moved_boxes.append((box[0] + direction_vx, box[1] + direction_vy))
    self.boxes.update(moved_boxes)


  def move_robot(self, direction: Direction):
    directions = {
      '^': (0, -1),
      '>': (1, 0),
      'v': (0, 1),
      '<': (-1, 0)
    }

    direction_v = directions[direction]
    locations_ahead = self.get_locations_ahead(direction_v)
    if self.can_move(locations_ahead):
      boxes = self.boxes & locations_ahead
      boxes_to_move = self.get_boxes_to_move(boxes, direction_v)
      self.move_boxes(boxes_to_move, direction_v)
      self.robot = (self.robot[0] + direction_v[0], self.robot[1] + direction_v[1])


@dataclass
class WideWarehouse(WarehouseBase):
  boxes: set[WideBox]

  def is_location_inside_warehouse(self, location: Location) -> bool:    
    # print("Location:", location, "In walls?", location in self.walls)
    if location in self.walls:
      return False
    x, y = location
    return 1 < x <= self.width - 2 and 0 < y <= self.length - 1
  
  def get_locations_ahead(self, direction_v: Vector) -> set[Location]:
    direction_vx, direction_vy = direction_v
    steps = 0
    locations_ahead: set[Location] = set()

    while True:
      steps += 1
      robot_x, robot_y = self.robot
      location_ahead = (robot_x + direction_vx * steps, robot_y + direction_vy * steps)
      if not self.is_location_inside_warehouse(location_ahead):
        break
      if location_ahead in self.walls:
        break
      locations_ahead.add(location_ahead)

    return locations_ahead
  
  def can_move_box(self, box: WideBox, direction_v: Vector) -> bool:
    box_left_part, box_right_part = box
    direction_vx, direction_vy = direction_v
    if (box_left_part[0] + direction_vx, box_left_part[1] + direction_vy) in self.walls:
      return False
    if (box_right_part[0] + direction_vx, box_right_part[1] + direction_vy) in self.walls:
      print("1", (box_right_part[0] + direction_vx, box_right_part[1] + direction_vy))
      return False
    return True

  
  def get_boxes_to_move(self, previous_location: Location, direction_v: Vector) -> set[WideBox] | Literal[False]:
    def _add_box_and_connected_boxes(_box: WideBox, _boxes: set[WideBox]):
      _boxes.add(_box)
      left_box_part, right_box_part = _box
      boxes_to_move_left = self.get_boxes_to_move(left_box_part, direction_v)
      boxes_to_move_right = self.get_boxes_to_move(right_box_part, direction_v)
      if boxes_to_move_right is False or boxes_to_move_left is False:
        return False
      boxes.update(boxes_to_move_left)
      boxes.update(boxes_to_move_right)

    boxes: set[WideBox] = set()
    direction_vx, direction_vy = direction_v
    px, py = previous_location
    if direction_vy != 0:
      left_box = ((px - 1, py + direction_vy), (px, py + direction_vy))
      right_box = ((px, py + direction_vy), (px + 1, py + direction_vy))
      left_right_boxes = [left_box, right_box]
      
      flattened_boxes = {box_part for box in left_right_boxes for box_part in box if box in self.boxes}
      if len({left_box, right_box} & self.boxes) == 0:
        return boxes

      for box in left_right_boxes:
        if box in self.boxes and not self.can_move_box(box, direction_v):
          return False
      
      for flattened_box in flattened_boxes:
        if not self.is_location_inside_warehouse(flattened_box):
          return False
      
      if left_box in self.boxes:
        if _add_box_and_connected_boxes(left_box, boxes) is False:
          return False

      if right_box in self.boxes:
        if _add_box_and_connected_boxes(right_box, boxes) is False:
          return False
    else:
      robot_x, robot_y = self.robot
      if direction_vx == -1:
        box = ((robot_x - 2, robot_y), (robot_x - 1, robot_y))
        if box in self.boxes and not self.can_move_box(box, direction_v):
          return False
        while box in self.boxes:
          boxes.add(box)
          box = ((box[0][0] - 2, robot_y), (box[1][0] - 2, robot_y))
          if box not in self.boxes:
            break
          if not self.can_move_box(box, direction_v):
            return False
      else:
        box = ((robot_x + 1, robot_y), (robot_x + 2, robot_y))
        if box in self.boxes and not self.can_move_box(box, direction_v):
          return False
        while box in self.boxes:
          boxes.add(box)
          box = ((box[0][0] + 2, robot_y), (box[1][0] + 2, robot_y))
          if box not in self.boxes:
            break
          if not self.can_move_box(box, direction_v):
            return False
      
      if box in self.walls:
        return False
    
    return boxes
  
  def move_boxes(self, boxes: set[WideBox], direction_v: Vector):
    direction_vx, direction_vy = direction_v
    moved_boxes: list[WideBox] = list()
    for box in boxes:
      self.boxes.remove(box)
      left_box_part, right_box_part = box
      moved_boxes.append((
        (left_box_part[0] + direction_vx, left_box_part[1] + direction_vy),
        (right_box_part[0] + direction_vx, right_box_part[1] + direction_vy)
      ))
    self.boxes.update(moved_boxes)


  def move_robot(self, direction: Direction) -> bool:
    directions = {
      '^': (0, -1),
      '>': (1, 0),
      'v': (0, 1),
      '<': (-1, 0)
    }

    direction_v = directions[direction]
    robot_new_location = (self.robot[0] + direction_v[0], self.robot[1] + direction_v[1])
    if not self.is_location_inside_warehouse(robot_new_location):
      return False
    boxes_to_move = self.get_boxes_to_move(self.robot, direction_v)
    if boxes_to_move != False:
      self.move_boxes(boxes_to_move, direction_v)
      self.robot = (self.robot[0] + direction_v[0], self.robot[1] + direction_v[1])
    else:
      return False

    return True


def part_1(data: list[str]) -> int:
  is_warehouse = True
  length = 0
  walls: set[Location] = set()
  boxes: set[Location] = set()
  robot: Location = (0, 0)
  move_instructions: Sequence[Direction] = list()
  for y, row in enumerate(data):
    if not len(row):
      is_warehouse = False
      length = y
      continue
    if is_warehouse:
      for x, val in enumerate(row):
        if val == '#':
          walls.add((x, y))
        elif val == 'O':
          boxes.add((x, y))
        elif val == '@':
          robot = (x, y)
    elif len(row):
      move_instructions = cast(Sequence[Direction], list(row))

  warehouse = Warehouse(length, len(data[1]), robot, walls, boxes)

  for move_instruction in move_instructions:
    warehouse.move_robot(move_instruction)

  return sum([(x + y * 100) for x, y in warehouse.boxes])


def part_2(data: list[str]) -> int:
  is_warehouse = True
  length = 0
  walls: set[Location] = set()
  boxes: set[WideBox] = set()
  robot: Location = (0, 0)
  move_instructions: Sequence[Direction] = list()
  for y, row in enumerate(data):
    if not len(row):
      is_warehouse = False
      length = y
      continue
    if is_warehouse:
      for x, val in enumerate(row):
        location1 = (x * 2, y)
        location2 = (x * 2 + 1, y)
        if val == '#':
          walls.add(location1)
          walls.add(location2)
        elif val == 'O':
          boxes.add((location1, location2))
        elif val == '@':
          robot = location1
    elif len(row):
      move_instructions = cast(Sequence[Direction], list(row))

  width = len(data[1]) * 2
  warehouse = WideWarehouse(length, width, robot, walls, boxes)

  counter = 0
  for move_instruction in move_instructions:
    warehouse.move_robot(move_instruction)
    counter += 1

  score = 0
  for box in warehouse.boxes:
    x, y = box[0]
    score += x + y * 100
  return score



if __name__ == '__main__':
  import time 

  data = read_data(15, production=True)
  start_time = time.perf_counter()
  answer_part_1 = part_1(data)
  end_time = time.perf_counter()
  print(f"Part 1 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

  start_time = time.perf_counter()
  answer_part_1 = part_2(data)
  end_time = time.perf_counter()
  print(f"Part 2 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")
