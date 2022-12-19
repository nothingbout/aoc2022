from datetime import datetime
import itertools

input_file = 'input.txt'

def parse_elements(input, whitelist):
    return [''.join(g) for _, g in filter(lambda g: g[0], itertools.groupby(input, key=lambda x: x in whitelist))]

def parse_nums(input):
    return [int(x) for x in parse_elements(input, '-0123456789')]

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    blueprints = []
    for line in lines:
        blueprints.append(tuple(parse_nums(line)[1:]))
    return blueprints

def get_robot_cost(blueprint, n):
    match n:
        case 0: return (blueprint[0], 0, 0, 0)
        case 1: return (blueprint[1], 0, 0, 0)
        case 2: return (blueprint[2], blueprint[3], 0, 0)
        case 3: return (blueprint[4], 0, blueprint[5], 0)
    raise "wtf"

def add_robot(robot_counts, n):
    tmp = list(robot_counts)
    tmp[n] += 1
    return tuple(tmp)

def add_resources(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2], a[3] + b[3])

def remove_resources(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2], a[3] - b[3])

def has_resources(a, b):
    return a[0] >= b[0] and a[1] >= b[1] and a[2] >= b[2] and a[3] >= b[3]

def get_max_geode(blueprint, robot_counts, resources, time_remaining, seen_states):
    if time_remaining == 0:
        # exit(0)
        return resources[3]

    state_key = (time_remaining, robot_counts, resources)
    if state_key in seen_states: return seen_states[state_key]

    # print(f'{time_remaining} {robot_counts} {resources}')

    new_resources = add_resources(resources, robot_counts)
    max_geode = 0

    max_ore_cost = max(blueprint[0], blueprint[1], blueprint[2], blueprint[4])
    max_clay_cost = blueprint[3] / 2 + 1

    for n in range(3, -1, -1):
        if n == 0 and robot_counts[n] >= max_ore_cost: continue
        elif n == 1 and robot_counts[n] >= max_clay_cost: continue

        cost = get_robot_cost(blueprint, n)
        if not has_resources(resources, cost): continue

        # print(f'Build robot: {n}, cost: {cost}')

        max_geode = max(max_geode, 
            get_max_geode(blueprint, add_robot(robot_counts, n), remove_resources(new_resources, cost), time_remaining - 1, seen_states))

    max_geode = max(max_geode, get_max_geode(blueprint, robot_counts, new_resources, time_remaining - 1, seen_states))

    seen_states[state_key] = max_geode
    return max_geode


blueprints = parse_input()
# print(blueprints)

robot_counts = (1, 0, 0, 0) # ore, clay, obsidian, geode
resources = (0, 0, 0, 0)

total_quality = 0
for i, blueprint in enumerate(blueprints):
    geode = get_max_geode(blueprint, robot_counts, resources, 24, {})
    print(f'{i}: {geode}')
    total_quality += (i + 1) * geode
    # break

print(total_quality)