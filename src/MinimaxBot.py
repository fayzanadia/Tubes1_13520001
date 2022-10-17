from re import L
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from time import time

class MinimaxBot(Bot):
    def __init__(self, is_player1: bool):
        self.is_player1 = is_player1 # True jika bot adalah player 1

    def get_action(self, state: GameState) -> GameAction:
        is_maximize = False
        if (self.is_player1):
            is_maximize = True
        return self.minimax(state, is_maximize, -9999, 9999, True)[1]

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
        
        if (self.is_player1):
            return p1_total_boxes - p2_total_boxes
        else:
            return p2_total_boxes - p1_total_boxes

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
        
        if ((new_state.player1_turn and point_scored) or (not(new_state.player1_turn) and not(point_scored))):
            return new_state._replace(player1_turn = True)
        else:
            return new_state._replace(player1_turn = False)


    def minimax(self, state: GameState, is_maximize: bool, alpha: int, beta: int, first_call: bool, start_time: int = 0):
        # fungsi algoritma minimax, mengembalikan aksi terbaik yang dapat dilakukan

        if (first_call):
            start_time = time()

        if (self.terminal_test(state) or time() - start_time > 5):
            # print(time() - start_time)
            return self.utility_function(state), None 

        
        if (is_maximize):
            best_action = None
            best_value = -9999
            for action in (self.get_possible_actions(state)):
                v = self.minimax(self.get_state_from_action(state, action), False, alpha, beta, False, start_time)[0]
                best_value = max(v, best_value)
                if (best_value == v):
                    best_action = action
                alpha = max(alpha, v)
                if (beta <= alpha):
                    break
            print("Best Value: ", best_value)
            print("Best Action: ", best_action, "\n")
            return best_value, best_action
        else:
            worst_action = None
            worst_value = 9999
            for action in (self.get_possible_actions(state)):
                v = self.minimax(self.get_state_from_action(state, action), True, alpha, beta, False, start_time)[0]
                worst_value = min(v, worst_value)
                if (worst_value == v):
                    best_action = action
                beta = min(beta, v)
                if (beta <= alpha):
                    break
            print("Worst Value: ", worst_value)
            print("Worst Action: ", best_action, "\n")
            return worst_value, worst_action