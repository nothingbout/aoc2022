from datetime import datetime
import functools
import itertools
import time
import math

IS_EXAMPLE = False
INPUT_FILE = 'example_input.txt' if IS_EXAMPLE else 'input.txt'

def parse_input():
    with open(INPUT_FILE, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]
    return lines

def snafu_digit_to_decimal(c):
    match c:
        case '=': return -2
        case '-': return -1
        case '0': return 0
        case '1': return 1
        case '2': return 2
    raise Exception(f'Unknown snafu digit: {c}')

def decimal_to_snafu_digit(d):
    match d:
        case -2: return '='
        case -1: return '-'
        case 0: return '0'
        case 1: return '1'
        case 2: return '2'
    raise Exception(f'Unknown decimal digit: {d}')

def snafu_to_decimal(snafu):
    decimal = 0
    base = 1
    for c in reversed(snafu):
        decimal += base * snafu_digit_to_decimal(c)
        base *= 5
    return decimal

def decimal_to_snafu(decimal):
    snafu = ''
    base = 1
    while abs(decimal) >= base * 5: base *= 5
    while base >= 1:
        digit = None
        min_rem = None
        for d in range(-2, 3):
            rem = abs(decimal - d * base)
            if min_rem is None or rem < min_rem:
                digit = d
                min_rem = rem
        # print(f'Remaining: {decimal}, base: {base}, digit: {digit}')
        decimal -= digit * base
        snafu += decimal_to_snafu_digit(digit)
        base //= 5
    return snafu

def decimal_to_snafu2(decimal):
    snafu_digits = []
    while decimal > 0:
        digit = decimal % 5
        if digit > 2: digit -= 5
        decimal -= digit
        decimal //= 5
        snafu_digits.append(decimal_to_snafu_digit(digit))
    return ''.join(reversed(snafu_digits))

start_time = datetime.now()

snafus = parse_input()
# print(snafus)

snafus_sum = sum([snafu_to_decimal(snafu) for snafu in snafus])
# print(snafus_sum)
print(decimal_to_snafu2(snafus_sum))

end_time = datetime.now()
print(f'run time: {end_time - start_time}')
