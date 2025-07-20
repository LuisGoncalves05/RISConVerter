import csv


def read_csv(file, mode) -> tuple[dict, dict]|dict:
    if mode == 'bin':
        instruction_dict = {}
        with open(file) as instruction_data:
            instruction_data = csv.DictReader(instruction_data)
            for line in instruction_data:
                inst = line['inst']
                parameters = {
                    'type': line['type'],
                    'opcode': line['opcode'],
                    'funct3': line['funct3'],
                    'funct7': line['funct7']
                }
                instruction_dict[inst] = parameters
        return instruction_dict
    else:
        instruction_dict_op = {}
        instruction_dict_full = {}
        with open(file) as instruction_data:
            instruction_data = csv.DictReader(instruction_data)
            for line in instruction_data:
                if line['funct3'] != 'None' and line['funct7'] != 'None':
                    identifier = line['opcode'] + line['funct3'] + line['funct7']
                elif line['funct3'] != 'None':
                    identifier = line['opcode'] + line['funct3']
                else:
                    identifier = line['opcode']
                instruction_dict_op[line['opcode']] = line['type']
                instruction_dict_full[identifier] = line['inst']
    return instruction_dict_op, instruction_dict_full
