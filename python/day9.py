from utils import read_data

def part_1(data: list[str]) -> int:
  checksum = 0
  for row in data:
    vals = list(row)
    file_blocks = [[int(i/2)] * int(j) for i, j in enumerate(vals) if i % 2 == 0]
    space_blocks = [[-1] * int(j) for i, j in enumerate(vals) if i % 2]
    selected_space_block_index = 0

    for file_block in reversed(file_blocks):
      if selected_space_block_index >= len(space_blocks):
        break
      space_block = space_blocks[selected_space_block_index]
      space_left = space_block.count(-1)
      while True and space_left:
        try:
          file_block_id = file_block.pop()
          if selected_space_block_index >= file_block_id:
            file_block.append(file_block_id)
            break
        except IndexError: 
          break
        space_block[space_block.index(-1)]  = file_block_id
        space_left -= 1
        while not space_left:
          try:
            selected_space_block_index += 1
            space_block = space_blocks[selected_space_block_index]
            space_left = space_block.count(-1)
          except IndexError:
            break

    new_file_order: list[int] = list()
    for i in range(len(file_blocks) + len(space_blocks)):
      if i % 2 == 0:
        new_file_order += file_blocks[int(i/2)]
      else:
        new_file_order += space_blocks[int((i-1)/2)]  

    for i, val in enumerate(list(filter(lambda x: x != -1, new_file_order))):
      checksum += i * val
    
  return checksum


def part_2(data: list[str]) -> int:
  checksum = 0
  for row in data:
    vals = list(row)
    file_blocks = [[int(i/2)] * int(j) for i, j in enumerate(vals) if i % 2 == 0]
    space_blocks = [[-1] * int(j) for i, j in enumerate(vals) if i % 2]

    for file_block_id in range(len(file_blocks) - 1, -1, -1):
      file_block = file_blocks[file_block_id]
      
      for selected_space_block_index in range(len(space_blocks)):
        space_block = space_blocks[selected_space_block_index]
        space_left = space_block.count(-1)
        if selected_space_block_index >= file_block_id:
          break

        if len(file_block) <= space_left:
          space_block[space_block.index(-1):space_block.index(-1) + len(file_block)] = file_block
          space_left -= len(file_block)
          file_blocks[file_block_id] = [-1] * len(file_block)
          break
    
    new_file_order: list[int] = list()
    for i in range(len(file_blocks) + len(space_blocks)):
      if i % 2 == 0:
        new_file_order += file_blocks[int(i/2)]
      else:
        new_file_order += space_blocks[int((i-1)/2)]  

    checksum = 0
    for i, val in enumerate(new_file_order):
      if val != -1:
        checksum += i * val

  return checksum
    


if __name__ == '__main__':
  import time 

  data = read_data(9, production=True)
  start_time = time.perf_counter()
  answer_part_1 = part_1(data)
  end_time = time.perf_counter()
  print(f"Part 1 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

  start_time = time.perf_counter()
  answer_part_1 = part_2(data)
  end_time = time.perf_counter()
  print(f"Part 2 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

