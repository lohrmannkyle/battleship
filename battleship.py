import sys

SHIP_SIZES = { "A":5, "B":4, "S":3, "D":3, "P":2 } 

class GridPos:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._ship = None
        self._guessed = False

    def guessed(self):
        return self._guessed
    
    def mark_guessed(self):
        self._guessed = True
    
    def ship(self):
        return self._ship
    
    def add_ship(self, ship):
        self._ship = ship
    
    def __str__(self):
        return "[{},{}]".format(self._x, self._y) if self._ship is None else "[{}]".format(self._ship.get_type() * 3)
    
class Board:
    def __init__(self):
        self._board = []
        self.gen_board()
        self._ships = []
    
    def gen_board(self):
        for i in range(10):
            row = []
            for j in range(10):
                row.append(GridPos(i,j))
            self._board.append(row)

    def get_board(self):
        return self._board
        
    def __str__(self):
        string = ""
        for i in range (9, -1, -1):
            for j in range(10):
                string += str(self._board[i][j])
            string += "\n"
        return string
    
    def get_gridpos(self, x, y):
        return self._board[x][y]
    
    def valid_guess(x, y):
        return (x < 10 and x > -1) and (y < 10 and y > -1)
    
    def guess(self, x, y):
        """
        Checks to see if a ship exists on the guessed gridsquare. 
        """
        gridpos = self.get_gridpos(x,y)
        ship = gridpos.ship()
        if ship and not ship.guessed:
            ship.hit(x,y)
            gridpos.mark_guessed()
            return True
        return False
    
    def add_ship(self, gridpos, ship):
        self._ships[gridpos] = ship

class Ship:
    def __init__(self, type):
        self._type = type
        self._size = SHIP_SIZES[type]
        self._occupies = []
        self._remaining = None
    
    def hit(self, x, y):
        self._remaining.remove((x,y))

    def get_type(self):
        return self._type

    def occupies(self, start_x, stop_x, start_y, stop_y, board_obj):
        if stop_x == start_x:
            for i in range(start_y, stop_y + 1):
                self._occupies.append([start_x,i])
                board_obj.get_board()[start_x][i].add_ship(self)

        if start_y == stop_y:
            for i in range(start_x, stop_x + 1):
                self._occupies.append([i ,start_x])
                board_obj.get_board()[i][start_x].add_ship(self)

def parse_file(self, file, board):
    for line in file:
        line = line.split()
        type = line[0]
        start_x, stop_x = line[2] ,line[4]
        start_y, stop_y = line[1], line[3]

        ship = Ship(type)



def main():
    board = Board()
    # file = open(input())
    print(board)
    ship = Ship("B")
    ship.occupies(4, 8, 5, 5,board)
    print(board)

main()
