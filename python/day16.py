from utils import read_data


def part_1(data: list[str]) -> int:
  return 0



def part_2(data: list[str]) -> int:
  return 0


if __name__ == '__main__':
  import time 

  data = read_data(16, production=False)
  start_time = time.perf_counter()
  answer_part_1 = part_1(data)
  end_time = time.perf_counter()
  print(f"Part 1 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

  # start_time = time.perf_counter()
  # answer_part_1 = part_2(data)
  # end_time = time.perf_counter()
  # print(f"Part 2 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")
