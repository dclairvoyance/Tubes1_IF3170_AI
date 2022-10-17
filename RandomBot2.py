from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import random
import numpy as np
import time

class RandomBot2(Bot):
    def get_action(self, state: GameState) -> GameAction:
        all_row_marked = np.all(state.row_status == 1)
        all_col_marked = np.all(state.col_status == 1)
        all_marked = all_row_marked and all_col_marked

        if not all_marked:
            return self.minimax(0,-999,999,state,True)
            #return self.action(state)

    def evaluate(self, matrix: np.ndarray):
        score = 0
        for i in range (0,3):
            for j in range (0,3):
                if matrix[i,j] == 4:
                   score += 1
                elif matrix[i,j] == -4:
                    score -= 1
        
        return score 


    def get_random_position_with_zero_value(self, matrix: np.ndarray):
        [ny, nx] = matrix.shape

        x = -1
        y = -1
        valid = False
        
        while not valid:
            x = random.randrange(0, nx)
            y = random.randrange(0, ny)
            valid = matrix[y, x] == 0
        
        return (x, y)

    def action(self, state: GameState) -> GameAction:
        temp_status = np.zeros(shape=(3,3))
        for i in range (0,3):
            for j in range (0,3):
                temp_status[i,j] = state.board_status[i,j]
        playerModifier = 1
        
        
        all_row_marked = np.all(state.row_status == 1)
        if not all_row_marked:
            n = self.get_random_position_with_zero_value(state.row_status)
            action_result = GameAction("row", n)
        else:
            n = self.get_random_position_with_zero_value(state.col_status)
            action_result = GameAction("col", n)

        max = 0

        print(state.row_status)
        for i in range (0,4):
            for j in range (0,3):
                if state.row_status[i,j] == 0:
                    if i < 3 and j < 3:
                        temp_status[i,j] = (abs(temp_status[i,j]) + 1) * playerModifier
                    if i >= 1:
                        temp_status[i-1,j] = (abs(temp_status[i-1,j]) + 1) * playerModifier
                    print(str(i) + "," + str(j))
                    print(temp_status)
                    score = self.evaluate(temp_status)
                    if score > max:
                        max = score
                        action_result = GameAction("row", (j,i))
                    for k in range (0,3):
                        for l in range (0,3):
                            temp_status[k,l] = state.board_status[k,l]

        print(state.col_status)
        for i in range (0,3):
            for j in range (0,4):
                if state.col_status[i,j] == 0:
                    if i < 3 and j < 3:
                        temp_status[i][j] = (abs(temp_status[i][j]) + 1) * playerModifier
                    if j>=1:
                        temp_status[i][j-1] = (abs(temp_status[i][j-1]) + 1) * playerModifier
                    print(str(i) + "," + str(j))
                    print(temp_status)
                    score = self.evaluate(temp_status)
                    if score > max:
                        max = score
                        action_result = GameAction("col", (j,i))
                    for k in range (0,3):
                        for l in range (0,3):
                            temp_status[k,l] = state.board_status[k,l]

        print(state.board_status)
        return action_result

    def copy_row_status(self, arr):
        temp_arr = np.zeros(shape=(4,3))
        for i in range (0,4):
            for j in range (0,3):
                temp_arr[i,j] = arr[i,j]
        return temp_arr

    def copy_col_status(self, arr):
        temp_arr = np.zeros(shape=(3,4))
        for i in range (0,3):
            for j in range (0,4):
                temp_arr[i,j] = arr[i,j]
        return temp_arr

    def copy_board_status(self, arr):
        temp_arr = np.zeros(shape=(3,3))
        for i in range (0,3):
            for j in range (0,3):
                temp_arr[i,j] = arr[i,j]
        return temp_arr

    def minimax (self, depth, alpha, beta, state:GameState, playerModifier)->GameAction:
        
        playerModifier = 1
        
        temp_status = self.copy_board_status(state.board_status)
        temp_row_status = self.copy_row_status(state.row_status)
        temp_col_status = self.copy_col_status(state.col_status)    

        start = time.time()
        '''
        all_row_marked = np.all(state.row_status == 1)
        if not all_row_marked:
            n = self.get_random_position_with_zero_value(state.row_status)
            action_result = GameAction("row", n)
        else:
            n = self.get_random_position_with_zero_value(state.col_status)
            action_result = GameAction("col", n)
        '''

        score = -999
        for i in range (0,4):
            for j in range (0,3):
                if temp_row_status[i,j] == 0:
                    temp_row_status[i,j] = 1
                    if i < 3 and j < 3:
                        temp_status[i,j] = (abs(temp_status[i,j]) + 1) * playerModifier
                    if i >= 1:
                        temp_status[i-1,j] = (abs(temp_status[i-1,j]) + 1) * playerModifier

                    if (i<3 and j<3 and temp_status[i,j] == 4):
                        val = self.minimax2(depth, alpha, beta, temp_row_status, temp_col_status, temp_status, True)
                        if val>score:
                            score = val
                            action_result = GameAction("row", (j,i))

                    elif(i>=1 and temp_status[i-1,j] == 4):
                        val = self.minimax2(depth, alpha, beta, temp_row_status, temp_col_status, temp_status, True)
                        if val>score:
                            score = val
                            action_result = GameAction("row", (j,i))

                    else:
                        val = self.minimax2(depth+1, alpha, beta, temp_row_status, temp_col_status, temp_status, False)
                        if val>score:
                            score = val
                            action_result = GameAction("row", (j,i))
                    
                temp_row_status = self.copy_row_status(state.row_status)
                temp_col_status = self.copy_col_status(state.col_status)
                temp_status = self.copy_board_status(state.board_status)

        for i in range (0,3):
            for j in range (0,4):
                if temp_col_status[i,j] == 0:
                    temp_col_status[i,j] = 1
                    if i < 3 and j < 3:
                        temp_status[i][j] = (abs(temp_status[i][j]) + 1) * playerModifier
                    if j>=1:
                        temp_status[i][j-1] = (abs(temp_status[i][j-1]) + 1) * playerModifier

                    if (i<3 and j<3 and temp_status[i,j] == 4):
                        val = self.minimax2(depth, alpha, beta, temp_row_status, temp_col_status, temp_status, True)
                        if val>score:
                            score = val
                            action_result = GameAction("col", (j,i))
                    elif(j>=1 and temp_status[i,j-1] == 4):
                        val = self.minimax2(depth, alpha, beta, temp_row_status, temp_col_status, temp_status, True)
                        if val>score:
                            score = val
                            action_result = GameAction("col", (j,i))
                    else:
                        val = self.minimax2(depth+1, alpha, beta, temp_row_status, temp_col_status, temp_status, False)
                        if val>score:
                            score = val
                            action_result = GameAction("col", (j,i))
            
                temp_row_status = self.copy_row_status(state.row_status)
                temp_col_status = self.copy_col_status(state.col_status)
                temp_status = self.copy_board_status(state.board_status)

        end = time.time()
        print("waktu gerakan: " + str("{:.2f}".format(end-start)))

        return action_result

    def minimax2 (self, depth, alpha, beta, temp_row_status, temp_col_status, temp_status, maximizingPlayer):
        maximum = 999
        minimum = -999
        
        if depth == 3 or (np.all(temp_col_status == 1) and np.all(temp_row_status == 1)):
            return self.evaluate(temp_status)
        
        if maximizingPlayer :

            temp_col_status2 = self.copy_col_status(temp_col_status)
            temp_row_status2 = self.copy_row_status(temp_row_status)
            temp_status2 = self.copy_board_status(temp_status)

            playerModifier = 1
            best = minimum
            for i in range (0,4):
                for j in range (0,3):
                    if temp_row_status2[i,j] == 0:
                        temp_row_status2[i,j] = 1
                        if i < 3 and j < 3:
                            temp_status2[i,j] = (abs(temp_status2[i,j]) + 1) * playerModifier
                        if i >= 1:
                            temp_status2[i-1,j] = (abs(temp_status2[i-1,j]) + 1) * playerModifier
                        
                        if (i<3 and j<3 and temp_status2[i,j] == 4):
                            val = self.minimax2(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, True)
                            best = max(best,val)
                            alpha = max(alpha, best)

                        elif(i>=1 and temp_status2[i-1,j] == 4):
                            val = self.minimax2(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, True)
                            best = max(best,val)
                            alpha = max(alpha, best)

                        else:
                            val = self.minimax2(depth+1, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, False)
                            best = max(best,val)
                            alpha = max(alpha, best)
                        
                        temp_row_status2 = self.copy_row_status(temp_row_status)
                        temp_status2 = self.copy_board_status(temp_status)
                        
                        if beta<=alpha:
                            return best
                    
            for i in range (0,3):
                for j in range (0,4):
                    if temp_col_status2[i,j] == 0:
                        temp_col_status2[i,j] = 1
                        if i < 3 and j < 3:
                            temp_status2[i][j] = (abs(temp_status2[i][j]) + 1) * playerModifier
                        if j>=1:
                            temp_status2[i][j-1] = (abs(temp_status2[i][j-1]) + 1) * playerModifier

                        if (i<3 and j<3 and temp_status2[i,j] == 4):
                            val = self.minimax2(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, True)
                            best = max(best,val)
                            alpha = max(alpha, best)

                        elif(j>=1 and temp_status2[i,j-1] == 4):
                            val = self.minimax2(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, True)
                            best = max(best,val)
                            alpha = max(alpha, best)

                        else:
                            val = self.minimax2(depth+1, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, False)
                            best = max(best,val)
                            alpha = max(alpha, best)
                        
                        temp_col_status2 = self.copy_col_status(temp_col_status)
                        temp_status2 = self.copy_board_status(temp_status)
                        
                        if beta<=alpha:
                            return best

            return best

        elif not maximizingPlayer:

            temp_col_status2 = self.copy_col_status(temp_col_status)
            temp_row_status2 = self.copy_row_status(temp_row_status)
            temp_status2 = self.copy_board_status(temp_status)

            playerModifier = -1
            best = maximum
            for i in range (0,4):
                for j in range (0,3):
                    if temp_row_status2[i,j] == 0:
                        temp_row_status2[i,j] = 1
                        if i < 3 and j < 3:
                            temp_status2[i,j] = (abs(temp_status2[i,j]) + 1) * playerModifier
                        if i >= 1:
                            temp_status2[i-1,j] = (abs(temp_status2[i-1,j]) + 1) * playerModifier

                        if (i<3 and j<3 and temp_status2[i,j] == -4):
                            val = self.minimax2(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, False)
                            best = min(best,val)
                            beta = min(beta, best)

                        elif (i>=1 and temp_status2[i-1,j] == -4):
                            val = self.minimax2(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, False)
                            best = min(best,val)
                            beta = min(beta, best)
                        else:
                            val = self.minimax2(depth+1, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, True)
                            best = min(best,val)
                            beta = min(beta, best)
                        
                        temp_row_status2 = self.copy_row_status(temp_row_status)
                        temp_status2 = self.copy_board_status(temp_status)
                        
                        if beta<=alpha:
                            return best

            for i in range (0,3):
                for j in range (0,4):
                    if temp_col_status2[i,j] == 0:
                        temp_col_status2[i,j] = 1
                        if i < 3 and j < 3:
                            temp_status2[i][j] = (abs(temp_status2[i][j]) + 1) * playerModifier
                        if j>=1:
                            temp_status2[i][j-1] = (abs(temp_status2[i][j-1]) + 1) * playerModifier

                        if (i<3 and j<3 and temp_status2[i,j] == -4):
                            val = self.minimax2(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, False)
                            best = min(best,val)
                            beta = min(beta, best)

                        elif(j>=1 and temp_status2[i,j-1] == -4):
                            val = self.minimax2(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, False)
                            best = min(best,val)
                            beta = min(beta, best)

                        else:
                            val = self.minimax2(depth+1, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, True)
                            best = min(best,val)
                            beta = min(beta, best)
                        
                        temp_col_status2 = self.copy_col_status(temp_col_status)
                        temp_status2 = self.copy_board_status(temp_status)
                        
                        if beta<=alpha:
                            return best

            return best
                