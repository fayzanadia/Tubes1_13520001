from re import L
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import numpy as np

class MinimaxBot(Bot):
    def get_action(self, state: GameState) -> GameAction:

        a = self.minimax(state, True, -9999, 9999)
        print(a)
        return None # TO DO: return action yg akan dilakukan

    def utility_function(self, state: GameState) -> int:
        # fungsi utilitas: jumlah box player 1 - jumlah box player 2

        ny = len(state.board_status[0]) # jumlah kotak dalam satu baris
        nx = len(state.board_status) # jumlah kotak dalam satu kolom matriks
    
        p1_total_boxes = 0
        p2_total_boxes = 0

        for y in range(ny):
            for x in range(nx):
                if (state.board_status[y,x] == -4): # box milik player 1
                    p1_total_boxes += 1
                elif (state.board_status[y,x] == 4): # box milik player 2
                    p2_total_boxes += 1
        
        return p1_total_boxes - p2_total_boxes

    def terminal_test(self, state: GameState) -> bool:
        # fungsi untuk mengecek apakah state sudah terminal

        ny = len(state.board_status[0]) # jumlah kotak dalam satu baris
        nx = len(state.board_status) # jumlah kotak dalam satu kolom matriks

        for y in range(ny):
            for x in range(nx):
                if (abs(state.board_status[y,x]) != 4):
                    return False
        return True

    def get_possible_actions(self, state: GameState):
        # fungsi untuk menghasilkan aksi-aksi yang mungkin dari state masukan

        ny = len(state.board_status[0]) # jumlah kotak dalam satu baris
        nx = len(state.board_status) # jumlah kotak dalam satu kolom matriks

        possible_actions = []
        empty_rows = [(x, y) for y in range(ny + 1) for x in range(nx) if state.row_status[y,x] == 0]
        for row in empty_rows:
            possible_actions.insert(len(possible_actions), GameAction("row", row))
        
        empty_cols = [(x, y) for y in range(ny) for x in range(nx + 1) if state.col_status[y,x] == 0]
        for col in empty_cols:
            possible_actions.insert(len(possible_actions), GameAction("col", col))

        return possible_actions

    def get_state_from_action(self, state: GameState, action: GameAction) -> GameState:
        # fungsi untuk menghasilkan state dari sebuah aksi yang dilakukan
        # berdasarkan fungsi update_board dari main.py
        
        new_state = GameState(state.board_status.copy(), state.row_status.copy(), state.col_status.copy(), state.player1_turn) # copy dari current game state

        point_scored = False

        ny = len(state.board_status[0]) # jumlah kotak dalam satu baris
        nx = len(state.board_status) # jumlah kotak dalam satu kolom matriks
        x, y = action.position

        if new_state.player1_turn:
            player_modifier = -1
        else:
            player_modifier = 1
            
        if (y < ny) and (x < nx):
            new_state.board_status[y,x] = (abs(new_state.board_status[y,x]) + 1) * player_modifier
            if abs(new_state.board_status[y,x]) == 4:
                point_scored = True

        if (action.action_type == 'row'):
            new_state.row_status[y,x] = 1
            if y >= 1:
                new_state.board_status[y-1,x] = (abs(new_state.board_status[y-1,x]) + 1) * player_modifier
                if abs(new_state.board_status[y-1,x]) == 4:
                    point_scored = True

        elif (action.action_type == 'col'):
            new_state.col_status[y,x] = 1
            if x >= 1:
                new_state.board_status[y,x-1] = (abs(new_state.board_status[y,x-1]) + 1) * player_modifier
                if abs(new_state.board_status[y,x-1]) == 4:
                    point_scored = True
        
        if (not(point_scored)):
            new_state.player1_turn = False

        return new_state

    def minimax(self, state: GameState, is_maximize: bool, alpha: int, beta: int, depth: int = 0):
        # fungsi algoritma minimax, mengembalikan aksi terbaik yang dapat dilakukan

        # TO DO: dapatkan action terbaik sehingga yg direturn bukan nilainya tapi action-nya

        # start_time = time()

        # if (time() - start_time > 5):
        #     return self.get_possible_actions(state)[0]
        # print("DEPTH: ", depth)

        if (self.terminal_test(state)):
            return self.utility_function(state) # TO DO: jadiin return action

        if (is_maximize):
            v = -9999
            for action in (self.get_possible_actions(state)):
                v = max(v, self.minimax(self.get_state_from_action(state, action), False, alpha, beta, depth + 1))
                alpha = max(alpha, v)
                if (beta <= alpha):
                    break
            return v # TO DO: jadiin return action
        else:
            v = 9999
            for action in (self.get_possible_actions(state)):
                v = min(v, self.minimax(self.get_state_from_action(state, action), True, alpha, beta, depth + 1))
                beta = min(beta, v)
                if (beta <= alpha):
                    break
            return v # TO DO: jadiin return action