#! /usr/bin/env python3

import sys

def check_file(name):
    if_c = 0
    for_c = 0
    flag = False
    with open(name, 'r') as f:
        for line in f:
            line = line.lstrip()
            if line.startswith('FOR '):
                for_c += 1
            elif line.startswith('IF '):
                if_c += 1
            elif line.rstrip() == 'ENDIF':
                if_c -= 1
                flag = verify(if_c, 'ENDIF', lambda x: x < 0)
            elif line.rstrip() == 'NEXT':
                for_c -= 1
                flag = verify(for_c, 'NEXT', lambda x: x < 0)
    flag = verify(if_c, 'ENDIF', lambda x: x > 0)
    flag = verify(for_c, 'NEXT', lambda x: x > 0)
    return flag


def verify(count, label, func):
    if func(count):
        print('Missing {0}.'.format(label), file=sys.stderr)
        return True
    return False


def spacing(indent):
    return (2 * indent) * ' '

def indent(name, output):
    indent = 0
    with open(name, 'r') as i, open(output, 'w+') as o:
        for line in i:
            line = line.strip()
            if line.startswith('FOR ') or line.startswith('IF '):
                o.write(spacing(indent) + line + '\n')
                indent += 1
            elif line == 'NEXT' or line == 'ENDIF':
                indent -= 1
                o.write(spacing(indent) + line + '\n')
            else:
                o.write(spacing(indent) + line + '\n')


name = sys.argv[1]
if check_file(name):
    exit(1)
else:
    output = 'indented_' + name
    indent(name, output)
