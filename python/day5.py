import copy
from functools import cmp_to_key
from typing import Optional, Set, Tuple
from utils import read_data


class ValidationError(Exception):
  def __init__(self, v1: str, v2: str, *args):
    super().__init__(*args)
    self.v1 = v1
    self.v2 = v2


def parse_data(data: list) -> Tuple[dict[str, Set[str]], list[list[str]]]:
  page_ordering_rules: dict[str, Set[str]] = dict()
  page_updates_list: list[list[str]] = list()

  parse_page_ordering_rules = True
  for row in data:
    if parse_page_ordering_rules:
      if not len(row):
        parse_page_ordering_rules = False
      else:
        v1, v2 = row.split('|')
        if v1 not in page_ordering_rules:
          page_ordering_rules[v1] = set()
        page_ordering_rules[v1].add(v2)
    else:
      page_updates_list.append(row.split(','))
  
  return page_ordering_rules, page_updates_list


def validate_update_order(updates: list[str], rules: dict[str, Set[str]], previous_values: Optional[list[str]] = None) -> bool:
  if not previous_values:
    previous_values = list()
  update_value = updates.pop(0)
  rule_set = rules.get(update_value)
  if rule_set:
    for v in rule_set:
      if v in previous_values:
        raise ValidationError(update_value, v)
  if update_value:
    previous_values.append(update_value)
    if len(updates):
      validate_update_order(updates, rules, previous_values)
  return True


def part_1(page_ordering_rules: dict[str, Set[str]], page_updates_list: list[list[str]]) -> int:
  valid_updates_sum = 0
  for page_updates in page_updates_list:
    try:
      middle_number = page_updates[int(len(page_updates)/2)]
      validate_update_order(page_updates, page_ordering_rules)
      valid_updates_sum += int(middle_number)
    except ValidationError:
      pass
  return valid_updates_sum

# Very inefficient while loop. Takes like 5s, but it works. Could just write a custom sort function to get them in order tbh
def part_2(page_ordering_rules: dict[str, Set[str]], page_updates_list: list[list[str]]) -> int:
  invalid_updates_sum = 0
  all_valid = False
  corrected_lists: Set[int] = set()
  while not all_valid:  
    validation_list: list[bool] = list()
    for (index, page_updates) in enumerate(page_updates_list):
      try:
        valid = validate_update_order(copy.deepcopy(page_updates), page_ordering_rules)
        validation_list.append(valid)
      except ValidationError as e:
        v1, v2 = e.v1, e.v2
        index_v1, index_v2 = page_updates.index(v1), page_updates.index(v2)
        page_updates[index_v2], page_updates[index_v1] = page_updates[index_v1], page_updates[index_v2]
        validation_list.append(False)
        corrected_lists.add(index)
        break
    all_valid = all(validation_list)
  for correct_list_index in corrected_lists:
    corrected_list = page_updates_list[correct_list_index]
    invalid_updates_sum += int(corrected_list[int(len(corrected_list)/2)])
  return invalid_updates_sum

# Ok, this is much better
def part_2_optimised(page_ordering_rules: dict[str, Set[str]], page_updates_list: list[list[str]]) -> int:
  def _is_invalid_page_update(page_updates: list[str]) -> bool:
    try:
      validate_update_order(page_updates.copy(), page_ordering_rules)
    except ValidationError:
      return True
    return False
  
  def _compare_update_order(v1: str, v2: str):
    if v2 in page_ordering_rules.get(v1, set()):
        return -1
    elif v1 in page_ordering_rules.get(v2, set()):
        return 1
    else:
        return 0
  
  def _fix_order(updates: list[str]) -> list[str]:
    return sorted(updates, key=cmp_to_key(_compare_update_order))
  
  invalid_updates = list(filter(lambda page_updates: _is_invalid_page_update(page_updates), page_updates_list))
  invalid_updates_sum = 0
  for invalid_update in invalid_updates:
    corrected_list = _fix_order(invalid_update)
    invalid_updates_sum += int(corrected_list[int(len(corrected_list)/2)])
  return invalid_updates_sum


if __name__ == '__main__':
  import time
  page_ordering_rules, page_updates_list = parse_data(read_data(5, production=True))
  start_time_p1 = time.perf_counter()
  p1 = part_1(page_ordering_rules, copy.deepcopy(page_updates_list))
  end_time_p1 = time.perf_counter()
  print(f"Part 1 - {p1} (Execution Time: {end_time_p1 - start_time_p1:.6f} seconds)")
  
  start_time_p2 = time.perf_counter()
  p2 = part_2(page_ordering_rules, copy.deepcopy(page_updates_list))
  end_time_p2 = time.perf_counter()
  print(f"Part 2 (slow) - {p2} (Execution Time: {end_time_p2 - start_time_p2:.6f} seconds)")
  
  start_time_p2_opt = time.perf_counter()
  p2_opt = part_2_optimised(page_ordering_rules, copy.deepcopy(page_updates_list))
  end_time_p2_opt = time.perf_counter()
  print(f"Part 2 (optimised) - {p2_opt} (Execution Time: {end_time_p2_opt - start_time_p2_opt:.6f} seconds)")
 