import random

# Global game parameters
grid_size = 0
num_carrots = 0
num_holes = 0

def generate_map():
    global grid_size, num_carrots, num_holes
    width, height = grid_size, grid_size

    # Create an empty map
    map_grid = [['-' for _ in range(width)] for _ in range(height)]

    # Place rabbit
    rabbit_x, rabbit_y = random.randint(0, width - 1), random.randint(0, height - 1)
    map_grid[rabbit_y][rabbit_x] = 'r'

    # Place carrots
    for _ in range(num_carrots):
        while True:
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            if map_grid[y][x] == '-':
                map_grid[y][x] = 'c'
                break

    # Place rabbit holes
    for _ in range(num_holes):
        while True:
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            if map_grid[y][x] == '-':
                map_grid[y][x] = 'O'
                break

    return map_grid
def print_instructions():
    print("\nIntroduction: Our friendly neighbourhood rabbit, Mr. Bunny wants to gather carrots from the yard and take them back to his humble abode.")
    print("He needs your help in picking up the carrots from the yard and dropping them in his rabbit hole.")
    print("\nInstructions:")
    print("For playing the remember the following commands:")
    print("\na - Move left")
    print("d - Move right")
    print("w - Move up")
    print("s - Move down")
    print("p - Put carrot in rabbit hole")
    print("j - Jump across rabbit hole (if adjacent)")
    print("q - Quit the game")

def find_rabbit_position(game_map):
    rabbit_positions = [(x, y) for y in range(len(game_map)) for x in range(len(game_map[y])) if game_map[y][x] in ('r', 'R')]
    return rabbit_positions

def move_rabbit(action, x, y):
    if action == 'a':
        return x - 1, y
    elif action == 'd':
        return x + 1, y
    elif action == 'w':
        return x, y - 1
    elif action == 's':
        return x, y + 1


def is_valid_move(game_map, x, y, holding_carrot):
    if 0 <= x < len(game_map[0]) and 0 <= y < len(game_map):
        if game_map[y][x] == 'c' and not holding_carrot:
            return True
        return game_map[y][x] not in ('c', 'O')
    return False
    

def jump_rabbit(game_map, x, y):
    if game_map[y][x] == 'O':
        game_map[y][x] = '-'
        game_map[y - 1][x] = 'R'

def play_game(game_map):
    rabbit_positions = find_rabbit_position(game_map)
    rabbit_x, rabbit_y = rabbit_positions[0]  # Get the first rabbit position
    holding_carrot = False
    while True:
        
        for row in game_map:
            print("".join(row))

        action = input("Enter your move (a/d/w/s/p/j/q to quit): ").lower()

        if action == 'q':
            break
        elif action in ('a', 'd', 'w', 's'):
            new_x, new_y = move_rabbit(action, rabbit_x, rabbit_y)
            if is_valid_move(game_map, new_x, new_y, holding_carrot):
                if game_map[new_y][new_x] == 'c':
                    holding_carrot = True
                    game_map[new_y][new_x] = 'R'
                else:
                    game_map[new_y][new_x] = 'R' if holding_carrot else 'r'
                game_map[rabbit_y][rabbit_x] = '-'
                rabbit_x, rabbit_y = new_x, new_y
        elif action == 'p':
            if holding_carrot:
                game_map[rabbit_y][rabbit_x] = '-'
                holding_carrot = False
        elif action == 'j':
            if game_map[rabbit_y][rabbit_x] == 'O':
                jump_rabbit(game_map, rabbit_x, rabbit_y)
            else:
                print("Invalid move! Try again.")

def generate_solution(game_map):
    solution_moves = ['d', 's', 'p', 'w', 'd', 'j', 'p']

    for move in solution_moves:
        rabbit_x, rabbit_y = find_rabbit_position(game_map)

        if move == 'p':
            game_map[rabbit_y][rabbit_x] = '-'
        elif move == 'j':
            jump_rabbit(game_map, rabbit_x, rabbit_y)
        else:
            new_x, new_y = move_rabbit(move, rabbit_x, rabbit_y)
            game_map[rabbit_y][rabbit_x] = '-'
            rabbit_x, rabbit_y = new_x, new_y
            game_map[rabbit_y][rabbit_x] = 'R'

def  main():
    global grid_size, num_carrots, num_holes
    print_instructions()
    grid_size = int(input("Enter grid size (width and height): "))
    num_carrots = int(input("Enter the number of carrots(More than 1): "))
    num_holes = int(input("Enter the number of rabbit holes(More than 1): "))

    game_map = generate_map()

    print("Initial map:")
    
    play_game(game_map)

    if 'R' in [''.join(row) for row in game_map]:
        print("\nSolution map:")
        generate_solution(game_map)
        for row in game_map:
            print("".join(row))
if __name__ == "__main__":
    main()