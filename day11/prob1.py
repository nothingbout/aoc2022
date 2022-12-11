input_file = 'input.txt'

class Monkey:
    def __init__(self):
        self.items = []
        self.op = None
        self.test_divider = None
        self.true_dst = None
        self.false_dst = None
        self.inspections = 0

    def __str__(self):
        return f'Monkey({self.items}, {self.op}, {self.test_divider}, {self.true_dst}, {self.false_dst})'
    __repr__ = __str__

def parse_param(str):
    return -1 if str == 'old' else int(str)

def parse_op(str):
    return 1 if str == '+' else 2

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

        monkeys = []
        for i in range(0, len(lines), 7):
            monkey = Monkey()
            monkey.items = [int(x) for x in lines[i + 1][len('  Starting items: '):].split(',')]
            op_parts = lines[i + 2][len('  Operation: new = '):].split()
            monkey.op = (parse_param(op_parts[0]), parse_op(op_parts[1]), parse_param(op_parts[2]))
            monkey.test_divider = int(lines[i + 3][len('  Test: divisible by '):])
            monkey.true_dst = int(lines[i + 4][len('    If true: throw to monkey '):])
            monkey.false_dst = int(lines[i + 5][len('    If false: throw to monkey '):])

            monkeys.append(monkey)

        return monkeys

def apply_op(op, value):
    a, o, b = op
    if a < 0: a = value
    if b < 0: b = value
    return a + b if o == 1 else a * b

monkeys = parse_input()
# print(monkeys)

for _ in range(20):
    for monkey in monkeys:
        items = reversed(monkey.items)
        monkey.inspections += len(monkey.items)
        monkey.items = []

        for value in items:
            value = apply_op(monkey.op, value)
            value //= 3
            if value % monkey.test_divider == 0:
                monkeys[monkey.true_dst].items.append(value)
            else:
                monkeys[monkey.false_dst].items.append(value)

inspections = []
for monkey in monkeys:
    # print(monkey.inspections)
    inspections.append(monkey.inspections)

inspections = sorted(inspections)

print(inspections[-1] * inspections[-2])