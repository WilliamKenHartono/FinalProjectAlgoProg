import pygame, sys
import numpy as np
import random
pygame.init()

# ALL the variables that will draw the board
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

BG_COLOR = (20, 200, 160)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Displays the width and height
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'TIC TAC TOE' )
screen.fill( BG_COLOR )

# The variable board
board = np.zeros( (BOARD_ROWS, BOARD_COLS) )

# The drawing of the game board
def draw_lines():

    pygame.draw.line( screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH )

    pygame.draw.line( screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH )

    pygame.draw.line( screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH )

    pygame.draw.line( screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH )

# Used to draw the circle and the lines for cross
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle( screen, CIRCLE_COLOR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
            elif board[row][col] == 2:
                pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )
                pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )

# function for marking the board
def mark_square(row, col, player):
    board[row][col] = player

# Function returns true if square is available and false if not available
def available_square(row, col):
    return board[row][col] == 0

# Returns true if board is full and if board is not true, function returns false, this will loop through rows and columns
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False

    return True

# Greedy AI
def greedy(board):
    # Greedy AI is player 2 and its opponent (you) is player 1
    greedAI = 2
    opponent = 1
    possible = []

    # First, check if greedAI can win in the next move
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = greedAI
                if calc_check_win(greedAI):
                    board[row][col] = 0
                    return row * 3 + col
                board[row][col] = 0

    # If no winning move, then check if opponent can win in the next move and block it
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = opponent
                if calc_check_win(opponent):
                    board[row][col] = 0
                    return row * 3 + col
                board[row][col] = 0
                possible.append(row * 3 + col)
    # Both codes brute force every possible combination to see if is possible or if one player is going to win and then swiftly undoing the move
    # If neither can win in the next move, choose a random available square
    return random.choice(possible) if possible else None

# Translates the single number input for the AI (0-8) into 2 variables of rows and cols
def greedToPlayer(AI_Input):
    match AI_Input:
        case 0:
            AI_row = 0
            AI_col = 0
        case 1:
            AI_row = 0
            AI_col = 1
        case 2:
            AI_row = 0
            AI_col = 2
        case 3:
            AI_row = 1
            AI_col = 0
        case 4:
            AI_row = 1
            AI_col = 1
        case 5:
            AI_row = 1
            AI_col = 2
        case 6:
            AI_row = 2
            AI_col = 0
        case 7:
            AI_row = 2
            AI_col = 1
        case 8:
            AI_row = 2
            AI_col = 2
    return AI_row, AI_col


# Checks win conditions for player without drawing the winning lines
def calc_check_win(player):
    # Checks for win condition in vertical lines
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    # Checks for win condition in horizontal lines
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    # Checks for win condition in diagonal lines
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    
    return False

def check_win(player):
    # Checks for win condition in vertical lines
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True
    # Checks for win condition in horizontal lines
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True
    # Checks for win condition in diagonal lines
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player)
        return True
    # If nobody wins then game is not won
    return False



# Draws vertical winning lines and changes color based on player that won
def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE//2

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line( screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH )

# Draws horizontal winning lines and changes color based on player that won 
def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE//2

    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH )

# Draws ascending diagonal winning line and changes color based on player that won
def draw_asc_diagonal(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH )

# Draws descending diagonal winning line and changes color based on player that won
def draw_desc_diagonal(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH )

# A restart function to try again for when game ends or you rage quit in the middle
def restart():
    screen.fill( BG_COLOR )
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

# Main function of the game is below
draw_lines()

# The game is not over and player starts at one
player = 1
game_over = False
# Main loop of the main game
while True:
    for event in pygame.event.get():
        # Exits game if the game quits
        if event.type == pygame.QUIT:
            sys.exit()

        # when mouse is pressed and game didnt end, determine location of click
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)
            
            # Checks if clicked square is taken and if not then it runs the code
            if available_square( clicked_row, clicked_col ):
                mark_square( clicked_row, clicked_col, player )
                if check_win( player ):
                    game_over = True
                else:
                    player = player % 2 + 1
                draw_figures()

        # Checks if its player 2. AI takes control
        if player == 2:
            # Now this is where the AI comes into place. If the game is not over, the code finds out what the AI's Row and Cols
            if not game_over:
                AI_row, AI_col = greedToPlayer(greedy(board))
                # Checks if square is square is taken and if not then it runs the code
                if available_square( AI_row, AI_col ):
                    # Marks square and checks if game is won
                    mark_square( AI_row, AI_col, player )
                    if check_win( player ):
                        game_over = True
                    else:
                        player = player % 2 + 1
                    draw_figures()

        # Restart button
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1
                game_over = False

    pygame.display.update()