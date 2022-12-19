from datetime import datetime
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

def add_robots(robot_counts, robot, count):
    tmp = list(robot_counts)
    tmp[robot] += count
    return tuple(tmp)

def add_resources(a, b, n):
    return (
        a[0] + b[0] * n, 
        a[1] + b[1] * n, 
        a[2] + b[2] * n, 
        a[3] + b[3] * n)

def has_resources(a, b):
    return a[0] >= b[0] and a[1] >= b[1] and a[2] >= b[2] and a[3] >= b[3]

def time_until_has_resources(cur_resources, req_resources, robot_counts):
    time = 0
    for cur_amount, req_amount, robots in zip(cur_resources, req_resources, robot_counts): 
        if cur_amount >= req_amount: continue
        if robots == 0: return None
        time = max(time, math.ceil((req_amount - cur_amount) / robots))
    return time

def get_max_geode(blueprint, robot_counts, resources, time_remaining, max_robots_to_build):
    # print(f'{time_remaining} Resources {resources}, robot counts {robot_counts}')

    max_geode = resources[3] + time_remaining * robot_counts[3]

    if max_robots_to_build[0] > 0: robots_to_build = range(1) # always build ore robots first
    else: robots_to_build = range(3, 0, -1) # try building robots in order: geode, obsidian, clay

    min_time_until_build = 100

    for robot in robots_to_build:
        if max_robots_to_build[robot] == 0: continue

        cost = get_robot_cost(blueprint, robot)
        time_until_build = time_until_has_resources(resources, cost, robot_counts)
        if time_until_build is None or time_remaining <= time_until_build: continue

        # never delay a better robot by building a clay robot (not sure if correct assumption in all cases, but works with given input)
        if robot == 1 and time_until_build >= min_time_until_build: continue
        min_time_until_build = min(min_time_until_build, time_until_build)

        time_until_ready = time_until_build + 1
        new_resources = add_resources(resources, robot_counts, time_until_ready)
        new_resources = add_resources(new_resources, cost, -1)
        new_robot_counts = add_robots(robot_counts, robot, 1)
        new_max_robots_to_build = add_robots(max_robots_to_build, robot, -1)

        # print(f'{time_remaining - time_until_build} Build robot {robot}, cost {cost}')

        max_geode = max(max_geode, 
            get_max_geode(blueprint, new_robot_counts, new_resources, time_remaining - time_until_ready, new_max_robots_to_build))

    return max_geode

start_time = datetime.now()

blueprints = parse_input()
# print(blueprints)

robot_counts = (1, 0, 0, 0) # ore, clay, obsidian, geode
resources = (0, 0, 0, 0)

product = 1
for i, blueprint in enumerate(blueprints):
    # it's never beneficial to build more robots of a given resource than the maximum cost
    max_ore_cost = max(blueprint[0], blueprint[1], blueprint[2], blueprint[4])
    max_clay_cost = blueprint[3]
    max_obsidian_cost = blueprint[5]

    max_geode = 0
    # we already have one ore robot so maximum to build is one less than the max cost
    for max_ore_robots in range(0, max_ore_cost): 
        geode = get_max_geode(blueprint, robot_counts, resources, 32, (max_ore_robots, max_clay_cost, max_obsidian_cost, 100))
        max_geode = max(max_geode, geode)

    print(f'{i}: {max_geode}')
    product *= max_geode
    # break

print(product)

end_time = datetime.now()
print(f'run time: {end_time - start_time}')
