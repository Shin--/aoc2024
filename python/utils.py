def read_data(day: int, production: False) -> list[str]:
  content = ""
  with open(f'C:/Users/Tim/Repos/aoc2024/data/day{day}/{"production" if production else "dev"}.txt', 'r') as f:
    content = f.read().splitlines()
  return content