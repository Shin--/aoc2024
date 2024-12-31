from dataclasses import dataclass
from sitecustomize import new_prefix
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
    register.A = int(register.A / (2 ** get_combo_operand(operand, register)))


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
    register.B = int(register.A / (2 ** get_combo_operand(operand, register)))


def cdv(operand: int, register: Register):
    register.C = int(register.A / (2 ** get_combo_operand(operand, register)))


# # 0: adv -> division | Numerator: A register, denominator: <combo operand>^2 | Result: int(), saved to A
# # 1: bxl -> bitwise xor of B and literal operand. Save to B
# # 2: bst -> combo operand % 8. Save to B
# # 3: jnz -> does nothing if A = 0. Sets instruction pointer to literal operand value
# # 4: bxc -> bitwise XOR of B and C. Save to B
# # 5: out -> combo operand % 8. Output value
# # 6: bdv -> like adv, but saved to B
# # 7: cdv -> like adv, but saved to C


def run_instruction(instruction: int, operand: int, register: Register) -> tuple[Optional[int], Optional[int]]:
    new_pointer: Optional[int] = None
    output = None

    match instruction:
        case 0:
            adv(operand, register)
        case 1:
            bxl(operand, register)
        case 2:
            bst(operand, register)
        case 3:
            new_pointer = jnz(operand, register)
        case 4:
            bxc(operand, register)
        case 5:
            output = out(operand, register)
        case 6:
            bdv(operand, register)
        case 7:
            cdv(operand, register)

    return new_pointer, output


def run_program(program: list[int], register: Register) -> list[int]:
    instruction_pointer = 0
    program_output: list[int] = list()

    while instruction_pointer < len(program):
        instruction = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        new_pointer, output = run_instruction(instruction, operand, register)
        if new_pointer is not None:
            instruction_pointer = new_pointer
        else:
            instruction_pointer += 2
        if output is not None:
            program_output.append(output)

    return program_output




def reverse_program(program: list[int]) -> int:
    a = 0
    iter_start = 0
    reversed_program_pointer = 1
    while reversed_program_pointer <= len(program) and reversed_program_pointer >= 0:
        a <<= 3
        for j in range(iter_start, 8):
            if program[-reversed_program_pointer:] == run_program(program, Register(A=a + j, B=0, C=0)):
                a += j
                reversed_program_pointer += 1
                iter_start = 0
                break
        else:
            reversed_program_pointer -= 1
            a >>= 3
            iter_start = a % 8 + 1
            a >>= 3

    return a

    # a = 0
    # incremental_power = 1
    # program_part = program[:incremental_power]
    # while program_part != program:
    #     output = run_program(program, Register(A=a, B=0, C=0))
    #     if output[:len(program_part)] == program_part:
    #         incremental_power += 1
    #         program_part = program[:(len(program_part) + 1)]
    #     if incremental_power < 0:
    #         break
    #     a += 8 ** incremental_power
    # return a

    # for i in reversed(range(0, len(program), 2)):
    #     a = a << 3
    #     program_part = program[i:]
    #
    #     while True:
    #         instruction_pointer = 0
    #         program_output: list[int] = list()
    #         register = Register(A=a, B=0, C=0)
    #
    #         while instruction_pointer < len(program):
    #             instruction = program[instruction_pointer]
    #             operand = program[instruction_pointer + 1]
    #             new_pointer, output = run_instruction(instruction, operand, register)
    #             if new_pointer is not None and register.A:
    #                 instruction_pointer = operand - 2
    #             if output is not None:
    #                 program_output.append(output)
    #             instruction_pointer += 2
    #         if program_output == program_part:
    #             break
    #         a += 1
    #     print(a)


def part_1(data: list[str]) -> str:
    register = Register(A=0, B=0, C=0)
    program: list[int] = list()

    for row in data:
        if ':' not in row:
            continue
        row_type, value = row.split(': ')
        if 'Register' in row_type:
            x, register_type = row_type.split(' ')
            setattr(register, register_type, int(value))
        elif 'Program' in row_type:
            program = [int(x) for x in value.split(',')]

    output = run_program(program, register)
    return ",".join([str(x) for x in output])


def part_2(data: list[str]) -> int:
    program: list[int] = list()

    for row in data:
        if ':' not in row:
            continue
        row_type, value = row.split(': ')
        if 'Program' in row_type:
            program = [int(x) for x in value.split(',')]

    return reverse_program(program)


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
