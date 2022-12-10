import fileinput

current_elf_total = 0
max_total = 0

for line in fileinput.input():
    line = line.strip()
    if len(line) == 0: 
        current_elf_total = 0
        continue

    amount = int(line)
    current_elf_total += amount
    if current_elf_total > max_total:
        max_total = current_elf_total

print(max_total)