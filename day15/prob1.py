import itertools

input_file = 'input.txt'
test_line_y = 2000000

class Sensor:
    def __init__(self, sensor_pos, beacon_pos):
        self.sensor_pos = sensor_pos
        self.beacon_pos = beacon_pos
        self.beacon_distance = self.calc_beacon_distance()

    def __str__(self):
        return f'Sensor({self.sensor_pos}, {self.beacon_pos})'
    __repr__ = __str__

    def calc_beacon_distance(self):
        sx, sy = self.sensor_pos
        bx, by = self.beacon_pos
        return abs(sx - bx) + abs(sy - by)

    def range_on_line(self, line_y):
        sx, sy = self.sensor_pos
        line_distance = abs(line_y - sy)
        remaining_distance = self.beacon_distance - line_distance
        if remaining_distance < 0: return None

        range_min = sx - remaining_distance
        range_max = sx + remaining_distance

        bx, by = self.beacon_pos
        if by == line_y:
            if range_min == range_max: return None
            elif bx == range_min: range_min += 1
            elif bx == range_max: range_max -= 1

        return (range_min, range_max)

    def is_in_range(self, pos):
        pos_x, pos_y = pos
        sx, sy = self.sensor_pos
        line_distance = abs(pos_y - sy)
        remaining_distance = self.beacon_distance - line_distance
        return abs(sx - pos_x) <= remaining_distance

class Line:
    def __init__(self, pos_y):
        self.pos_y = pos_y
        self.ranges = []

    def reduce(self):
        self.ranges.sort()
        # print(self.ranges)

        new_ranges = []
        cur_min, cur_max = self.ranges.pop(0)
        while len(self.ranges) > 0:
            next_min, next_max = self.ranges.pop(0)
            if next_min > cur_max + 1:
                new_ranges.append((cur_min, cur_max))
                cur_min, cur_max = (next_min, next_max)
            else:
                # cur_min = next_min
                cur_max = max(cur_max, next_max)

        new_ranges.append((cur_min, cur_max))

        self.ranges = list(new_ranges)


def parse_pos(input):
    parts = input.split(', ')
    return (int(parts[0][2:]), int(parts[1][2:]))

def parse_input():
    with open(input_file, 'r') as file:
        lines = [line.rstrip('\r\n') for line in file.readlines()]

    sensors = []
    for line in lines:
        # Sensor at x=3844106, y=3888618: closest beacon is at x=3225436, y=4052707
        parts = line.split(': ')
        sensor_pos = parse_pos(parts[0][len('Sensor at '):])
        beacon_pos = parse_pos(parts[1][len('closest beacon is at '):])

        sensors.append(Sensor(sensor_pos, beacon_pos))
    return sensors

sensors = parse_input()
# print(sensors)

line = Line(test_line_y)

for sensor in sensors:
    range_on_line = sensor.range_on_line(line.pos_y)
    if range_on_line is not None:
        line.ranges.append(range_on_line)

# print(line.ranges)
line.reduce()
# print(line.ranges)

print(sum(map(lambda x: x[1] - x[0] + 1, line.ranges)))

# total = 0
# for x in range(-353600, 5933241):
#     pos = (x, test_line_y)

#     for sensor in sensors:
#         if sensor.is_in_range(pos) and pos != sensor.beacon_pos:
#             total += 1
#             break
# print(total)
