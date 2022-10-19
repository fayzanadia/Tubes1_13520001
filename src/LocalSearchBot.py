from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import random
import numpy as np

class LocalSearchBot(Bot): 
    def __init__(self, is_player1: bool):
        self.is_player1 = is_player1 # True jika bot adalah player 1
    
    def get_action(self, state: GameState) -> GameAction:
        all_row_marked = np.all(state.row_status == 1)
        all_col_marked = np.all(state.col_status == 1)

        if not (all_row_marked or all_col_marked):
            return self.get_random_action(state)
#        else:
#            return self.get_random_row_action(state)

    def get_random_action(self, poss_act: list) -> GameAction:
        position = random.randrange(0, len(poss_act))
        y, x = poss_act[position]
        return GameAction
        '''
        all_row_marked = np.all(state.row_status == 1)
        all_col_marked = np.all(state.col_status == 1)
        row_coord = self.get_row_neighbours(state)
        col_coord = self.get_col_neighbours(strate)
        
        if not (all_row_marked or all_col_marked):
            if random.random() < 0.5:
                return self.get_random_row_action(row_coord)
            else:
                return self.get_random_col_action(col_coord)
        elif all_row_marked:
            return self.get_random_col_action(col_coord)
        else:
            return self.get_random_row_action(row_coord)
'''
'''

    def get_random_row_action(self, row_coord: list) -> GameAction:
        position = random.randrange(0, len(row_coord))
        y, x = row_coord[position]
        return GameAction("row", (y, x))


    def get_random_col_action(self, col_coord: list) -> GameAction:
        position = random.randrange(0, len(col_coord))
        y, x = col_coord[position]
        return GameAction("col", (y, x))
    
    def get_row_neighbours(self, state: GameState):   
        row_neighbours = []     # nanti isinya list of tuples koordinat row yg bisa dipilih
        [ny, nx] = state.row_status.shape
        for i in range(ny):       
            for j in range(nx):
                if (state.row_status[i,j] == 0):
                    neighbour = (i,j)
                    row_neighbours.append(neighbour)       
        return row_neighbours
    
    def get_col_neighbours(self, state: GameState):   
        col_neighbours = []     # nanti isinya list of tuples koordinat col yg bisa dipilih
        [ny, nx] = state.col_status.shape
        for i in range(ny):       
            for j in range(nx):
                if (state.col_status[i,j] == 0):
                    neighbour = (i,j)
                    col_neighbours.append(neighbour)     
        return col_neighbours
 '''

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
        
        return new_state, point_scored

    def get_next_random_state(self, state: GameState):
        
        return GameState
    
    # Fungsi Count Box (All Marked)
    def count_box(self, state: GameState):
        count = 0
        player1 = self.is_player1
        ny = len(state.board_status[0]) 
        nx = len(state.board_status)        

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

        ny = len(state.board_status[0]) 
        nx = len(state.board_status)        

        for i in range(ny):
            for j in range(nx):
                if (state.board_status[i, j] == 3):
                    count += 1 
        
        return count

    # Fungsi Value Calculation
    # +2 / every box created
    # -1 / every three marked line created per box
    def calculate_value(self, state: GameState, next_state: GameState):
        value = 0
        
        count_box_current = self.count_box(state)
        count_box_next = self.count_box(next_state)
        count_box_next_almost = self.count_box_almost(next_state)

        if (count_box_next > count_box_current):
            value += 2 * (count_box_next - count_box_current)
        
        value -= count_box_next_almost

        return value
 
    def get_best_neighbour(self, state: GameState, row_neighbours: list, col_neighbours: list):
        possible_actions = self.get_possible_actions(state)
        possible_states = []

        for i in range(len(possible_actions)):
            possible_states.append(self.get_state_from_action(state, possible_actions[i]))
        

        # Data Structure = array[possible_action, score]
        possible_values = []
        for i in range(len(possible_states)):
            value = self.calculate_value(state, possible_states[i])
            possible_values.append(tuple(possible_actions[i], value))


        return GameState, int
    
    def local_search(self, state: GameState):
        row_neighbours = self.get_row_neighbours(state)
        col_neighbours = self.get_col_neighbours(state)
        best_neighbour, best_neighbour_value = self.get_best_neighbour(state, row_neighbours, col_neighbours)
        return best_neighbour, best_neighbour_value

    # Fungsi Empty Box Side
    # Returns an array of box side status in the order of (Top, Left, Right, Bottom)
    # True if empty and false if marked
    def empty_box_side(self, state: GameState, y: int, x: int):
        if (state.board_status[y, x] == 4) or (state.board_status[y, x] == -4):
            return [False, False, False, False]
        else:
            top_status, left_status, right_status, bottom_status = True
            if (state.col_status[y, x] == 1):
                top_status = False
            if (state.col_status[y + 1, x] == 1):
                bottom_status = False
            if (state.row_status[y, x] == 1):
                left_status = False
            if (state.row_status[y, x + 1] == 1):
                right_status = False
            return [top_status, left_status, right_status, bottom_status]


    # Fungsi Count Marked
    # Returns numbers of marked side in one box
    def count_marked(self, box_side):
        count = 0
        for i in range(len(box_side)):
            if (box_side[i] == False):
                count += 1
        return count


    # Fungsi Adjacent Boxes
    # Returns true if two boxes are adjacent
    def is_adjacent(self, state: GameState, y1, x1, y2, x2):
        box_side_1 = self.empty_box_side(state, y1, x1)
        box_side_2 = self.empty_box_side(state, y2, x2)

        count_marked_1 = self.count_marked(box_side_1)
        count_marked_2 = self.count_marked(box_side_2)

        if (count_marked_1 >= 2) and (count_marked_2 >= 2):
            # One row
            if (y1 == y2) and ((x1 - x2 == 1) or (x1 - x2 == -1)):
                if ((x1 < x2) and (state.col_status[x2] == 0)) or ((x1 > x2) and (state.col_status[x1] == 0)):
                    return True
            # One col
            if (x1 == x2) and ((y1 - y2 == 1) or (y1 - y2 == -1)):
                if ((y1 < y2) and (state.row_status[y2] == 0)) or ((y1 > y2) and (state.row_status[y1] == 0)):
                    return True
        else:
            return False