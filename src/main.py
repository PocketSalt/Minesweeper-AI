import pygame

from tile import Tile
from graphics import GRID_SIZE, BOMB_COUNT, DrawBoard, InitGraphics, CELL_SIZE
from config import DIFFICULTIES, difficulty, player, WIDTH, HEIGHT, FPS, MARGIN
from game import GameState
from ai import GetMove, OutputAIStats, AIClear, MidRunAIStats, WriteToCSV

# track AI
wins = 0
losses = 0
runCount = 0

game = GameState(GRID_SIZE, BOMB_COUNT)
global currentState

def GetKeys():
    global currentState, running, player
    for event in pygame.event.get():

        # handles quits
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # restart
            if event.key == pygame.K_r:
                # r counts as a loss
                currentState = 2

        if event.type == pygame.MOUSEBUTTONDOWN and currentState == 0 and player == 0:
            x, y = pygame.mouse.get_pos()
            col = x // (CELL_SIZE + MARGIN)
            row = y // (CELL_SIZE + MARGIN)

            # check if within bounds
            if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                if event.button == 1: # left click
                    if not game.grid[row][col].flagged:
                        game.Reveal(row, col)
                        if game.grid[row][col].value == -1:
                            currentState = 2

                if event.button == 3: # right click
                    if not game.grid[row][col].visible:
                        game.grid[row][col].flag()

def main():
    global currentState, running, wins, losses, runCount
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()

    running = True

    currentState = 0
    InitGraphics()

    while running:
        DrawBoard(screen, game.grid)

        GetKeys()

        if runCount == 1000:
            running = False

        # check if lost:
        if (Tile.correctFlagCount == DIFFICULTIES[difficulty]["bombs"]):
            currentState = 1

        if currentState == 0:
            if player == 1:
                currentState = GetMove(game)

        else:
            if currentState == 2:
                print("You Lost!")
                losses += 1
            elif currentState == 1:
                print("You Won!")
                wins += 1

            WriteToCSV(currentState, Tile.correctFlagCount, DIFFICULTIES[difficulty]["bombs"], wins, losses)
            game.Restart()
            AIClear()
            MidRunAIStats(wins, losses)
            runCount += 1
            currentState = 0

        pygame.display.flip()
        clock.tick(FPS)

    # stop running: output AI stats

    if player == 1:
        OutputAIStats(wins, losses)
    pygame.quit()

if __name__ == "__main__":
    main()
