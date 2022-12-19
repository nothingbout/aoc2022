from datetime import datetime
import functools
import itertools
import time
import math

input_file = 'input.txt'

def v_set(a, idx, value):
    if idx < 0 or idx >= len(a): raise Exception(f'index out of bounds: len(a) == {len(a)}, idx == {idx}')
    return a[0:idx] + (value,) + a[idx+1 : len(a)]
def v_check(a, b):
    if isinstance(b, tuple):
        if len(a) != len(b): raise Exception(f'length mismatch: len(a) == {len(a)}, len(b) == {len(b)}')
        return True
    return False
def v_add(a, b): return tuple(map(lambda x, y: x + y, a, b)) if v_check(a, b) else tuple(map(lambda x: x + b, a))
def v_sub(a, b): return tuple(map(lambda x, y: x - y, a, b)) if v_check(a, b) else tuple(map(lambda x: x - b, a))
def v_mul(a, b): return tuple(map(lambda x, y: x * y, a, b)) if v_check(a, b) else tuple(map(lambda x: x * b, a))
def v_div(a, b): return tuple(map(lambda x, y: x / y, a, b)) if v_check(a, b) else tuple(map(lambda x: x / b, a))
def v_floor(a): return tuple(map(math.floor, a))
def v_ceil(a): return tuple(map(math.ceil, a))
def v_min(a, b): return tuple(map(lambda x, y: min(x, y), a, b)) if v_check(a, b) else None
def v_max(a, b): return tuple(map(lambda x, y: max(x, y), a, b)) if v_check(a, b) else None

def parse_elements(input, whitelist):
    return [''.join(g) for _, g in filter(lambda g: g[0], itertools.groupby(input, key=lambda x: x in whitelist))]

def parse_nums(input):
    return [int(x) for x in parse_elements(input, '-0123456789')]

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    blueprints = []
    for line in lines[:3]:
        blueprints.append(tuple(parse_nums(line)[1:]))
    return blueprints

def get_robot_cost(blueprint, n):
    match n:
        case 0: return (blueprint[0], 0, 0, 0)
        case 1: return (blueprint[1], 0, 0, 0)
        case 2: return (blueprint[2], blueprint[3], 0, 0)
        case 3: return (blueprint[4], 0, blueprint[5], 0)
    raise "wtf"

def v_all_greater_or_equal(a, b):
    return functools.reduce(lambda x, y: x and y, map(lambda x, y: x >= y, a, b))

def get_next_states(robot_costs, max_costs, robot_counts, resources):
    new_states = []
    new_resources = v_add(resources, robot_counts)
    useful_to_wait = False
    for robot in range(4):
        if robot_counts[robot] >= max_costs[robot]: continue

        cost = robot_costs[robot]
        if v_all_greater_or_equal(resources, cost):
            new_states.append( (v_set(robot_counts, robot, robot_counts[robot] + 1), v_sub(new_resources, cost)) )
        else:
            for i in range(4):
                if resources[i] < cost[i] and robot_counts[i] > 0: 
                    useful_to_wait = True
                    break

    if useful_to_wait:
        new_states.append((robot_counts, new_resources))

    return new_states

def get_max_geode(blueprint, max_steps):
    robot_costs = [get_robot_cost(blueprint, n) for n in range(4)]
    max_costs = functools.reduce(lambda a, b: v_max(a, b), robot_costs)
    max_costs = v_max(max_costs, (0, 0, 0, 10000000))

    current_states = [((1, 0, 0, 0), (0, 0, 0, 0))]

    for step in range(max_steps):
        new_states = []
        for robot_counts, resources in current_states:
            new_states.extend(get_next_states(robot_costs, max_costs, robot_counts, resources))


        steps_remaining = max_steps - step - 1
        if steps_remaining > 0:
            max_needed_resources = v_mul(max_costs, steps_remaining)
            max_needed_resources = v_sub(max_needed_resources, v_mul(robot_counts, steps_remaining - 1))
            for i in range(len(new_states)):
                robot_counts, resources = new_states[i]
                new_states[i] = (robot_counts, v_min(resources, max_needed_resources))
        
        new_states = list(set(new_states)) # remove duplicates

        filtered_new_states = []
        for i in range(len(new_states)):
            strictly_worse = False
            for j in range(len(new_states)):
                if i == j: continue
                robot_counts, resources = new_states[i]
                other_robot_counts, other_resources = new_states[j]
                if v_all_greater_or_equal(other_robot_counts, robot_counts) and v_all_greater_or_equal(other_resources, resources):
                    strictly_worse = True
                    break

            if not strictly_worse:
                filtered_new_states.append(new_states[i])

        current_states = filtered_new_states
        # print(f'{step}: {len(current_states)}')

    max_geode = 0
    for _, resources in current_states:
        max_geode = max(max_geode, resources[3])
    return max_geode

start_time = datetime.now()

blueprints = parse_input()
# print(blueprints)

product = 1
for i, blueprint in enumerate(blueprints):
    max_geode = get_max_geode(blueprint, 32)

    print(f'{i}: {max_geode}')
    product *= max_geode
    # break

print(product)

end_time = datetime.now()
print(f'run time: {end_time - start_time}')
