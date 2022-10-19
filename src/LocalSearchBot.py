from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import random
import numpy as np

class LocalSearchBot(Bot): 
    def __init__(self, is_player1: bool):
        self.is_player1 = is_player1 # True jika bot adalah player 1
    
    
    def get_action(self, state: GameState) -> GameAction:
        return self.local_search(state)


    def get_possible_actions(self, state: GameState):
        # fungsi untuk menghasilkan aksi-aksi yang mungkin dari state masukan
        [ny, nx] = state.board_status.shape
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

        [ny, nx] = state.board_status.shape
        x, y = action.position

        if new_state.player1_turn:
            player_modifier = -1
        else:
            player_modifier = 1
            
        if (y < ny) and (x < nx):
            new_state.board_status[y,x] = (abs(new_state.board_status[y,x]) + 1) * player_modifier

        if (action.action_type == 'row'):
            new_state.row_status[y,x] = 1
            if y >= 1:
                new_state.board_status[y-1,x] = (abs(new_state.board_status[y-1,x]) + 1) * player_modifier

        elif (action.action_type == 'col'):
            new_state.col_status[y,x] = 1
            if x >= 1:
                new_state.board_status[y,x-1] = (abs(new_state.board_status[y,x-1]) + 1) * player_modifier
        
        return new_state
    
    
    # Fungsi Count Box (All Marked)
    def count_box(self, state: GameState):
        count = 0
        player1 = self.is_player1
        [ny, nx] = state.board_status.shape     

        for i in range(ny):
            for j in range(nx):
                if (player1):
                   if (state.board_status[i,j] == -4):
                       count += 1
                else:
                   if (state.board_status[i,j] == 4):
                       count += 1
        
        return count


    # Fungsi Count Box (Three Marked)
    def count_box_almost(self, state: GameState):
        count = 0
        [ny, nx] = state.board_status.shape       

        for i in range(ny):
            for j in range(nx):
                if (state.board_status[i, j] == 3) or (state.board_status[i, j] == -3):
                    count += 1 
        
        return count


    def count_box_almost_bool(self, state: GameState):
        [ny, nx] = state.board_status.shape       

        for i in range(ny):
            for j in range(nx):
                if (state.board_status[i, j] == 3) or (state.board_status[i, j] == -3):
                    return True
        
        return False


    # Fungsi Count Box (Else Marked)
    def count_box_else(self, state: GameState):
        count = 0
        [ny, nx] = state.board_status.shape       

        for i in range(ny):
            for j in range(nx):
                if (state.board_status[i, j] != 3) or (state.board_status[i, j] != 4) or (state.board_status[i, j] != -3) or (state.board_status[i, j] != -4):
                    count += 1 
        
        return count


    # Fungsi Value Calculation
    # +2 / every box created
    # -1 / every three marked line created per box
    def calculate_value(self, state: GameState):
        value = 0
        
        count_box_current = self.count_box(state)
        count_box_current_else = self.count_box_else(state)
        count_box_current_almost = self.count_box_almost(state)

        value += 3 * (count_box_current)
        value += 2 * (count_box_current_else)
        value += 1 * (count_box_current_almost)

        return value


    def local_search(self, state: GameState) -> GameAction:
        possible_actions = self.get_possible_actions(state)
        possible_states = []

        for i in range(len(possible_actions)):
            possible_states.append(self.get_state_from_action(state, possible_actions[i]))
        
        value = self.count_box(state)
        idx_poss_state = []
        idx_poss_val = []
        idx_box_almost = []

        for i in range(len(possible_states)):
            next_value = self.count_box(possible_states[i])
            is_almost = self.count_box_almost_bool(possible_states[i])
            if (next_value >= value):
                if (is_almost):
                    idx_box_almost.append(i)
                idx_poss_state.append(i)
                idx_poss_val.append(next_value)

        is_all_almost = True
        for i in range(len(idx_poss_state)):
            if (idx_poss_state[i] not in idx_box_almost):
                is_all_almost = False

        max_val = max(idx_poss_val)
        max_val_list = []

        if (is_all_almost):
            for i in range(len(idx_poss_state)):
                if (idx_poss_val[i] == max_val):
                    max_val_list.append(idx_poss_state[i])
            if (len(max_val_list) > 1):                
                idx_action = random.choice(max_val_list)
            else:
                idx_action = max_val_list[0]
            return possible_actions[idx_action]
        else:
            for i in range(len(idx_poss_state)):
                if (idx_poss_val[i] == max_val and idx_poss_state[i] not in idx_box_almost):
                    max_val_list.append(idx_poss_state[i])
            if (len(max_val_list) > 1):                
                idx_action = random.choice(max_val_list)
            else:
                idx_action = max_val_list[0]
            return possible_actions[idx_action]