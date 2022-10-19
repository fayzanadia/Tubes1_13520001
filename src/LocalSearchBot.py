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
                    neighbour = state.row_status[i,j]
                    row_neighbours.append(neighbour)
                    
        return row_neighbours
    
    
    def get_col_neighbours(self, state: GameState):
        #all_col_not_marked = np.all(state.col_status == 0)     
        col_neighbours = []     # nanti isinya list of tuples koordinat col yg bisa dipilih
 
        [ny, nx] = state.col_status.shape
        
        for i in range(ny):       
            for j in range(nx):
                if (state.col_status[i,j] == 0):
                    neighbour = state.col_status[i,j]
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
