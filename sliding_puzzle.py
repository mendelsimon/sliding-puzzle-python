import pygame
import sys
import random
from pygame.locals import *

FPS = 30
BOARD_HEIGHT = 4
BOARD_WIDTH = 4
BOARD = [[cell + (row * BOARD_WIDTH) for cell in range(1, BOARD_WIDTH + 1)] for row in range(BOARD_HEIGHT)]
BOARD[BOARD_HEIGHT - 1][BOARD_WIDTH - 1] = 0

BOX_SIZE = 100
GAP_SIZE = 5
MARGIN_SIZE = 20
INFO_SIZE = 0
WINDOW_WIDTH = (BOX_SIZE * BOARD_WIDTH) + ((GAP_SIZE * BOARD_WIDTH) - GAP_SIZE) + (MARGIN_SIZE * 2)
WINDOW_HEIGHT = (BOX_SIZE * BOARD_HEIGHT) + ((GAP_SIZE * BOARD_HEIGHT) - GAP_SIZE) + (MARGIN_SIZE * 2) + INFO_SIZE

SHUFFLE_MOVES = 50
FONT_SIZE = 32
ANIMATE_SPEED = 25

ROW_INDEX = 0
CELL_INDEX = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BOX_COLOR = GREEN
FONT_COLOR = BLACK
BG_COLOR = BLUE

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'


def main():
    global DISPLAY_SURFACE, FPSCLOCK, FONT
    pygame.init()

    FONT = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
    FPSCLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sliding Puzzle")

    while True:
        play_game()
        play_win_screen()


def play_game():
    draw_board()
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_UP:
                    move(UP)
                elif event.key == K_DOWN:
                    move(DOWN)
                elif event.key == K_LEFT:
                    move(LEFT)
                elif event.key == K_RIGHT:
                    move(RIGHT)
                elif event.key == K_s:
                    shuffle()

        FPSCLOCK.tick(FPS)


def draw_board():
    """Draws the game board"""
    DISPLAY_SURFACE.fill(BG_COLOR)
    for row in range(len(BOARD)):
        for cell in range(len(BOARD[row])):
            if BOARD[row][cell] > 0:
                x, y = get_box_position((row, cell))
                draw_box((x, y, BOX_SIZE, BOX_SIZE), BOARD[row][cell])


def get_box_position(box):
    """Returns the x and y coordinates of the specified box"""
    row = box[ROW_INDEX]
    cell = box[CELL_INDEX]

    x = MARGIN_SIZE + (BOX_SIZE * cell) + (GAP_SIZE * cell)
    y = MARGIN_SIZE + INFO_SIZE + (BOX_SIZE * row) + (GAP_SIZE * row)
    return x, y


def draw_box(rect, num):
    """Draws the rect, with the num in middle"""
    label = FONT.render(str(num), True, FONT_COLOR)
    label_rect = label.get_rect()
    box = pygame.Rect(rect)
    label_rect.center = box.center
    pygame.draw.rect(DISPLAY_SURFACE, BOX_COLOR, box)
    DISPLAY_SURFACE.blit(label, label_rect)


def move(direction):
    """Moves the appropriate box in the specified direction, if possible."""
    TOP = 0
    BOTTOM = BOARD_HEIGHT - 1
    LEFTMOST = 0
    RIGHTMOST = BOARD_WIDTH - 1

    blank = find_blank()
    row = blank[ROW_INDEX]
    cell = blank[CELL_INDEX]

    if direction == UP and row != BOTTOM:
        value = BOARD[row + 1][cell]
        BOARD[row + 1][cell] = 0
        animate((row + 1, cell), blank, value)
        BOARD[row][cell] = value
    elif direction == DOWN and row != TOP:
        value = BOARD[row - 1][cell]
        BOARD[row - 1][cell] = 0
        animate((row - 1, cell), blank, value)
        BOARD[row][cell] = value
    elif direction == LEFT and cell != RIGHTMOST:
        value = BOARD[row][cell + 1]
        BOARD[row][cell + 1] = 0
        animate((row, cell + 1), blank, value)
        BOARD[row][cell] = value
    elif direction == RIGHT and cell != LEFTMOST:
        value = BOARD[row][cell - 1]
        BOARD[row][cell - 1] = 0
        animate((row, cell - 1), blank, value)
        BOARD[row][cell] = value

    draw_board()
    pygame.display.update()


def find_blank():
    """Finds the 0 on the board. Returns a tuple: (row, cell)"""
    for row in range(len(BOARD)):
        for cell in range(len(BOARD[row])):
            if BOARD[row][cell] == 0:
                return (row, cell)
    raise Exception("Was not able to find the blank cell")


def animate(start_box, end_box, num):
    """Animates the specified box moving in the specified direction"""
    x, y = get_box_position(start_box)
    end_x, end_y = get_box_position(end_box)
    delta_x, delta_y = end_x - x, end_y - y
    if delta_x + delta_y > 0:
        x_step = y_step = ANIMATE_SPEED
    else:
        x_step = y_step = -ANIMATE_SPEED

    if delta_x != 0:
        for new_x in range(x, end_x, x_step):
            draw_board()
            draw_box((new_x, y, BOX_SIZE, BOX_SIZE), num)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    elif delta_y != 0:
        for new_y in range(y, end_y, y_step):
            draw_board()
            draw_box((x, new_y, BOX_SIZE, BOX_SIZE), num)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    else:
        raise Exception("Nothing to animate")


def play_win_screen():
    """Displays a message informing the player that they won"""
    # TODO implement win screen


def shuffle():
    """Shuffles the board intelligently. Does not make invalid moves, or undo last move"""
    TOP = 0
    BOTTOM = BOARD_HEIGHT - 1
    LEFTMOST = 0
    RIGHTMOST = BOARD_WIDTH - 1
    blank_row, blank_cell = find_blank()

    moves = []
    for i in range(0, SHUFFLE_MOVES):
        previous_move = ""
        if i > 0:
            previous_move = moves[i-1]
        choices = []
        if blank_row != TOP and previous_move != UP:
            choices.append(DOWN)
        if blank_row != BOTTOM and previous_move != DOWN:
            choices.append(UP)
        if blank_cell != LEFTMOST and previous_move != LEFT:
            choices.append(RIGHT)
        if blank_cell != RIGHTMOST and previous_move != RIGHT:
            choices.append(LEFT)

        moves.append(random.choice(choices))

        if moves[i] == UP:
            blank_row += 1
        elif moves[i] == DOWN:
            blank_row -= 1
        elif moves[i] == LEFT:
            blank_cell += 1
        elif moves[i] == RIGHT:
            blank_cell -= 1

    for direction in moves:
        if len(pygame.event.get(QUIT)) > 0 or pygame.key.get_pressed()[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        move(direction)


main()
