from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import random
import numpy as np
import time

class LocalBot(Bot):
    def get_action(self, state: GameState) -> GameAction:
        # returns GameAction: ("row", (j, i))
        # executes whenever game is not finished (TODO: necessary?)

        # TODO: timer start

        # validates whether all rows and cols are not marked
        all_row_marked = np.all(state.row_status == 1)
        all_col_marked = np.all(state.col_status == 1)
        all_marked = all_row_marked and all_col_marked

        # generates complete board state
        # countEmpty = np.count_nonzero(state.row_status == 0) + np.count_nonzero(state.col_status == 1)
        # if countEmpty == 15 or countEmpty == 16:
        self.tempBoard = np.zeros(shape=(3, 3))
        self.tempRow = np.zeros(shape=(4, 3))
        self.tempCol = np.zeros(shape=(3, 4))
        player1 = state.player1_turn
        self.tempRow, self.tempCol, self.tempBoard = self.fillBoard(self.tempRow, self.tempCol, self.tempBoard, player1)

        # here: board status already filled randomly and row/col status filled

        # main local search algorithm
        if not all_marked:
            return self.hillClimbing1(state)
        
        # TODO: timer end
    
    # A. SUPPORTING FUNCTIONS
    # gets player ID from state
    def getPlayer(self, player1):
        if player1:
            player = 1
        else:
            player = 2
        return player

    # B. OBJECTIVE FUNCTIONS
    # calculates objective function of complete state
    def evaluate(self, matrix: np.ndarray):
        score = 0
        for i in range (0,3):
            for j in range (0,3):
                if matrix[i,j] == 4:
                   score += 1
                elif matrix[i,j] == -4:
                    score -= 1
        return score

    # counts number of chains
    def countChain(self, rowstatus: np.ndarray, colstatus: np.ndarray):
        # observation: 6 -> 3 chain, 7 -> 4 chain, 8 -> 5 chain, etc.
        # count in row
        count = 0
        (x, y) = rowstatus.shape
        for i in range (1, x-1):
            for j in range (y):
                count += rowstatus[i][j]        

        # count in col
        (x, y) = colstatus.shape
        for i in range (x):
            for j in range(1, y-1):
                count += colstatus[i][j]

        return count - 3
    
    # converts number of chains into points
    def pointChain(self, rowstatus: np.ndarray, colstatus: np.ndarray):
        count = self.countChain(rowstatus, colstatus)
        if count % 2 == 1:
            point = 10
        else:
            point = 0
        return point

    # verifies if board status is less than or equal to 2
    def countBoard(self, move, matrix: np.ndarray, pos):
        [x, y] = pos
        num1 = 0
        num2 = 0

        # above line/left of line
        if x < 3 and y < 3:
            num1 = (abs(matrix[x][y]) + 1)

        # below line
        if (move == "row"):
            if x >= 1:
                num2 = abs(matrix[x-1][y]) + 1
        # right of line
        else:
            if y >= 1:
                num2 = abs(matrix[x][y-1]) + 1

        return num1, num2
    
    # converts quality of line position on board into points
    def pointBoard(self, move, matrix:np.ndarray, pos):
        num1, num2 = self.countBoard(move, matrix, pos)
        point = 0

        # two boxes
        if num1 == 4 and num2 == 4:
            point += 25
        # one box and another prepared
        elif (num1 == 4 and num2 == 3) or (num1 == 3 and num2 == 4):
            point += 20
        # one box
        elif (num1 == 4 or num2 == 4):
            point += 15
        # two boxes prepared for opponent
        elif (num1 == 3 and num2 == 3):
            point -= 20
        # one box prepared for opponent
        elif (num1 == 3 or num2 == 3):
            point -= 15
        # boxes prepared
        elif (num1 == 2 or num2 == 2):
            point += 10
        else:
            point += 5

        return point

    # calculates objective function of move (additional value)
    def calcObjective(self, state:GameState, move, pos):
        count = 0

        # strategy: plays until all board status are 2, while maintaining odd number of chains
        count += self.pointChain(state.row_status, state.col_status)
        count += self.pointBoard(move, state.board_status, pos)

        return count
    
    # C. STATUS FUNCTIONS
    # copies status of matrix
    def copyStatus(self, matrix: np.ndarray):
        [x, y] = matrix.shape
        tempMatrix = np.zeros(shape=(x, y))
        for i in range (x):
            for j in range (y):
                tempMatrix[i][j] = matrix[i][j]
        return tempMatrix

    # fills all line status of row/col
    def fillStatus(self, matrix: np.ndarray):
        [x, y] = matrix.shape
        for i in range (x):
            for j in range (y):
                matrix[i][j] += 1
        return matrix
    
    # fills one line status of row/col
    def fillLineStatus(self, matrix: np.ndarray, pos):
        [x, y] = pos
        matrix[x][y] += 1
        return matrix

    # fills box status of board whenever fills one line
    def fillBoardStatus(self, move, matrix: np.ndarray, pos, player):
        [x, y] = pos

        if (player == 1):
            playerMod = -1
        else:
            playerMod = 1

        newFilled1 = False # left/up
        newFilled2 = False # right/down

        # above line/left of line
        if x < 3 and y < 3:
            matrix[x][y] = (abs(matrix[x][y]) + 1) * playerMod
            newFilled1 = matrix[x][y] == 4 or matrix[x][y] == -4

        # below line
        if (move == "row"):
            if x >= 1:
                matrix[x-1][y] = (abs(matrix[x-1][y]) + 1) * playerMod
                newFilled2 = matrix[x-1][y] == 4 or matrix[x-1][y] == -4
        # right of line
        else:
            if y >= 1:
                matrix[x][y-1] = (abs(matrix[x][y-1]) + 1) * playerMod
                newFilled2 = matrix[x][y-1] == 4 or matrix[x][y-1] == -4
        
        return matrix, (newFilled1 or newFilled2) # True if double move

    # gets a random valid move as a backup of bad neighbors
    def getRandMove(self, rowstatus: np.ndarray, colstatus: np.ndarray):
        allRowFilled = self.isAllLineFilled(rowstatus)
        allColFilled = self.isAllLineFilled(colstatus)
        
        # gets the correct status
        if (not allRowFilled and not allColFilled):
            p = random.randrange(0, 2)
            if (p == 0):
                move = "row"
                matrix = rowstatus
                [x, y] = rowstatus.shape
            else:
                move = "col"
                matrix = colstatus
                [x, y] = colstatus.shape
        elif (allRowFilled):
            move = "col"
            matrix = colstatus
            [x, y] = colstatus.shape
        elif (allColFilled):
            move = "row"
            matrix = rowstatus
            [x, y] = rowstatus.shape

        # finds a valid move
        a = -1
        b = -1
        valid = False

        while not valid:
            a = random.randrange(0, x)
            b = random.randrange(0, y)
            valid = (matrix[a][b] == 0)

        return GameAction(move, (b, a))

    # gets random empty position
    def getRandEmptyPos(self, matrix: np.ndarray):
        [x, y] = matrix.shape

        a = -1
        b = -1
        valid = False

        while not valid:
            a = random.randrange(0, x)
            b = random.randrange(0, y)
            valid = (matrix[a][b] == 0)

        return (a, b)
    
    # checks whether all line is filled
    def isAllLineFilled(self, matrix: np.ndarray):
        [x, y] = matrix.shape

        for i in range (x):
            for j in range(y):
                if matrix[i][j] == 0:
                    return False
        return True

    # gets a random valid move
    def moveRand(self, rowstatus, colstatus, boardstatus, player):
        allRowFilled = self.isAllLineFilled(rowstatus)
        allColFilled = self.isAllLineFilled(colstatus)
        
        if (not allRowFilled and not allColFilled):
            p = random.randrange(0, 2)
            if (p == 0):
                move = "row"
            else:
                move = "col"
        elif (allRowFilled):
            move = "col"
        elif (allColFilled):
            move = "row"
        else:
            remove = False
        
        if move == "row":
            pos = self.getRandEmptyPos(rowstatus)
            rowstatus = self.fillLineStatus(rowstatus, pos)
            boardstatus, remove = self.fillBoardStatus(move, boardstatus, pos, player)
        else:
            pos = self.getRandEmptyPos(colstatus)
            colstatus = self.fillLineStatus(colstatus, pos)
            boardstatus, remove = self.fillBoardStatus(move, boardstatus, pos, player)

        return rowstatus, colstatus, boardstatus, remove, pos, move
    
    # completes the board
    def fillBoard(self, rowstatus, colstatus, boardstatus, player1):
        player = self.getPlayer(player1)
        
        counter = 1
        allRowFilled = self.isAllLineFilled(rowstatus)
        allColFilled = self.isAllLineFilled(colstatus)

        while (not allRowFilled or not allColFilled):
            remove = True
            # moves player
            while remove and (not allRowFilled or not allColFilled):
                rowstatus, colstatus, boardstatus, remove, pos, move = self.moveRand(rowstatus, colstatus, boardstatus, player)
                allRowFilled = self.isAllLineFilled(rowstatus)
                allColFilled = self.isAllLineFilled(colstatus)
                counter += 1
            
            # switches player
            if player == 1:
                player = 2
            else:
                player = 1

        return rowstatus, colstatus, boardstatus

    # deletes line on board
    def delLineonBoard(self, move, matrix: np.ndarray, pos, player):
        [x, y] = pos
        tempMatrix = np.zeros(shape=(3, 3))
        tempMatrix = self.copyStatus(matrix)

        if (player == 1):
            playerMod = -1
        else:
            playerMod = 1

        # above line/left of line
        if x < 3 and y < 3:
            tempMatrix[x][y] = abs(tempMatrix[x][y]) * playerMod

        # below line
        if (move == "row"):
            if x >= 1:
                tempMatrix[x-1][y] = abs(tempMatrix[x-1][y]) * playerMod
        # right of line
        else:
            if y >= 1:
                tempMatrix[x][y-1] = abs(tempMatrix[x][y-1]) * playerMod

        return tempMatrix
    
    # switches coordinates to match program's code
    def switchPos(self, pos):
        [x, y] = pos
        return (y, x)

    # implements local search: hill-climbing with steepest ascent
    def hillClimbing1(self, state:GameState) -> GameAction:
        # strategy: fills all row/colstatus and boardstatus to complete initial state

        player = self.getPlayer(state.player1_turn)
        currentValue = self.evaluate(self.tempBoard)
        bestValue = 0
        bestMove, bestPos = self.getRandMove(state.row_status, state.col_status)
        # possibleMove = []
        
        # insert line in empty position
        emptyRows = np.argwhere(state.row_status == 0)
        for pos in emptyRows:
            value = self.evaluate(self.delLineonBoard("row", self.tempBoard, pos, player))
            print(pos, value)
            # print(pos)
            # print("row", state.player1_turn)
            # print("value", value)
            # print("add value", self.calcObjective(state, "row", pos))
            if state.player1_turn and value - self.calcObjective(state, "row", pos) < bestValue:
                bestValue = value - self.calcObjective(state, "row", pos)
                bestPos = self.switchPos(pos)
                bestMove = "row"
                # print("best")
            elif not state.player1_turn and value + self.calcObjective(state, "row", pos) > bestValue:
                bestValue = value + self.calcObjective(state, "row", pos)
                bestPos = self.switchPos(pos)
                bestMove = "row"
                # print("best")
                
        emptyCols = np.argwhere(state.col_status == 0)
        for pos in emptyCols:
            value = self.evaluate(self.delLineonBoard("col", self.tempBoard, pos, player))
            print(pos, value)
            # print(pos)
            # print("col", state.player1_turn)
            # print("value", value)
            # print("add value", self.calcObjective(state, "col", pos))
            if state.player1_turn and value - self.calcObjective(state, "col", pos) < bestValue:
                bestValue = value - self.calcObjective(state, "col", pos)
                bestPos = self.switchPos(pos)
                bestMove = "col"
                # print("best")
            elif not state.player1_turn and value + self.calcObjective(state, "col", pos) > bestValue:
                bestValue = value + self.calcObjective(state, "col", pos)
                bestPos = self.switchPos(pos)
                bestMove = "col"
                # print("best")
        
        # main hill-climbing
        if state.player1_turn:
            if bestValue < currentValue:
                return GameAction(bestMove, bestPos)
        else:
            if bestValue > currentValue:
                return GameAction(bestMove, bestPos)
        
        return self.getRandMove(state.row_status, state.col_status)

    def hillClimbing2():
        # strategy: greedy, put in another file
        return