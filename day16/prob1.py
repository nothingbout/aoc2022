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

def find_min_distances_from(nodes, start_node):
    search_queue = [start_node]
    all_min_distances = { start_node.name: 0 }
    while len(search_queue) > 0:
        node = search_queue.pop(0)
        for dst_name in node.destinations:
            if dst_name in all_min_distances: continue
            all_min_distances[dst_name] = all_min_distances[node.name] + 1
            search_queue.append(nodes[dst_name])
    
    min_distances = {}
    for key, value in all_min_distances.items():
        if key != start_node.name and nodes[key].flow_rate > 0: 
            min_distances[key] = value
    return min_distances

def find_max_released(nodes, min_distances, visited, start_node_name, flow_rate, total_released, time_spent):
    visited.add(start_node_name)
    
    max_released = 0

    all_visited = True
    for dst_name, distance in min_distances[start_node_name].items():
        if dst_name in visited: continue

        new_time_spent = min(time_spent + distance + 1, 30)
        new_total_released = total_released + flow_rate * (new_time_spent - time_spent)

        if new_time_spent == 30: 
            max_released = max(max_released, new_total_released)
            # print(f'foo {max_released}')
            continue

        all_visited = False

        new_flow_rate = flow_rate + nodes[dst_name].flow_rate

        # print(f'{dst_name}, {new_total_released}, {new_time_spent}')
        released = find_max_released(nodes, min_distances, visited, dst_name, new_flow_rate, new_total_released, new_time_spent)
        max_released = max(max_released, released)

    if all_visited:
        max_released = total_released + flow_rate * (30 - time_spent)
        # print(f'bar {max_released}')
        
    visited.remove(start_node_name)
    return max_released

nodes = parse_input()
print(nodes)

min_distances = {}
for node in nodes.values():
    if node.flow_rate > 0 or node.name == 'AA':
        min_distances[node.name] = find_min_distances_from(nodes, node)

for key, value in min_distances.items():
    print(f'{key}: {min_distances[key]}')

max_released = find_max_released(nodes, min_distances, set(), 'AA', 0, 0, 0)
print(max_released)

