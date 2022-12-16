from datetime import datetime
import itertools
import heapq

class Node:
    def __init__(self):
        self.name = None
        self.destinations = []
        self.flow_rate = 0

    def __str__(self):
        return f'Node({self.name}, {self.destinations}, {self.flow_rate})'
    __repr__ = __str__

input_file = 'input.txt'

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    nodes = {}
    for line in lines:
        node = Node()
        parts = line.split('; ')
        node.name = parts[0][len('Valve '):len('Valve ') + 2]
        node.flow_rate = int(parts[0][len('Valve AA has flow rate='):])
        node.destinations = list(map(lambda x: x.strip(), parts[1][len('tunnels lead to valves'):].split(', ')))
        nodes[node.name] = node
    return nodes

def find_min_distances_from(nodes, start_node_name):
    search_queue = [start_node_name]
    min_distances = { start_node_name: 0 }
    while len(search_queue) > 0:
        node = nodes[search_queue.pop(0)]
        for dst_name in node.destinations:
            if dst_name in min_distances: continue
            min_distances[dst_name] = min_distances[node.name] + 1
            search_queue.append(dst_name)
    return min_distances

def find_max_released(time_limit, nodes, min_distances, unopened_valve_names, valve_name, flow_rate, total_released, time_spent):
    max_released = 0
    for dst_name in list(unopened_valve_names): # copy set to list to avoid mutating while iterating
        distance = min_distances[valve_name][dst_name]

        new_time_spent = time_spent + distance + 1
        if new_time_spent >= time_limit: continue

        new_total_released = total_released + flow_rate * (new_time_spent - time_spent)
        new_flow_rate = flow_rate + nodes[dst_name].flow_rate

        unopened_valve_names.remove(dst_name)
        max_released = max(max_released, 
            find_max_released(time_limit, nodes, min_distances, unopened_valve_names, dst_name, new_flow_rate, new_total_released, new_time_spent))
        unopened_valve_names.add(dst_name)

    return max(max_released, total_released + flow_rate * (time_limit - time_spent))

nodes = parse_input()
# print(nodes)

valve_names = []
for node in nodes.values():
    if node.flow_rate > 0: valve_names.append(node.name)

min_distances_between_valves = {}
for valve_name in valve_names + ['AA']:
    all_min_distances = find_min_distances_from(nodes, valve_name)
    min_distances_to_valves = {}
    for dst_name, distance in all_min_distances.items():
        if nodes[dst_name].flow_rate > 0: min_distances_to_valves[dst_name] = distance
    min_distances_between_valves[valve_name] = min_distances_to_valves
    # print(f'{valve_name}: {min_distances_to_valves}')


# part 1 solution
# max_released = find_max_released(30, nodes, min_distances_between_valves, set(valve_names), 'AA', 0, 0, 0)
# print(max_released)

max_released = 0
all_valves = set(valve_names)
iteration = 0

for n in range(1, len(all_valves) // 2 + 1):
    for valves_for_human in itertools.combinations(all_valves, n):        
        valves_for_human = set(valves_for_human)
        valves_for_elephant = all_valves.difference(valves_for_human)

        # print(f'{valves_for_human} - {valves_for_elephant}')

        released = find_max_released(26, nodes, min_distances_between_valves, valves_for_human, 'AA', 0, 0, 0)
        released += find_max_released(26, nodes, min_distances_between_valves, valves_for_elephant, 'AA', 0, 0, 0)
        max_released = max(max_released, released)

        iteration += 1
        if iteration % 100 == 0: print(f'{iteration}: {max_released}')

print(f'{iteration}: {max_released}')
