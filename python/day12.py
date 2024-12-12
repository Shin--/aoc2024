from collections import defaultdict
from typing import TypeAlias
from utils import read_data


Plot: TypeAlias = tuple[int, int]
GardenArea: TypeAlias = set[Plot]


def calculate_perimeter(area: GardenArea) -> int:
  perimeter = 0
  for plot in area:
    perimeter += (4 - len(get_connected_plots(plot) & area))
  return perimeter


def calculate_sides(area: GardenArea) -> int:
  sides = 0

  def _are_neighbours(p1: Plot, p2: Plot) -> bool:
    x1, y1 = p1
    x2, y2 = p2

    if (x1 == x2 and abs(y1 - y2) == 1) or (y1 == y2 and abs(x1 - x2) == 1):
      return True
    return False
  
  for plot in area:
    x, y = plot
    plot_corners: list[GardenArea] = [
      {
        (x - 1, y),
        (x - 1, y - 1),
        (x, y- 1)
      },
      {
        (x, y - 1),
        (x + 1, y - 1),
        (x + 1, y)
      },
      {
        (x - 1, y),
        (x - 1, y + 1),
        (x, y + 1)
      },
      {
        (x + 1, y),
        (x + 1, y + 1),
        (x, y + 1)
      }
    ]
    for corners in plot_corners:
      corner_plots = corners & area
      if len(corner_plots) == 0:
        sides += 1
      elif len(corner_plots) == 2 and not _are_neighbours(*corner_plots):
        sides += 1
      elif len(corner_plots) == 1 and not _are_neighbours(plot, *corner_plots):
        sides += 1
  return sides



def get_connected_plots(plot: Plot) -> GardenArea:
  connected_plots: GardenArea = set()
  x, y = plot
  if y > 0:
    connected_plots.add((x, y - 1))
  if x > 0:
    connected_plots.add((x - 1, y))
  # Not properly checking if they are out of bounds, but the checks whether or not the plot exists handle it and I am too lazy to pass width and height
  connected_plots.add((x + 1, y))
  connected_plots.add((x, y + 1))
  return connected_plots


def get_plot_area(current_plot: Plot, plots: GardenArea, visited_plots: GardenArea) -> GardenArea:
  for connected_plot in get_connected_plots(current_plot):
    if connected_plot in plots:
      plots.remove(connected_plot)
      visited_plots.add(connected_plot)
      get_plot_area(connected_plot, plots, visited_plots)
  return visited_plots


def get_areas(data: list[str]) -> list[GardenArea]:
  plant_types: defaultdict[str, GardenArea] = defaultdict(set)
  areas: list[GardenArea] = list()

  for y, row in enumerate(data):
    for x, plant_type in enumerate(list(row)):
      plant_types[plant_type].add((x, y))

  for garden_plots in plant_types.values():
    while len(garden_plots):
      try:
        area: GardenArea = set()
        garden_plot = garden_plots.pop()
        area.add(garden_plot)
        area.update(get_plot_area(garden_plot, garden_plots, set()))
        areas.append(area)
      except KeyError:
        areas.append(area)
        pass
  
  return areas


def part_1(areas: list[GardenArea]) -> int:
  return sum([calculate_perimeter(area) * len(area) for area in areas])


def part_2(areas: list[GardenArea]) -> int:
  return sum([calculate_sides(area) * len(area) for area in areas])


if __name__ == '__main__':
  import time

  data = read_data(12, production=True)
  gardening_areas = get_areas(data)
  start_time = time.perf_counter()
  answer_part_1 = part_1(gardening_areas)
  end_time = time.perf_counter()
  print(f"Part 1 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

  start_time = time.perf_counter()
  answer_part_1 = part_2(gardening_areas)
  end_time = time.perf_counter()
  print(f"Part 2 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

