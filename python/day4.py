from dataclasses import dataclass
from utils import read_data

@dataclass
class Dimensions:
  x: int
  y: int

def has_space_left(x: int, search: str):
  return x >= (len(search) - 1)

def has_space_right(x: int, search: str, dims: Dimensions):
  return x + (len(search) - 1) < dims.x

def has_space_up(y: int, search: str):
  return y - (len(search) - 1) >= 0

def has_space_down(y: int, search: str, dims: Dimensions):
  return y + (len(search) - 1) < dims.y

def check_horizontal(data: list[str], x: int, y: int, search: str, dims: Dimensions) -> bool:
  if has_space_right(x, search, dims):
    return data[y][x:x+4] == search
  return False

def check_horizontal_reverse(data: list[str], x: int, y: int, search: str) -> bool:
  if has_space_left(x, search):
    return data[y][x-3:x+1] == search[::-1]
  return False

def check_vertical(data: list[str], x: int, y: int, search: str, dims: Dimensions) -> bool:
  if has_space_down(y, search, dims):
    return "".join([data[y+i][x] for i in range(len(search))]) == search
  return False

def check_vertical_reverse(data: list[str], x: int, y: int, search: str) -> bool:
  if has_space_up(y, search):
    return "".join([data[y-i][x] for i in range(len(search))]) == search
  return False

def diagonal_down(data: list[str], x: int, y: int, search: str, dims: Dimensions) -> bool:
  if has_space_right(x, search, dims) and has_space_down(y, search, dims):
    return "".join([data[y+i][x+i] for i in range(len(search))]) == search
  return False

def diagonal_down_reverse(data: list[str], x: int, y: int, search: str) -> bool:
  if has_space_left(x, search) and has_space_up(y, search):
    return "".join([data[y-i][x-i] for i in range(len(search))]) == search
  return False

def diagonal_up(data: list[str], x: int, y: int, search: str, dims: Dimensions) -> bool:
  if has_space_right(x, search, dims) and has_space_up(y, search):
    return "".join([data[y-i][x+i] for i in range(len(search))]) == search
  return False

def diagonal_up_reverse(data: list[str], x: int, y: int, search: str, dims: Dimensions) -> bool:
  if has_space_left(x, search) and has_space_down(y, search, dims):
    return "".join([data[y+i][x-i] for i in range(len(search))]) == search
  return False


data = read_data(4, production=True)
dims = Dimensions(x=len(data[0]), y=len(data))

def part_1():
  search = 'XMAS'
  found_search = 0
  for i, row in enumerate(data):
    for j, c in enumerate(row):
      if c == 'X':
        if check_horizontal(data, j, i, search, dims):
          found_search += 1
        if check_horizontal_reverse(data, j, i, search):
          found_search += 1
        if check_vertical(data, j, i, search, dims):
          found_search += 1
        if check_vertical_reverse(data, j, i, search):
          found_search += 1
        if diagonal_down(data, j, i, search, dims):
          found_search += 1
        if diagonal_down_reverse(data, j, i, search):
          found_search += 1
        if diagonal_up(data, j, i, search, dims):
          found_search += 1
        if diagonal_up_reverse(data, j, i, search, dims):
          found_search += 1
  print(found_search)


def part_2():
  searches = ['MAS', 'SAM']
  center_char = 'A'
  crosses = 0
  for i, row in enumerate(data):
    for j, c in enumerate(row):
      if c == center_char and 0 < i < (dims.y - 1) and 0 < j < (dims.x - 1):
        if f"{data[i-1][j-1]}{data[i][j]}{data[i+1][j+1]}" in searches and f"{data[i+1][j-1]}{data[i][j]}{data[i-1][j+1]}" in searches:
          crosses += 1
  print(crosses)




if __name__ == '__main__':
  part_1()
  part_2()
