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
            jobs[name] = (int(parts[1]),)
        else:
            jobs[name] = (parts[1], parts[2], parts[3])
    print(len(lines))
    print(len(jobs))
    return jobs

def is_const_params(params):
    return len(params) == 1

def get_const_value(params):
    return params[0] if is_const_params(params) else None

def get_dependencies(params):
    return [params[0], params[2]]

def eval_op(op, a, b):
    match op:
        case '+': return a + b
        case '-': return a - b
        case '*': return a * b
        case '/': return a / b
    raise Exception("wut")

jobs = parse_input()
print(jobs)

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

values = {}
for name in sorted_job_names:
    params = jobs[name]
    if is_const_params(params):
        values[name] = get_const_value(params)
    else:
        values[name] = eval_op(params[1], values[params[0]], values[params[2]])

print(values['root'])
