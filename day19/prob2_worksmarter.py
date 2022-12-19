from datetime import datetime
import functools
import itertools
import time
import math

input_file = 'input.txt'

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

def mk_tuple(i, n):
    match i:
        case 0: return (n, 0, 0, 0)
        case 1: return (0, n, 0, 0)
        case 2: return (0, 0, n, 0)
        case 3: return (0, 0, 0, n)

def add_all(a, b):
    return (
        a[0] + b[0], 
        a[1] + b[1], 
        a[2] + b[2], 
        a[3] + b[3])

def sub_all(a, b):
    return (
        a[0] - b[0], 
        a[1] - b[1], 
        a[2] - b[2], 
        a[3] - b[3])

def mul_all(a, n):
    return (
        a[0] * n, 
        a[1] * n, 
        a[2] * n, 
        a[3] * n)

def min_all(a, b):
    return (
        min(a[0], b[0]), 
        min(a[1], b[1]), 
        min(a[2], b[2]), 
        min(a[3], b[3]))

def max_all(a, b):
    return (
        max(a[0], b[0]), 
        max(a[1], b[1]), 
        max(a[2], b[2]), 
        max(a[3], b[3]))

def all_greater_or_equal(a, b):
    return a[0] >= b[0] and a[1] >= b[1] and a[2] >= b[2] and a[3] >= b[3]

def get_next_states(robot_costs, max_costs, robot_counts, resources):
    new_states = []
    new_resources = add_all(resources, robot_counts)
    useful_to_wait = False
    for robot in range(4):
        if robot_counts[robot] >= max_costs[robot]: continue

        cost = robot_costs[robot]
        if all_greater_or_equal(resources, cost):
            new_states.append( (add_all(robot_counts, mk_tuple(robot, 1)), sub_all(new_resources, cost)) )
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
    max_costs = functools.reduce(lambda a, b: max_all(a, b), robot_costs)
    max_costs = max_all(max_costs, (0, 0, 0, 10000000))

    current_states = [((1, 0, 0, 0), (0, 0, 0, 0))]

    for step in range(max_steps):
        new_states = []
        for robot_counts, resources in current_states:
            new_states.extend(get_next_states(robot_costs, max_costs, robot_counts, resources))


        steps_remaining = max_steps - step - 1
        if steps_remaining > 0:
            max_needed_resources = mul_all(max_costs, steps_remaining)
            max_needed_resources = sub_all(max_needed_resources, mul_all(robot_counts, steps_remaining - 1))
            for i in range(len(new_states)):
                robot_counts, resources = new_states[i]
                new_states[i] = (robot_counts, min_all(resources, max_needed_resources))
        
        new_states = list(set(new_states)) # remove duplicates

        filtered_new_states = []
        for i in range(len(new_states)):
            strictly_worse = False
            for j in range(len(new_states)):
                if i == j: continue
                robot_counts, resources = new_states[i]
                other_robot_counts, other_resources = new_states[j]
                if all_greater_or_equal(other_robot_counts, robot_counts) and all_greater_or_equal(other_resources, resources):
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
