import time
import csv
import os
from ortools.sat.python import cp_model
from config import DIFFICULTIES, difficulty, AISpeed
from collections import defaultdict

aiActions = []
unfairLosses = 0
csvFile = "AI_stats.csv"
size = DIFFICULTIES[difficulty]["grid_size"]

if os.path.exists(csvFile):
    os.remove(csvFile)

# inheriting from CPSolverSolutionCallback
# to allow the AI to calculate multiple solutions instead of just once
class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, vars):
        super().__init__()
        self.vars = vars
        self.solutions = []

    def on_solution_callback(self):
        assignment = {cell: self.Value(var) for cell, var in self.vars.items()}
        self.solutions.append(assignment)

def AIClear():
    global aiActions
    aiActions = []

def GetMove(game):
    global unfairLosses
    state = 0

    # if there are actions cued...
    if not aiActions:
        aiActions.append(('reveal', 1, 1))
        safeMoves, bombMoves = FindAiMoves(game.grid)
        for r, c in bombMoves:
            aiActions.append(('flag', r, c))
        for r, c in safeMoves:
            aiActions.append(('reveal', r, c))


    # otherwise go through the queue :D
    if aiActions:
        actionType, r, c = aiActions.pop(0)

        if actionType == 'reveal':
            if not game.grid[r][c].visible and not game.grid[r][c].flagged:
                game.Reveal(r, c)
                if game.grid[r][c].value == -1:
                    # this is a remnant of the previous version when 1,1 was never safe
                    # and was used to calculated how many runs ended because of 1,1 being a bomb
                    if r == 1 and c == 1:
                        unfairLosses += 1
                    state = 2

        elif actionType == 'flag':
            if not game.grid[r][c].flagged:
                game.grid[r][c].flag()

        # adjustable delay
        time.sleep(AISpeed)
    return state

def FindAiMoves(board):
    # assign row/col if not set
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            cell.row = r
            cell.col = c

    # find the frontier via defining unknown cells on board
    unknowns = set()
    constraints = []

    for r, row in enumerate(board):
        for c, cell in enumerate(row):

            # for every visible tile with value (therefore next to a bomb or flagged bomb)
            if cell.visible and cell.value >= 0:
                unknownNeighbours = []
                flaggedNeighbours = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        # skip self
                        if not (dr == 0 and dc == 0):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < size and 0 <= nc < size:
                                neighbor = board[nr][nc]
                                if neighbor.flagged:
                                    flaggedNeighbours += 1
                                elif not neighbor.visible:
                                    unknownNeighbours.append(neighbor)

                # if there are covered neighbours, determine the amount of unflagged bombs around self,
                # then update the constraints with that count and the cells/neighbours
                if unknownNeighbours:
                    reqBombs = cell.value - flaggedNeighbours
                    constraints.append((unknownNeighbours, reqBombs))
                    unknowns.update(unknownNeighbours)


    # now that the constraints are filled:
    model = cp_model.CpModel()
    # mapping cell to int 0 safe or 1 bomb
    cellVars = {cell: model.NewIntVar(0, 1, f'{cell.row}_{cell.col}') for cell in unknowns}

    for cells, bombCount in constraints:
        model.Add(sum(cellVars[c] for c in cells) == bombCount)

    solver = cp_model.CpSolver()

    safeMoves = set()
    bombMoves = set() #technically also flagMoves

    # Check every unknown cell and all possible solutions
    collector = SolutionCollector(cellVars)
    solver.SearchForAllSolutions(model, collector)

    # If a cell is always 0 in all solutions, its safe
    # If a cell is always 1 in all solutions, its a bomb
    for cell in unknowns:
        vals = [sol[cell] for sol in collector.solutions]
        if all(v == 0 for v in vals):
            safeMoves.add(cell)
        elif all(v == 1 for v in vals):
            bombMoves.add(cell)


    # If no moves could be made because no 100% certain: Probabilistic Inference :D
    if not safeMoves and not bombMoves:
        probMap = defaultdict(float) # probabilities per cell
        constraintsCountMap = defaultdict(float)

        for cells, bombCount in constraints:
            for cell in cells:
                probMap[cell] += bombCount / len(cells) # adds probability for every time it shows
                constraintsCountMap[cell] += 1 # count how many times it shows

        # normalize probabilities
        for cell in probMap:
            probMap[cell] /= constraintsCountMap[cell] # div so even though it shows up more its not higher chance

        # pick cell with lowest probability of being a bomb
        # must also check if probMap is empty
        if probMap:
            safestCell = None
            lowest = 1.0

            for cell, prob in probMap.items():
                if prob < lowest:
                    lowest = prob
                    safestCell = cell
            safeMoves.add(safestCell)
        else:
            # literally failed to make any move, just pick any
            unknown_cells = []
            for row in board:
                for cell in row:
                    if not cell.visible and not cell.flagged:
                        unknown_cells.append(cell)

            if unknown_cells:
                safeMoves.add(unknown_cells[0])

    return ([(c.row, c.col) for c in safeMoves],
            [(c.row, c.col) for c in bombMoves])

def MidRunAIStats(wins, losses):
    global unfairLosses

    totalGames = wins + losses
    adjustedLosses = losses - unfairLosses
    adjustedTotal = wins + adjustedLosses
    if adjustedTotal <= 0: adjustedTotal = 1

    winPercentage = wins / float(adjustedTotal)

    print("--------------------------------")
    print(f"Run #{totalGames}: {winPercentage}%")
    print("--------------------------------")

def OutputAIStats(wins, losses):
    global unfairLosses

    totalGames = wins + losses
    adjustedLosses = losses - unfairLosses
    adjustedTotal = wins + adjustedLosses
    if adjustedTotal <= 0: adjustedTotal = 1

    winPercentage = wins / float(adjustedTotal)

    print("--------------------------------")
    print(f"Out of {totalGames} {difficulty} game(s):")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Unfair losses account for {unfairLosses} runs.")
    print(f"Therefore final win percentage is: {winPercentage}")
    print("--------------------------------")

def WriteToCSV(win: int, guess: int, total: int, wins, losses):
    global unfairLosses
    totalGames = wins + losses
    adjustedLosses = losses - unfairLosses
    adjustedTotal = wins + adjustedLosses
    if adjustedTotal <= 0: adjustedTotal = 1
    winPercentage = wins / float(adjustedTotal)

    file_exists = os.path.isfile(csvFile)
    with open(csvFile, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Run ID", "Win/Lose", "Percent Bombs", "Overall Percent"])

        result = "W" if win == 1 else "L"
        bombsP = guess / float(total)
        writer.writerow([totalGames, result, bombsP, winPercentage])
