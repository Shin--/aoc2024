from dataclasses import dataclass
from typing import Optional
from utils import read_data


@dataclass
class Register:
  A: int
  B: int
  C: int


def get_combo_operand(operand: int, register: Register) -> int:
  if 0 <= operand <= 3:
    return operand
  if operand == 4:
    return register.A
  if operand == 5:
    return register.B
  if operand == 6:
    return register.C 
  raise ValueError


def adv(operand: int, register: Register):
  register.A = int(register.A / (2**get_combo_operand(operand, register)))


def bxl(operand: int, register: Register):
  register.B = register.B ^ operand

def bst(operand: int, register: Register):
  register.B = get_combo_operand(operand, register) % 8

def jnz(operand: int, register: Register) -> Optional[int]:
  if register.A != 0:
    return operand
  return None

def bxc(operand: int, register: Register):
  register.B = register.B ^ register.C

def out(operand: int, register: Register) -> int:
  return get_combo_operand(operand, register) % 8

def bdv(operand: int, register: Register):
  register.B = int(register.A / (2**get_combo_operand(operand, register)))

def cdv(operand: int, register: Register):
  register.C = int(register.A / (2**get_combo_operand(operand, register)))


# # 0: adv -> division | Numerator: A register, denominator: <combo operand>^2 | Result: int(), saved to A
# # 1: bxl -> bitwise xor of B and literal operand. Save to B
# # 2: bst -> combo operand % 8. Save to B
# # 3: jnz -> does nothing if A = 0. Sets instruction pointer to literal operand value
# # 4: bxc -> bitwise XOR of B and C. Save to B
# # 5: out -> combo operand % 8. Output value
# # 6: bdv -> like adv, but saved to B
# # 7: cdv -> like adv, but saved to C


def run_program(instruction: int, operand: int, register: Register, pointer: int) -> tuple[int, Optional[int]]:
  new_pointer: Optional[int] = None
  output = None
  if instruction == 0:
    adv(operand, register)
  elif instruction == 1:
    bxl(operand, register)
  elif instruction == 2:
    bst(operand, register)
  elif instruction == 3:
    new_pointer = jnz(operand, register)
  elif instruction == 4:
    bxc(operand, register)
  elif instruction == 5:
    output = out(operand, register)
  elif instruction == 6:
    bdv(operand, register)
  elif instruction == 7:
    cdv(operand, register)

  if new_pointer is not None:
    pointer = new_pointer
  else:
    pointer += 2

  return pointer, output


def part_1(data: list[str]) -> str:
  register = Register(A=0, B=0, C=0)
  program: list[int] = list()
  instruction_pointer = 0
  program_output: list[int] = list()

  for row in data:
    if ':' not in row:
      continue
    row_type, value = row.split(': ')
    if 'Register' in row_type:
      x, register_type = row_type.split(' ')
      setattr(register, register_type, int(value))
    elif 'Program' in row_type:
      program = [int(x) for x in value.split(',')]

  while instruction_pointer < len(program):
    instruction = program[instruction_pointer]
    operand = program[instruction_pointer + 1]
    instruction_pointer, output = run_program(instruction, operand, register, instruction_pointer)
    if output is not None:
      program_output.append(output)

  return ",".join([str(x) for x in program_output])


def part_2(data: list[str]) -> int:
  a = 0
  b = 0
  c = 0
  program: list[int] = list()
  instruction_pointer = 0
  program_output: list[int] = list()

  for row in data:
    if ':' not in row:
      continue
    row_type, value = row.split(': ')
    if 'Register' in row_type:
      x, register_type = row_type.split(' ')
      if register_type == 'A': a = int(value)
      elif register_type == 'B': b = int(value)
      elif register_type == 'C': c = int(value)
    elif 'Program' in row_type:
      program = [int(x) for x in value.split(',')]

  counter = 0
  # while program_output != program:
  for i in range(500):
    program_output = list()
    instruction_pointer = 0
    register = Register(A=(8**8) + counter, B=b, C=c)
    while instruction_pointer < len(program):
      instruction = program[instruction_pointer]
      operand = program[instruction_pointer + 1]
      instruction_pointer, output = run_program(instruction, operand, register, instruction_pointer)
      if output is not None:
        program_output.append(output)
        if len(program_output) > len(program):
          break
        elif program_output[-1] != program[len(program_output) - 1]: 
          break
    print(program_output, register.A, hex((8**8) + counter), (8**8) + counter, counter)
    counter += 1
  return 0

# Program: 2,4,1,3,7,5,1,5,0,3,4,3,5,5,3,0

# 3 bit, 0-7
# 3 registers, A, B, C, any int
# 8 instructions, 3bit code: opcode
# # 0: adv -> division | Numerator: A register, denominator: <combo operand>^2 | Result: int(), saved to A
# # 1: bxl -> bitwise xor of B and literal operand. Save to B
# # 2: bst -> combo operand % 8. Save to B
# # 3: jnz -> does nothing if A = 0. Sets instruction pointer to literal operand value
# # 4: bxc -> bitwise XOR of B and C. Save to B
# # 5: out -> combo operand % 8. Output value
# # 6: bdv -> like adv, but saved to B
# # 7: cdv -> like adv, but saved to C
# 3 bit number after instruction: operand
# instruction pointer: identifies position in program from where next opcode (8 instructions, 3 bit code) will be read
# # starts at 0, increases by 2. If trying to read opcode past end: halt
#
# literal operand: value of operand itself
# combo operands:
# # Combo operands 0 through 3 represent literal values 0 through 3.
# # Combo operand 4 represents the value of register A.
# # Combo operand 5 represents the value of register B.
# # Combo operand 6 represents the value of register C.
# # Combo operand 7 is reserved and will not appear in valid programs.



if __name__ == '__main__':
  import time 

  data = read_data(17, production=True)
  start_time = time.perf_counter()
  answer_part_1 = part_1(data)
  end_time = time.perf_counter()
  print(f"Part 1 - {answer_part_1} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")

  start_time = time.perf_counter()
  answer_part_2 = part_2(data)
  end_time = time.perf_counter()
  print(f"Part 2 - {answer_part_2} (Execution Time: {(end_time - start_time) * 1000:.3f} ms)")