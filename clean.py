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