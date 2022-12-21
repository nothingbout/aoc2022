from datetime import datetime
import functools
import itertools
import time
import math

input_file = 'input.txt'

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    jobs = {}
    for line in lines:
        parts = line.split()
        name = parts[0][:-1]
        if len(parts) == 2:
            jobs[name] = int(parts[1])
        else:
            jobs[name] = (parts[1], parts[2], parts[3])
    return jobs

def is_const_params(params):
    return not isinstance(params, tuple)

def get_const_value(params):
    return params if is_const_params(params) else None

def get_dependencies(params):
    return [params[0], params[2]] if not is_const_params(params) else []

def get_dependencies_recursive(jobs, job_name):
    all_deps = set(get_dependencies(jobs[job_name]))
    unresolved = list(all_deps)
    while len(unresolved) > 0:
        new_unresolved = []
        for name in unresolved:
            deps = get_dependencies(jobs[name])
            all_deps.update(deps)
            new_unresolved.extend(deps)
        unresolved = new_unresolved
    return all_deps

def get_dependency_chains(jobs, start_name, end_name):
    if start_name == end_name: return [[end_name]]
    chains = []
    for dep in get_dependencies(jobs[start_name]):
        chains.extend(map(lambda x: [start_name] + x, get_dependency_chains(jobs, dep, end_name)))
    return chains

def eval_op(op, a, b):
    match op:
        case '+': return a + b
        case '-': return a - b
        case '*': return a * b
        case '/': 
            if a % b != 0: raise Exception('invalid division')
            return a // b
    raise Exception('unknown op')

def eval_jobs(jobs, sorted_job_names):
    values = {}
    for name in sorted_job_names:
        params = jobs[name]
        if is_const_params(params):
            values[name] = get_const_value(params)
        else:
            values[name] = eval_op(params[1], values[params[0]], values[params[2]])    
    return values

def get_chain_input_for_expected_output(jobs, values, chain_names, expected_output):
    if len(chain_names) == 1: return expected_output
    params = jobs[chain_names[0]]

    if chain_names[1] == params[0]:
        p2_value = values[params[2]]
        match params[1]:
            case '+': prev_output = expected_output - p2_value
            case '-': prev_output = expected_output + p2_value
            case '*': prev_output = expected_output / p2_value
            case '/': prev_output = expected_output * p2_value
    elif chain_names[1] == params[2]:
        p0_value = values[params[0]]
        match params[1]:
            case '+': prev_output = expected_output - p0_value
            case '-': prev_output = p0_value - expected_output
            case '*': prev_output = expected_output / p0_value
            case '/': prev_output = p0_value / expected_output
    else:
        raise Exception(f'invalid chain')

    return get_chain_input_for_expected_output(jobs, values, chain_names[1:], prev_output)

jobs = parse_input()
# print(jobs)

sorted_job_names_set = set()
sorted_job_names = []
remaining_job_names = jobs.keys()

while len(remaining_job_names) > 0:
    new_remaining_job_names = []
    for name in remaining_job_names:
        params = jobs[name]
        deps_fulfilled = False
        if is_const_params(params):
            deps_fulfilled = True
        else:
            deps = get_dependencies(params)
            if set(deps).issubset(sorted_job_names_set):
                deps_fulfilled = True

        if deps_fulfilled:
            sorted_job_names.append(name)
            sorted_job_names_set.add(name)
        else:
            new_remaining_job_names.append(name)

    remaining_job_names = new_remaining_job_names

# print(sorted_job_names)

values = eval_jobs(jobs, sorted_job_names)

# print(values[jobs['root'][0]], values[jobs['root'][2]])

root_input1_name = jobs['root'][0]
root_input2_name = jobs['root'][2]

deps1 = get_dependencies_recursive(jobs, root_input1_name)
deps2 = get_dependencies_recursive(jobs, root_input2_name)
if 'humn' in deps1: print('input 1 has human')
if 'humn' in deps2: print('input 2 has human')

deps_chains = get_dependency_chains(jobs, root_input1_name, 'humn')
print(f'dependency chains with human: {deps_chains}')

deps_chain = deps_chains[0]
humn_value = get_chain_input_for_expected_output(jobs, values, deps_chain, values[root_input2_name])
print(f'human input: {humn_value}')

jobs['humn'] = humn_value
values = eval_jobs(jobs, sorted_job_names)
print(f'got: {values[root_input1_name]}, expected: {values[root_input2_name]}')
