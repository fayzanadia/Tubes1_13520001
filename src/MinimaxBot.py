from Bot import Bot
from GameAction import GameAction
from GameState import GameState

class MinimaxBot(Bot):
    def utility_function(self, state: GameState) -> int:
        # fungsi utilitas: jumlah box player 1 - jumlah box player 2

        ny = len(state.board_status[0]) # panjang matriks
        nx = len(state.board_status) # lebar matriks
    
        p1_total_boxes = 0
        p2_total_boxes = 0

        for y in range(ny):
            for x in range(nx):
                if (state.board_status[y,x] == -4): # box milik player 1
                    p1_total_boxes += 1
                elif (state.board_status[y,x] == 4): # box milik player 2
                    p2_total_boxes += 1
        
        return p1_total_boxes - p2_total_boxes