from typing import TextIO, BinaryIO


def get_file(mode) -> TextIO|BinaryIO:
    file_name: str = input('File to convert: ')
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