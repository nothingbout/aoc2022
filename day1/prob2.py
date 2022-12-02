import fileinput

current_elf_total = 0
top_totals = [0, 0, 0]

def insert_to_top_totals(amount):
    for i in range(0, len(top_totals)):
        if amount > top_totals[i]:
            top_totals.insert(i, amount)
            top_totals.pop() # remove last
            break

for line in fileinput.input():
    line = line.strip()
    if len(line) == 0: 
        insert_to_top_totals(current_elf_total)
        current_elf_total = 0
        continue

    amount = int(line)
    current_elf_total += amount

insert_to_top_totals(current_elf_total)

print(sum(top_totals))