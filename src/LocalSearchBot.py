from ast import Return
from Bot import Bot
from GameAction import GameAction
from GameState import GameState
import random
import numpy as np

class LocalSearchBot(Bot): 
    
    def get_action(self, state: GameState) -> GameAction:
        all_row_marked = np.all(state.row_status == 1)
        all_col_marked = np.all(state.col_status == 1)

        if not (all_row_marked or all_col_marked):
            return self.get_random_action(state)
#        else:
#            return self.get_random_row_action(state)

    def get_random_action(self, state: GameState) -> GameAction:
        all_row_marked = np.all(state.row_status == 1)
        all_col_marked = np.all(state.col_status == 1)

        if not (all_row_marked or all_col_marked):
            if random.random() < 0.5:
                return self.get_random_row_action(state)
            else:
                return self.get_random_col_action(state)
        elif all_row_marked:
            return self.get_random_col_action(state)
        else:
            return self.get_random_row_action(state)

    def get_random_row_action(self, state: GameState) -> GameAction:
        position = self.get_random_position_with_zero_value(state.row_status)
        return GameAction("row", position)

    def get_random_col_action(self, state: GameState) -> GameAction:
        position = self.get_random_position_with_zero_value(state.col_status)
        return GameAction("col", position)
        
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
 
    
    def get_row_neighbours(self, state: GameState):
        #all_row_not_marked = np.all(state.row_status == 0)     
        row_neighbours = []     # nanti isinya list of tuples koordinat row yg bisa dipilih
 
        [ny, nx] = state.row_status.shape
        
        for i in range(ny):       
            for j in range(nx):
                if (state.row_status[i,j] == 0):
                    neighbour = (i,j)
                    row_neighbours.append(neighbour)
                    
        return row_neighbours
    
    
    def get_col_neighbours(self, state: GameState):
        #all_col_not_marked = np.all(state.col_status == 0)     
        col_neighbours = []     # nanti isinya list of tuples koordinat col yg bisa dipilih
 
        [ny, nx] = state.col_status.shape
        
        for i in range(ny):       
            for j in range(nx):
                if (state.col_status[i,j] == 0):
                    neighbour = (i,j)
                    col_neighbours.append(neighbour)
                    
        return col_neighbours
 
    def get_next_random_state(self, state: GameState):
        return
    
    def calculate_value(self, state: GameState, curr_state: GameState):
        return
 
    def get_best_neighbour(self, state: GameState, curr_state: GameState, row_neighbours: list, col_neighbours: list):
        return
    
    def local_search(self, state: GameState):
        current_state = get_next_random_state(state)
        current_value = calculate_value(state, current_state)
        row_neighbours = get_row_neighbours(current_state)
        col_neighbours = get_col_neighbours(current_state)
        best_neighbour, best_neighbour_value = get_best_neighbour(state, current_state, row_neighbours, col_neighbours)
        
        while (best_neighbour_value >= current_value):
           current_state = best_neighbour
           current_value = best_neighbour_value
           row_neighbours = get_row_neighbours(current_state)
           col_neighbours = get_col_neighbours(current_state)
           best_neighbour, best_neighbour_value = get_best_neighbour(state, current_state, row_neighbours, col_neighbours)
        
        return current_state, current_value


    # Fungsi Heuristic
    # If state value tidak lebih besar dari current then randomize state
    
    # Fungsi Randomize State
    # Use only when semua state value sama aja

    # Fungsi State Value
    def count_value(self, state: GameState):
        # Priority:
        # 1. Long chain
        #    a. Even # of long chains = 1st player win
        #       Achievable by making side chain
        #    b. Odd # of long chains = 2nd player win
        #       Achievable by makin center chain (avoid side chain)
        # 2. 3 lines
        # 3. Empty box
        return

    # ############################
    # LONG CHAIN FUNCTION
    # ############################

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


    # Fungsi Long Chain Checker
    # Returns true if current box chain in the board is advantageous to player
    def is_box_chain(self, state: GameState):
        
        [ny, nx] = state.board_status.shape
        
        # Loop Checker
        count_box_checked = 0
        count_box_marked_3 = 0

        # for i in range(ny):
        #     for j in range(nx):
                


        # Final Checker
        if (count_box_checked > 2) and (count_box_marked_3 > 0):
            return True
        return False