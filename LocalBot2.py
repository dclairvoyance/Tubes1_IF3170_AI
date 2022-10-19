from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import random
import numpy as np
from copy import deepcopy

class LocalBot2(Bot):
    def get_action(self, state: GameState) -> GameAction:
        all_row_marked = np.argwhere(state.row_status != 0)
        all_col_marked = np.argwhere(state.col_status != 0)

        # Saat masih pertama, bebas mau generate row atau col
        if (len(all_row_marked) + len(all_col_marked) <= 1):
            return self.get_random_action(state)
        else:
            return self.get_action_local_search(state)

    def objective_function(self, state: GameState):
        score = 0
        mult = -1 if state.player1_turn else 1
        
        for row in state.board_status:
            for status in row:
                if (status == 4*mult):
                    score += 20
                elif (abs(status) == 3):
                    score -= 10
                elif (abs(status) == 2):
                    score += 5
        
        print(score)
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

    def get_random_action(self, state: GameState) -> GameAction:
        all_row_marked = np.all(state.row_status != 0)
        all_col_marked = np.all(state.col_status != 0)

        # Mengambil random move
        if not (all_row_marked or all_col_marked):
            if random.random() < 0.5:
                return self.get_random_row_action(state)
            else:
                return self.get_random_col_action(state)
        elif all_row_marked:
            # Jika semua row terisi
            return self.get_random_col_action(state)
        else:
            # Jika semua column terisi
            return self.get_random_row_action(state)        

    def get_random_row_action(self, state: GameState) -> GameAction:
        position = self.get_random_position_with_zero_value(state.row_status)
        return GameAction("row", position)

    def get_random_col_action(self, state: GameState) -> GameAction:
        position = self.get_random_position_with_zero_value(state.col_status)
        return GameAction("col", position)

    def get_next_state(self, state : GameState, act : GameAction) -> GameState:
        state_copy = deepcopy(state)
        y = act.position[0]
        x = act.position[1]
        val = 1
        playerModifier = 1
        scored = False
        if state.player1_turn:
            playerModifier = -1

        if act.action_type == 'row':
            state_copy.row_status[y][x] = playerModifier
        else :
            state_copy.col_status[y][x] = playerModifier

        if y < 3 and x < 3:
            state_copy.board_status[y][x] = (abs(state_copy.board_status[y][x]) + val) * playerModifier
            if abs(state_copy.board_status[y][x]) == 4:
                scored = True

        if act.action_type == 'row':
            state_copy.row_status[y][x] = 1
            if y >= 1:
                state_copy.board_status[y-1][x] = (abs(state_copy.board_status[y-1][x]) + val) * playerModifier
                if abs(state_copy.board_status[y-1][x]) == 4:
                    scored = True
        elif act.action_type == 'col':
            state_copy.col_status[y][x] = 1
            if x >= 1:
                state_copy.board_status[y][x-1] = (abs(state_copy.board_status[y][x-1]) + val) * playerModifier
                if abs(state_copy.board_status[y][x-1]) == 4:
                    scored = True

        if scored :
            return state_copy
        else:
            return GameState(board_status=state_copy.board_status,row_status=state_copy.row_status,
                                    col_status=state_copy.col_status,player1_turn=not state_copy.player1_turn)#state_copy

    def get_action_local_search(self, state: GameState) -> GameAction:
        unmarked_row = np.argwhere(state.row_status == 0)
        unmarked_col = np.argwhere(state.col_status == 0)

        # Menyimpan koordinat i, j dari unmarked_row dan unmarked_col yang terbaik
        best_coord = [0, 0]
        best_move = "no_bestmove"

        best_f = self.objective_function(state)
        for x, y in unmarked_row:
            state_copy = self.get_next_state(state, GameAction('row', (x,y)))
            f = self.objective_function(state_copy)
            if (f >= best_f):
                best_f = f
                best_coord = [x, y]
                best_move = "row"

        for x, y in unmarked_col:
            state_copy = self.get_next_state(state, GameAction('col', (x,y)))
            f = self.objective_function(state_copy)
            if (f >= best_f):
                best_f = f
                best_coord = [x, y]
                best_move = "col"

        print(best_move, best_coord)
        if best_move == "no_bestmove":
            # Generate random move
            return self.get_random_action(state)

        return GameAction(best_move, [best_coord[1], best_coord[0]])