import pygame
from tile import Tile
from config import DIFFICULTIES, difficulty, WIDTH, HEIGHT, FPS, MARGIN

# setup tiles and bomb count
GRID_SIZE = DIFFICULTIES[difficulty]["grid_size"]
BOMB_COUNT = DIFFICULTIES[difficulty]["bombs"]

# setup cell size
def GetCellSize(grid_size, width, height, margin):
    maxCellW = (width - (grid_size - 1) * margin) / grid_size
    maxCellH = (height - (grid_size - 1) * margin) / grid_size
    return int(min(maxCellW, maxCellH))


CELL_SIZE = GetCellSize(GRID_SIZE, WIDTH, HEIGHT, MARGIN)

FONT = None
NUMBER_COLOURS = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 255, 255),
    7: (0, 0, 0),
    8: (128, 128, 128),
}

def InitGraphics():
    global FONT
    FONT = pygame.font.SysFont(None, 30)

def DrawCellBack(screen, cell, rect):
    colour = (160, 160, 160)

    # cell box colour
    if cell.visible:
        if cell.value == 0:
            colour = (245, 245, 245)
        elif cell.value > 0:
            colour = (220, 220, 220)

    pygame.draw.rect(screen, colour, rect)

def DrawCellValue(screen, cell, rect):
    text = FONT.render(" ", True, (0, 0, 0))

    if cell.flagged:
        text = FONT.render("F", True, (255, 0, 0))
    elif cell.visible and cell.value > 0:
        colour = NUMBER_COLOURS.get(cell.value, (0, 0, 0))
        text = FONT.render(str(cell.value), True, colour)

    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)

def DrawBoard(screen, grid):
    screen.fill((255, 255, 255))

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * (CELL_SIZE + MARGIN)
            y = row * (CELL_SIZE + MARGIN)

            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            cell = grid[row][col]

            DrawCellBack(screen, cell, rect)
            DrawCellValue(screen, cell, rect)