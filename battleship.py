import random as r

def make_grid():
    grid = [[], [], [], [], [], [], [], [], [], []]
    for i in range(10):
        for j in range(10):
            grid[i].append('~')
    
    # Putting in the mothership
    row = r.randint(1, 8)
    col = r.randint(1, 8)
    # Center of monthership
    grid[row][col] = 'M'
    # Other mothership points
    grid[row - 1][col] = 'M'
    grid[row + 1][col] = 'M'
    grid[row][col - 1] = 'M'
    grid[row][col + 1] = 'M'

    # Putting in battleship
    valid = False
    while not valid:
        row = r.randint(0, 8)
        col = r.randint(0, 8)
        # Check if all points work (not alr taken)
        if grid[row][col] == '~' and grid[row][col + 1] == '~' and grid[row + 1][col] == '~' and grid[row + 1][col + 1] == '~':
            valid = True
    grid[row][col] = 'B'
    grid[row][col + 1] = 'B'
    grid[row + 1][col] = 'B'
    grid[row + 1][col + 1] = 'B'

    # Putting destroyer
    valid = False
    while not valid:
        row = r.randint(0, 8)
        col = r.randint(0, 8)
        if grid[row][col] == '~' and grid[row + 1][col] == '~' and grid[row + 1][col + 1] == '~':
            valid = True
    grid[row][col] = 'D'
    grid[row + 1][col] = 'D'
    grid[row + 1][col + 1] = 'D'

    # Putting stealth
    valid = False
    direction = r.choice(['vert', 'hori'])
    while not valid:
        if direction == 'hori':
            row = r.randint(0, 9)
            col = r.randint(0, 7)
            if grid[row][col] == '~' and grid[row][col + 1] == '~' and grid[row][col + 2] == '~':
                valid = True
        elif direction == 'vert':
            row = r.randint(0, 7)
            col = r.randint(0, 9)
            if grid[row][col] == '~' and grid[row + 1][col] == '~' and grid[row + 2][col] == '~':
                valid = True
    if direction == 'hori':
        grid[row][col], grid[row][col + 1], grid[row][col + 2] = 'S', 'S', 'S'
    else:
        grid[row][col], grid[row + 1][col], grid[row + 2][col] = 'S', 'S', 'S'

    # Putting patrol
    valid = False
    direction = r.choice(['vert', 'hori'])
    while not valid:
        if direction == 'hori':
            row = r.randint(0, 9)
            col = r.randint(0, 8)
            if grid[row][col] == '~' and grid[row][col + 1] == '~':
                valid = True
        else:
            row = r.randint(0, 8)
            col = r.randint(0, 9)
            if grid[row][col] == '~' and grid[row + 1][col] == '~':
                valid = True
    if direction == 'hori':
        grid[row][col], grid[row][col + 1] = 'P', 'P'
    else:
        grid[row][col], grid[row + 1][col] = 'P', 'P'

    return grid

def hall_fame():
    dict = {}
    i = 0

    with open("battleship_hof.txt") as fo:
        for line in fo:
            if i != 0:
                line = line.rstrip()
                vals = line.split(',')
                accuracy = float(float(vals[1]) / (float(vals[1]) + float(vals[2]))) * 100
                accur = format(accuracy, ',.2f')
                # Creating dictionary with ranks as keys and names/scores as values
                dict[int(i)] = {'name' : str(vals[0]), 'score' : accur}
            i += 1
    return dict

def the_game(grid):
    # Temp grid that will be shown to player
    temp_grid = [[], [], [], [], [], [], [], [], [], []]
    for i in range(10):
        for j in range(10):
            temp_grid[i].append('~')
    print_grid(temp_grid)
    hits = 0
    miss = 0
    mother = 0
    battle = 0
    destroy = 0
    stealth = 0
    patrol = 0
    row_conversion = {'A' : 0, 'a' : 0, 'B' : 1, 'b' : 1, 'C' : 2, 'c' : 2, 'D' : 3, 'd' : 3,
                      'E' : 4, 'e' : 4, 'F' : 5, 'f' : 5, 'G' : 6, 'g' : 6, 'H' : 7, 'h' : 7,
                      'I' : 8, 'i' : 8, 'J' : 9, 'j' : 9}

    while hits != 17:
        target = input("Where should we target next (q to quit)? ")
        if target == 'q' or target == 'Q':
            return 0, 0
        # Handles improper input below
        elif len(target) != 2:
            print("Please enter exactly two characters.")
        elif target[0] not in row_conversion.keys():
            print('Please enter a location in the form "G6".')
        # Handles all cases of an input (already chosen, hit, miss)
        else:
            if temp_grid[row_conversion.get(target[0])][int(target[1])] != '~':
                print("\nYou've already targeted that location")
                print_grid(temp_grid)
            elif grid[row_conversion.get(target[0])][int(target[1])] == '~':
                print('\nmiss')
                miss += 1
                temp_grid[row_conversion.get(target[0])][int(target[1])] = 'o'
                print_grid(temp_grid)
            elif grid[row_conversion.get(target[0])][int(target[1])] != '~':
                print("\nIT'S A HIT!")
                hits += 1
                temp_grid[row_conversion.get(target[0])][int(target[1])] = 'x'

                # Will find which ship has been hit
                # if all positions of that ship hit, will inform user
                if grid[row_conversion.get(target[0])][int(target[1])] == 'M':
                    mother += 1
                    if mother == 5:
                        print("The enemy's Mothership has been destroyed.")
                elif grid[row_conversion.get(target[0])][int(target[1])] == 'B':
                    battle += 1
                    if battle == 4:
                        print("The enemy's Battleship has been destroyed.")
                elif grid[row_conversion.get(target[0])][int(target[1])] == 'D':
                    destroy += 1
                    if destroy == 3:
                        print("The enemy's Destroyer has been destroyed.")
                elif grid[row_conversion.get(target[0])][int(target[1])] == 'S':
                    stealth += 1
                    if stealth == 3:
                        print("The enemy's Stealth Ship has been destroyed.")     
                elif grid[row_conversion.get(target[0])][int(target[1])] == 'P':
                    patrol += 1
                    if patrol == 2:
                        print("The enemy's Patrol Ship has been destroyed.")
                # After hitting all the ship points, returns hits and misses
                if hits == 17:
                    return hits, miss     
                print_grid(temp_grid)              

def print_grid(grid):
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    print()
    print("   0  1  2  3  4  5  6  7  8  9")
    for i in range(10):
        print(letters[i], end="")
        for j in range(10):
            print("  " + grid[i][j], end="")
        print()
    print()

def print_hof():
    print("\n\n~~~~~~~~ Hall of Fame ~~~~~~~~")
    print("Rank : Accuracy :  Player Name\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    dict = hall_fame()
    for i in range(len(dict)):
        print("{}".format(int(i+1)).rjust(4) + "{}%".format(dict[i+1]['score']).rjust(11) + str(dict[i+1]['name']).rjust(15))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()

def write_hof(dict, hits, misses, name):
    accuracy = format((hits / (hits + misses)) * 100, ',.2f')
    lin = name + ',' + str(hits) + ',' + str(misses) + '\n'
    if len(dict) == 0 or float(accuracy) <= float(dict[len(dict)]['score']):
        with open("battleship_hof.txt", "a") as fo:
            fo.write(name + ',' + str(hits) + ',' + str(misses) + '\n')
    else:
        rank = 0
        for i in range(len(dict)):
            if float(accuracy) > float(dict[i + 1]['score']):
                rank = i + 1
                break
        
        lines = []
        with open('battleship_hof.txt') as fo:
            lines = fo.readlines()
        lines.insert(rank, lin)
        if len(lines) > 10:
            lines.pop()
        with open('battleship_hof.txt', 'w') as fo:
            fo.writelines(lines)

def main():
    print("\n               ~ Welcome to Battleship! ~               \n")
    print('ChatGPT has gone rogue and commandeered a space strike')
    print("fleet. It's on a mission to take over the world.  We've")
    print("located the stolen ships, but we need your superior") 
    print("intelligence to help us destroy them before it's too")
    print('late.\n')
    choices = ['1 : Instructions', "2 : View Example Map", '3 : New Game', '4 : Hall of Fame', '5 : Quit']
    choice = 0
    while choice != 5:
        print("Menu:")
        for i in choices:
            print("  " + i)
        choice = input("What would you like to do? ")
        if choice.isnumeric():
            choice = int(choice)
        if choice == 1:
            print("\nInstructions:\n")
            print('Ships are positioned at fixed locations in a 10-by-10\n\
grid. The rows of the grid are labeled A through J, and\n\
the columns are labeled 0 through 9. Use menu option\n\
"2" to see an example. Target the ships by entering the\n\
row and column of the location you wish to shoot. A\n\
ship is destroyed when all of the spaces it fills have\n\
been hit. Try to destroy the fleet with as few shots as\n\
possible. The fleet consists of the following 5 ships:\n')
            print("Size : Type\n\
    5 : Mothership\n\
    4 : Battleship\n\
    3 : Destroyer\n\
    3 : Stealth Ship\n\
    2 : Patrol Ship\n")
        if choice == 2:
            print_grid(make_grid())
            print()
        if choice == 4:
            print_hof()
        if choice == 3:
            grid = make_grid() 
            hits, miss = the_game(grid)
            print()
            if hits == 17:
                print("You've destroyed the enemy fleet!\nHumanity has been saved from the threat of AI.\n\nFor now ...\n")

                accuracy = float(hits / (hits + miss)) * 100
                dict = hall_fame()
                last_place = 0
                if len(dict) > 0:
                    last_place = float(dict[len(dict)]['score'])
                if accuracy >= last_place or len(dict) < 10:
                    print("Congratulations, you have achieved a targeting accuracy\n\
of {}% and earned a spot in the Hall of Fame.".format(format(accuracy, ',.2f')))
                    name = input("Enter your name: ")
                    write_hof(dict, hits, miss, name)
                    print_hof()
                else:
                    print("Your targeting accuracy was {}%.".format(format(accuracy, ',.2f')))
                    print()
        if choice not in range(1,6):
            print("\nInvalid selection.  Please choose a number from the menu.\n")
    
    print("\nGoodbye\n")
