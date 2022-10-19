from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import random
import numpy as np
import time

class MinimaxBot(Bot):
    def get_action(self, state: GameState) -> GameAction:
        all_row_marked = np.all(state.row_status == 1)
        all_col_marked = np.all(state.col_status == 1)
        all_marked = all_row_marked and all_col_marked

        if not all_marked:
            return self.get_move(0,-999,999,state,True)

    def evaluate(self, matrix: np.ndarray):
        score = 0
        for i in range (0,3):
            for j in range (0,3):
                if matrix[i,j] == 4:
                   score += 1
                elif matrix[i,j] == -4:
                    score -= 1
        
        return score 

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

    def get_move(self, depth, alpha, beta, state:GameState, playerModifier)->GameAction:
        
        playerModifier = 1
        
        temp_status = self.copy_board_status(state.board_status)
        temp_row_status = self.copy_row_status(state.row_status)
        temp_col_status = self.copy_col_status(state.col_status)    

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
        start = time.time()
        for i in range (0,4):
            for j in range (0,3):
                if temp_row_status[i,j] == 0:
                    temp_row_status[i,j] = 1
                    if i < 3 and j < 3:
                        temp_status[i,j] = (abs(temp_status[i,j]) + 1) * playerModifier
                    if i >= 1:
                        temp_status[i-1,j] = (abs(temp_status[i-1,j]) + 1) * playerModifier

                    if (i<3 and j<3 and temp_status[i,j] == 4):
                        val = self.minimax(depth, alpha, beta, temp_row_status, temp_col_status, temp_status, True, start)
                        random_score = random.randrange(0,9)
                        if val>score:
                            score = val
                            action_result = GameAction("row", (j,i))
                        elif (val>=score and random_score >= 5):
                            score = val
                            action_result = GameAction("row", (j,i))
                        

                    elif(i>=1 and temp_status[i-1,j] == 4):
                        val = self.minimax(depth, alpha, beta, temp_row_status, temp_col_status, temp_status, True, start)
                        random_score = random.randrange(0,9)
                        if val>score:
                            score = val
                            action_result = GameAction("row", (j,i))
                        elif (val>=score and random_score >= 5):
                            score = val
                            action_result = GameAction("row", (j,i))

                    else:
                        val = self.minimax(depth+1, alpha, beta, temp_row_status, temp_col_status, temp_status, False, start)
                        random_score = random.randrange(0,9)
                        if val>score:
                            score = val
                            action_result = GameAction("row", (j,i))
                        elif (val>=score and random_score >= 5):
                            score = val
                            action_result = GameAction("row", (j,i))
                
                end = time.time()
                if end-start >= 4.9:
                    print("waktu gerakan: " + str("{:.2f}".format(end-start)))
                    return action_result

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
                        val = self.minimax(depth, alpha, beta, temp_row_status, temp_col_status, temp_status, True, start)
                        random_score = random.randrange(0,20)
                        if val>score:
                            score = val
                            action_result = GameAction("col", (j,i))
                        elif (val>=score and random_score == 18):
                            score = val
                            action_result = GameAction("col", (j,i))

                    elif(j>=1 and temp_status[i,j-1] == 4):
                        val = self.minimax(depth, alpha, beta, temp_row_status, temp_col_status, temp_status, True, start)
                        random_score = random.randrange(0,20)
                        if val>score:
                            score = val
                            action_result = GameAction("col", (j,i))
                        elif (val>=score and random_score == 18):
                            score = val
                            action_result = GameAction("col", (j,i))
                    else:
                        val = self.minimax(depth+1, alpha, beta, temp_row_status, temp_col_status, temp_status, False, start)
                        random_score = random.randrange(0,20)
                        if val>score:
                            score = val
                            action_result = GameAction("col", (j,i))
                        elif (val>=score and random_score == 18):
                            score = val
                            action_result = GameAction("col", (j,i))
                
                end = time.time()
                if end-start >= 4.9:
                    print("waktu gerakan: " + str("{:.2f}".format(end-start)))
                    return action_result
                
                temp_row_status = self.copy_row_status(state.row_status)
                temp_col_status = self.copy_col_status(state.col_status)
                temp_status = self.copy_board_status(state.board_status)

        end = time.time()
        print("waktu gerakan: " + str("{:.2f}".format(end-start)))

        return action_result

    def minimax (self, depth, alpha, beta, temp_row_status, temp_col_status, temp_status, maximizingPlayer, start):
        maximum = 999
        minimum = -999
        current_time = time.time()

        if (current_time-start >= 4.9):
            return -999

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
                            val = self.minimax(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, True, start)
                            best = max(best,val)
                            alpha = max(alpha, best)

                        elif(i>=1 and temp_status2[i-1,j] == 4):
                            val = self.minimax(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, True, start)
                            best = max(best,val)
                            alpha = max(alpha, best)

                        else:
                            val = self.minimax(depth+1, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, False, start)
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
                            val = self.minimax(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, True, start)
                            best = max(best,val)
                            alpha = max(alpha, best)

                        elif(j>=1 and temp_status2[i,j-1] == 4):
                            val = self.minimax(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, True, start)
                            best = max(best,val)
                            alpha = max(alpha, best)

                        else:
                            val = self.minimax(depth+1, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, False, start)
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
                            val = self.minimax(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, False, start)
                            best = min(best,val)
                            beta = min(beta, best)

                        elif (i>=1 and temp_status2[i-1,j] == -4):
                            val = self.minimax(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, False, start)
                            best = min(best,val)
                            beta = min(beta, best)
                        else:
                            val = self.minimax(depth+1, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, True, start)
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
                            val = self.minimax(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, False, start)
                            best = min(best,val)
                            beta = min(beta, best)

                        elif(j>=1 and temp_status2[i,j-1] == -4):
                            val = self.minimax(depth, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, False, start)
                            best = min(best,val)
                            beta = min(beta, best)

                        else:
                            val = self.minimax(depth+1, alpha, beta, temp_row_status2, temp_col_status2, temp_status2, True, start)
                            best = min(best,val)
                            beta = min(beta, best)
                        
                        temp_col_status2 = self.copy_col_status(temp_col_status)
                        temp_status2 = self.copy_board_status(temp_status)
                        
                        if beta<=alpha:
                            return best

            return best