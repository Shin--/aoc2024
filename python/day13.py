from typing import Optional, TypeAlias
from utils import read_data


ClawMachineButton: TypeAlias = tuple[int, int]
ClawMachinePrize = ClawMachineButton
ClawMachine: TypeAlias = tuple[ClawMachineButton, ClawMachineButton, ClawMachinePrize]


def parse_details(details_str: str, detail_type: str) -> ClawMachineButton | ClawMachinePrize:
  x_str, y_str = details_str.split(", ")
  if detail_type == 'Prize':
    x = int(x_str.split('X=')[1])
    y = int(y_str.split('Y=')[1])
  else:
    x = int(x_str.split('X')[1])
    y = int(y_str.split('Y')[1])
  return (x, y)


def get_claw_machines(data: list[str]) -> list[ClawMachine]:
  button_a: Optional[ClawMachineButton] = None
  button_b: Optional[ClawMachineButton] = None
  prize_location: Optional[ClawMachinePrize] = None
  claw_machines: list[ClawMachine] = list()

  for row in data:
    if not len(row):
      continue
    row_type, details_str = row.split(': ')
    if row_type == 'Button A':
      button_a = parse_details(details_str, row_type)
    elif row_type == 'Button B':
      button_b = parse_details(details_str, row_type)
    elif row_type == 'Prize':
      prize_location = parse_details(details_str, row_type)
    if button_a and button_b and prize_location:
      claw_machines.append((button_a, button_b, prize_location))
      button_a, button_b, prize_location = None, None, None

  return claw_machines


def get_min_tokens(claw_machine: ClawMachine, error: int = 0) -> int:
  button_a, button_b, prize_location = claw_machine
  ax, ay = button_a
  bx, by = button_b
  px, py = prize_location
  px, py = px + error, py + error
  det = ax * by - bx * ay
  a_presses = (px * by - bx * py) / det
  b_presses = (ax * py - px * ay) / det
  if (a_presses >= 0 or b_presses >= 0) and a_presses.is_integer() and b_presses.is_integer():
    return int(a_presses * 3 + b_presses)
  return 0


def part_1(claw_machines: list[ClawMachine]) -> int:
  return sum([get_min_tokens(machine) for machine in claw_machines])


def part_2(claw_machines: list[ClawMachine]) -> int:
  return sum([get_min_tokens(machine, error=10_000_000_000_000) for machine in claw_machines])


if __name__ == '__main__':
  import time 

  data = read_data(13, production=True)

  start_time = time.perf_counter()
  claw_machines = get_claw_machines(data)
  end_time = time.perf_counter()
  print(f"Build machines (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

  start_time = time.perf_counter()
  answer_part_1 = part_1(claw_machines)
  end_time = time.perf_counter()
  print(f"Part 1 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

  start_time = time.perf_counter()
  answer_part_1 = part_2(claw_machines)
  end_time = time.perf_counter()
  print(f"Part 2 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

