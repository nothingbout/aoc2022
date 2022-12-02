import fileinput

def calc_wanted_points(outcome):
    if outcome == 'X': return 0
    if outcome == 'Y': return 3
    if outcome == 'Z': return 6

def calc_result_points(their_choice, our_choice): 
    if their_choice == 'A': # rock
        if our_choice == 'A': return 3 # rock
        if our_choice == 'B': return 6 # paper
        if our_choice == 'C': return 0 # scissors
    if their_choice == 'B': # paper
        if our_choice == 'A': return 0 # rock
        if our_choice == 'B': return 3 # paper
        if our_choice == 'C': return 6 # scissors
    if their_choice == 'C': # scissors
        if our_choice == 'A': return 6 # rock
        if our_choice == 'B': return 0 # paper
        if our_choice == 'C': return 3 # scissors

def calc_choice_points(our_choice):
    if our_choice == 'A': return 1
    if our_choice == 'B': return 2
    if our_choice == 'C': return 3

total_points = 0

for line in fileinput.input():
    inputs = line.strip().split(' ')

    their_choice = inputs[0]
    wanted_points = calc_wanted_points(inputs[1])

    our_choice = next(filter(lambda choice: calc_result_points(their_choice, choice) == wanted_points, ['A', 'B', 'C']))
    
    result_points = calc_result_points(their_choice, our_choice)
    choice_points = calc_choice_points(our_choice)
    total_points += result_points + choice_points
    
print(total_points)