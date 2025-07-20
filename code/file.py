from typing import TextIO, BinaryIO


def get_file(mode) -> TextIO|BinaryIO:
    file_name: str = '../data/' + input('File to convert: ')
    if mode == "asm":
        if file_name.endswith('.bin'):
            try:
                file = open(file_name, 'rb')
            except FileNotFoundError:
                print('File not found.')
                return get_file(mode)
        else:
            print('Invalid file extension, needed .bin')
            return get_file(mode)

    else:
        if file_name.endswith(('.asm','.s')):
            try:
                file = open(file_name, 'r')
            except FileNotFoundError:
                print('File not found.')
                return get_file(mode)
        else:
            print('Invalid file extension, needed .asm/.s')
            return get_file(mode)
    
    return file

def clean_file(file) -> list[str]:
    lines = file.readlines()
    for i, line in enumerate(lines):
        for j in range(len(line)):
            if line[j] == '#':
                line = line[:j]
                break
        if '(' in line:
            line = line.replace('(', ',')
            line = line.replace(')', '')
        line = line.replace(',', ' ')
        idxs = []
        for k in range(1, len(line)):
            if line[k] == line[k-1] == ' ':
                idxs.append(k)
        line = ''.join([line[i] for i in range(len(line)) if i not in idxs])
        line = line.replace('?', '')
        line = line.strip()
        lines[i] = line
    lines = [line for line in lines if line]
    return lines