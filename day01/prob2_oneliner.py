import fileinput
import itertools

print(sum(sorted(
    map(lambda group: sum(map(lambda s: int(s), group[1])),     # group[1] == the list of values in the group
        filter(lambda group: group[0],                          # group[0] == the key of the group (True for non-empty lines)
            itertools.groupby(fileinput.input(), lambda line: len(line.strip()) > 0)
        )
    )
)[-3:]))