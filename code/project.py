from csv_reader import read_csv
from file import get_file, clean_file
from typing import TextIO, BinaryIO
import sys


def main() -> None:
    output, mode = get_info()
    input = get_file(mode)
    if mode == 'asm':
        convert2asm(input, output)
    else:
        convert2bin(input, output)
    input.close()
    print('Process complete!')
    retry()


def get_info() -> tuple[str, str]:
    name = "../data/" + input('Name of resulting file: ')
    name = name.strip()
    if name.endswith(('.asm', '.s', '.bin')):
        return name, name.split('.')[-1]
    else:
        print('Invalid file extension, needed .asm/.s/.bin')
        return get_info()


def convert2asm(initial: TextIO|BinaryIO, final: str) -> None:
    with open(final, 'w') as final_file:
        while inst:= initial.read(32).decode('utf-8'): #type: ignore
            opcode = inst[:7][::-1]
            rd = inst[7:12][::-1]
            funct3 = inst[12:15][::-1]
            rs1 = inst[15:20][::-1]
            rs2 = inst[20:25][::-1]
            funct7 = inst[25:][::-1]

            immI = funct7 + rs2
            immS = funct7 + rd
            immB = (inst[8:12] + inst[25:31] + inst[7:8] + inst[31:32])[::-1] + '0'
            immU = inst[12:][::-1] + '000000000000'
            immJ = (inst[21:31] + inst[20:21] + inst[12:20] + inst[31:32])[::-1]

            immI = twos_str_to_int(immI, len(immI))
            immS = twos_str_to_int(immS, len(immS))
            immB = twos_str_to_int(immB, len(immB))
            immU = twos_str_to_int(immU, len(immU))
            immJ = twos_str_to_int(immJ, len(immJ))
            
            rd = f'x{int(rd, base = 2)}'
            rs1 = f'x{int(rs1, base = 2)}'
            rs2 = f'x{int(rs2, base = 2)}'

            instruction_dict_op, instruction_dict_full = read_csv('../data/insts.csv', 'asm')
            inst_type = instruction_dict_op[opcode]
            identifier = opcode + funct3 + funct7

            match inst_type:
                case 'R':
                    inst = instruction_dict_full[identifier]
                    instruction = inst + f' {rd}, {rs1}, {rs2}'
                case 'I':
                    if identifier in {'00100110010000000', '00100111010000000', '00100111010100000', '11100110000000000', '11100110000000001'}:
                        inst = instruction_dict_full[identifier]
                        if opcode == '1110011':
                            instruction = 'ebreak' if immI else 'ecall'
                        else:
                            instruction = inst + f' {rd}, {rs1}, {immI}'
                    else:
                        inst = instruction_dict_full[identifier[0:10]]
                        if inst[0] == 'l':
                            instruction = inst + f' {rs2}, {immI}({rs1})'
                        else:
                            instruction = inst + f' {rd}, {rs1}, {immI}'
                case 'S':
                    inst = instruction_dict_full[identifier[0:10]]
                    instruction = inst + f' {rs2}, {immS}({rs1})'
                case 'B':
                    inst = instruction_dict_full[identifier[0:10]]
                    instruction = inst + f' {rs1}, {rs2}, {immB}'
                case 'U':
                    inst = instruction_dict_full[opcode]
                    instruction = inst + f' {rd}, {immU}'
                case 'J':
                    inst = instruction_dict_full[opcode]
                    instruction = inst + f' {rd}, {immJ}'
            final_file.write(f"{instruction}\n")

    
def convert2bin(initial_file: TextIO|BinaryIO, final: str) -> None:
        instruction_dict = read_csv('insts.csv', 'bin')
        with open(final, 'wb') as final_file:
            instruction_list = clean_file(initial_file)
            for instruction in instruction_list:
                instruction = instruction.split(' ')
                inst = instruction[0]
                parameters = instruction_dict[inst] # type: ignore

                match parameters['type']:
                    case 'R':
                        rd = int(instruction[1][1:])
                        rs1 = int(instruction[2][1:])
                        rs2 = int(instruction[3][1:])
                        rd, rs1, rs2 = f"{rd:05b}", f"{rs1:05b}", f"{rs2:05b}"
                        instruction_f = parameters['funct7'] + rs2 + rs1 + parameters['funct3'] + rd + parameters['opcode']

                    case 'I':
                        if inst not in {'ebreak', 'ecall'}:
                            if inst[0] == 'l':
                                rd = int(instruction[1][1:])
                                rs1 = int(instruction[3][1:])
                                imm = get_int(instruction[2])
                            else:
                                rd = int(instruction[1][1:])
                                rs1 = int(instruction[2][1:])
                                imm = get_int(instruction[3])
                        elif inst == 'ecall':
                            rd, rs1, imm = 0, 0, 0
                        else:
                            rd, rs1, imm = 0, 0, 1
                        rd, rs1, imm = f"{rd:05b}", f"{rs1:05b}", int_to_twos_str(imm, 12)
                        instruction_f= imm + rs1 + parameters['funct3'] + rd + parameters['opcode']

                    case 'S':
                        rs2 = int(instruction[1][1:])
                        rs1 = int(instruction[3][1:])
                        imm = get_int(instruction[2])
                        rs2, rs1, imm = f"{rs2:05b}", f"{rs1:05b}", int_to_twos_str(imm, 12)
                        instruction_f = imm[:7]+ rs2 + rs1 + parameters['funct3'] + imm[7:] + parameters['opcode']

                    case 'B':
                        rs1 = int(instruction[1][1:])
                        rs2 = int(instruction[2][1:])
                        imm = get_int(instruction[3])
                        rs1, rs2, imm = f"{rs1:05b}", f"{rs2:05b}", int_to_twos_str(imm, 13)
                        instruction_f = imm[0] + imm[2:8] + rs2 + rs1 + parameters['funct3'] + imm[8:12] + imm[1] + parameters['opcode']

                    case 'U':
                        rd = int(instruction[1][1:])
                        imm = get_int(instruction[2])
                        rd, imm = f"{rd:05b}", int_to_twos_str(imm, 32)
                        instruction_f = imm[0:20] + rd + parameters['opcode']
    
                    case 'J':
                        rd = int(instruction[1][1:])
                        imm = get_int(instruction[2])
                        rd, imm = f"{rd:05b}", int_to_twos_str(imm, 21)
                        instruction_f = imm[0] + imm[11:21] + imm[10] + imm[1:9] + rd + parameters['opcode']
                
                final_file.write(bytes(instruction_f[::-1], 'utf-8'))


def twos_str_to_int(val: str, bits: int) -> int:
    val_int = int(val, base = 2)
    if (val_int & (1 << (bits - 1))) != 0:
        val_int = val_int - (1 << bits)
    return val_int


def int_to_twos_str(val: int, bits: int) -> str:
    positive = val & (2**bits - 1)
    return f"{positive:0{bits}b}"


def get_int(num: str) -> int:
    if num.startswith('0x'):
        imm = int(num, base = 16)
    else:
        imm = int(num)
    return imm


def retry() -> None:
    ans = input('Convert another file?(y/n) ').lower().strip()
    if ans == 'y':
        main()
    elif ans == 'n':
        sys.exit()
    else:
        print('Invalid answer')
        retry()


if __name__ == '__main__':
    main()