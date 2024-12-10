from utils import read_data
from typing import Optional


data = read_data(2, production=True)

def check_report(report_values: list[int]) -> bool:
    last_value = report_values[0]
    is_increasing = last_value < report_values[1]
    for report_value in report_values[1:]:
      if abs(report_value - last_value) > 3 or (is_increasing != (last_value < report_value)) or last_value == report_value:
        return False
      last_value = report_value
    return True


def part_1() -> int:
  unsafe_reports = 0
  for report in data:
    if not check_report([int(x) for x in report.split(' ')]):
      unsafe_reports += 1
  return unsafe_reports


def part_2() -> int:
  unsafe_reports = 0
  for report in data:
    int_report = [int(x) for x in report.split(' ')]
    if not (check_report(int_report)):
      dampened_reports: list[int] = []
      for i in range(len(int_report)):
        dampened_reports.append(int_report[:i] + int_report[i+1:])
      if not any([check_report(dampened_report) for dampened_report in dampened_reports]):
        unsafe_reports += 1
  return unsafe_reports


print("Part 1 - Safe reports:", len(data) - part_1())
print("Part 2 - Safe reports:", len(data) - part_2())
