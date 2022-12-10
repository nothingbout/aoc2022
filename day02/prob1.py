import fileinput

def calc_result_points(their_choice, our_choice): 
    if their_choice == 'A': # rock
        if our_choice == 'X': return 3 # rock
        if our_choice == 'Y': return 6 # paper
        if our_choice == 'Z': return 0 # scissors
    if their_choice == 'B': # paper
        if our_choice == 'X': return 0 # rock
        if our_choice == 'Y': return 3 # paper
        if our_choice == 'Z': return 6 # scissors
    if their_choice == 'C': # scissors
        if our_choice == 'X': return 6 # rock
        if our_choice == 'Y': return 0 # paper
        if our_choice == 'Z': return 3 # scissors

def calc_choice_points(our_choice):
    if our_choice == 'X': return 1
    if our_choice == 'Y': return 2
    if our_choice == 'Z': return 3

total_points = 0

for line in fileinput.input():
    choices = line.strip().split(' ')
    result_points = calc_result_points(choices[0], choices[1])
    choice_points = calc_choice_points(choices[1])
    total_points += result_points + choice_points
    
print(total_points)