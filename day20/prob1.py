from datetime import datetime
import functools
import itertools
import math

input_file = 'input.txt'

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    nums = []
    for line in lines:
        nums.append(int(line))
    return nums

def wrap_index(idx, size):
    return idx % size

def swap(arr, i, j):
    tmp = arr[i]
    arr[i] = arr[j]
    arr[j] = tmp

orig_nums = parse_input()
print(f'count: {len(orig_nums)}, unique: {len(set(orig_nums))}')
print(orig_nums)

nums_count = len(orig_nums)
orig_num_indices = []
nums_with_indices = []
for i, num in enumerate(orig_nums): 
    orig_num_indices.append(i)
    nums_with_indices.append((i, num))

for i in range(len(orig_num_indices)):
    idx = orig_num_indices[i]
    _, num = nums_with_indices[idx]
    offset = num
    dir = 1 if offset > 0 else -1
    for _ in range(abs(offset)):
        next_idx = wrap_index(idx + dir, nums_count)

        orig_num_indices[nums_with_indices[idx][0]] = next_idx
        orig_num_indices[nums_with_indices[next_idx][0]] = idx
        swap(nums_with_indices, idx, next_idx)

        idx = next_idx

    # print(list(map(lambda x: x[1], nums_with_indices)))

zero_idx = orig_num_indices[orig_nums.index(0)]
sum = 0
for offset in [0, 1000, 2000, 3000]:
    idx = wrap_index(zero_idx + offset, nums_count)
    num = nums_with_indices[idx][1]
    print(f'{idx} {num}')
    sum += num

print(sum)
