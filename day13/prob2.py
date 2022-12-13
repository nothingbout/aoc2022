import functools
import itertools

input_file = 'input.txt'

class Value:
    def __init__(self, list = None, num = None):
        self.list = list
        self.num = num

    def is_list(self):
        return self.list is not None

    def is_num(self):
        return self.num is not None

    def __str__(self):
        return str(self.num) if self.is_num() else str(self.list)
    __repr__ = __str__


def parse_char(buf, idx, char):
    if buf[idx] != char: raise f'Unexpected character: {buf[idx]}'
    return idx + 1

def parse_num(buf, idx):
    num_str = ''
    while buf[idx].isnumeric():
        num_str += buf[idx]
        idx += 1
    return idx, Value(num = int(num_str))

def parse_list(buf, idx):
    idx = parse_char(buf, idx, '[')
    values = []
    while (buf[idx] != ']'):
        idx, value = parse_value(buf, idx)
        values.append(value)
        if buf[idx] == ',': idx += 1

    idx = parse_char(buf, idx, ']')
    return idx, Value(list = values)

def parse_value(buf, idx = 0):
    # print(f'{buf[idx:]}')
    if buf[idx] == '[': return parse_list(buf, idx)
    else: return parse_num(buf, idx)

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]
    packets = []
    for line in lines:
        if len(line) == 0: continue
        packets.append(parse_value(line)[1])
    return packets

def compare_lists(a, b):
    for i in range(min(len(a), len(b))):
        r = compare_values(a[i], b[i])
        if r != 0: return r
    if len(a) < len(b): return -1
    if len(a) > len(b): return 1
    return 0

def compare_values(a, b):
    if a.is_num() and b.is_num():
        if a.num < b.num: return -1
        if a.num > b.num: return 1
        return 0
    elif a.is_list() and b.is_list():
        return compare_lists(a.list, b.list)
    elif a.is_list() and b.is_num():
        return compare_lists(a.list, [b])
    elif a.is_num() and b.is_list():
        return compare_lists([a], b.list)
    else:
        raise "wut"

divider_packets = [
    parse_value('[[2]]')[1], 
    parse_value('[[6]]')[1]
]

packets = parse_input()
packets.extend(divider_packets)

packets = sorted(packets, key=functools.cmp_to_key(compare_values))
# print(packets)

divider_indices = []
for i, packet in enumerate(packets):
    if compare_values(packet, divider_packets[len(divider_indices)]) == 0:
        divider_indices.append(i)
        if len(divider_indices) == len(divider_packets): break

print(functools.reduce(lambda x, y: (x + 1) * (y + 1), divider_indices))