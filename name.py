def get_name_mode() -> tuple[str, str]:
    name = input('Name of resulting file: ')
    name = name.strip()
    if name.endswith(('.asm', '.s', '.bin')):
        return name, name.split('.')[-1]
    else:
        print('Invalid file extension, needed .asm/.s/.bin')
        return get_name_mode()

