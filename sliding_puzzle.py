import pygame
import sys
from pygame.locals import *

FPS = 30
BOARD_HEIGHT = 4
BOARD_WIDTH = 4
BOARD = [[cell + (row * BOARD_WIDTH) for cell in range(1, BOARD_WIDTH + 1)] for row in range(BOARD_HEIGHT)]
BOARD[BOARD_WIDTH - 1][BOARD_HEIGHT - 1] = 0

BOX_SIZE = 100
GAP_SIZE = 5
MARGIN_SIZE = 20
INFO_SIZE = 0
WINDOW_WIDTH = (BOX_SIZE * BOARD_WIDTH) + ((GAP_SIZE * BOARD_WIDTH) - GAP_SIZE) + (MARGIN_SIZE * 2)
WINDOW_HEIGHT = WINDOW_WIDTH + INFO_SIZE
FONT_SIZE = 32

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BOX_COLOR = GREEN
FONT_COLOR = BLACK
BG_COLOR = BLUE


def main():
    global DISPLAY_SURFACE, FPSCLOCK
    pygame.init()

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
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        FPSCLOCK.tick(FPS)


def draw_board():
    DISPLAY_SURFACE.fill(BG_COLOR)
    for row in range(len(BOARD)):
        for cell in range(len(BOARD[row])):
            if BOARD[row][cell] != 0:
                x = MARGIN_SIZE + (BOX_SIZE * cell) + (GAP_SIZE * cell)
                y = MARGIN_SIZE + INFO_SIZE + (BOX_SIZE * row) + (GAP_SIZE * row)
                draw_box((x, y, BOX_SIZE, BOX_SIZE), BOARD[row][cell])


def draw_box(rect, num):
    font = pygame.font.Font("freesansbold.ttf", FONT_SIZE)
    label = font.render(str(num), True, FONT_COLOR)
    label_rect = label.get_rect()
    box = pygame.Rect(rect)
    label_rect.center = box.center
    pygame.draw.rect(DISPLAY_SURFACE, BOX_COLOR, box)
    DISPLAY_SURFACE.blit(label, label_rect)


main()
