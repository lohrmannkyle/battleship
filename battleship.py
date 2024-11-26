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
        if self._ship == None:
            self._ship = ship
            return True
        return False
    
    def __str__(self):
        return "[{},{}]".format(self._x, self._y) if self._ship is None else "[{}]".format(self._ship.get_type() * 3)
    
class Board:
    def __init__(self):
        self._board = []
        self._ships = {}
        self._duplicate = False
        self.gen_board()

    def duplicate(self):
        return self._duplicate

    def ships(self):
        return self._ships
    
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
                string += str(self._board[j][i])
            string += "\n"
        return string
    
    def get_gridpos(self, x, y):
        return self._board[x][y]
    
    def valid_guess(self, x, y):
        return (x < 10 and x > -1) and (y < 10 and y > -1)
    
    def game_over(self):
        return len(self._ships) == 0
    
    def guess(self, x, y):
        """
        Checks to see if a ship exists on the guessed gridsquare. 
        """
        if not self.valid_guess(x, y):
            print("illegal guess")
            return 

        gridpos = self.get_gridpos(x,y)
        ship = gridpos.ship()
        if ship and not gridpos.guessed():
            ship.hit(x,y)
            gridpos.mark_guessed()
            if ship.sunk():
                self._ships.pop(ship.get_type())
                print("{} sunk".format(ship))
            
            if self.game_over():
                print("all ships sunk: game over") 
                sys.exit(0)
        else:
            print("miss")
        return False
    
    def add_ship_to_grid(self, ship, i, j):
        return self.get_gridpos(i,j).add_ship(ship)
    
    def add_ship_to_ships(self, ship):
        if ship.get_type() in self.ships().keys():
            self._duplicate = True

        self._ships[ship.get_type()] = ship



class Ship:
    def __init__(self, type):
        self._type = type
        self._size = SHIP_SIZES[type]
        self._occupies = []
        self._remaining = self._size
    
    def hit(self, x, y):
        self._remaining -= 1
        print("hit")

    def get_type(self):
        return self._type
    
    def sunk(self):
        return self._remaining == 0

    def place(self, start_x, stop_x, start_y, stop_y, board_obj, line):

        start_x, stop_x = min(start_x, stop_x), max(start_x, stop_x)
        start_y, stop_y = min(start_y, stop_y), max(start_y, stop_y)

        if stop_x == start_x:
            for i in range(start_y, stop_y + 1):
                self._occupies.append([start_x,i])
                board_obj.add_ship_to_grid(self, start_x, i)

        elif start_y == stop_y:
            for i in range(start_x, stop_x + 1):
                self._occupies.append([i ,start_y])
                overlap = not board_obj.add_ship_to_grid(self, i, start_y)
                if overlap:
                    print("ERROR: overlapping ship: " + line)
                    sys.exit(0)  
        else:
            "ERROR: ship not horizontal or vertical: " + line
            sys.exit(0)

        board_obj.add_ship_to_ships(self)

    def __str__(self):
        return "{}".format(self.get_type())

def gen_board(placement_file):
    board = Board()
    for line in placement_file:
        split = line.split()
        type = split[0]
        start_x, stop_x = int(split[1]) ,int(split[3])
        start_y, stop_y = int(split[2]), int(split[4])

        if max(start_x, stop_x, start_y, stop_y) > 9 or \
            min(start_x, stop_x, start_y, stop_y) < 0:
            print("ERROR: ship out-of-bounds: " + line)
            sys.exit(0)


        ship = Ship(type)        
        ship.place(start_x, stop_x, start_y, stop_y, board, line)

        if len(ship._occupies) != SHIP_SIZES[ship.get_type()]:
            print("ERROR: incorrect ship size: " + line)
            sys.exit(0)

    return board

def process_guesses(guess_file, board):
    for line in guess_file:
        line = line.split()
        x, y = int(line[0]), int(line[1])

        board.guess(x, y)




def main():

    # placement_file = open("test/example-placement.txt")
    # guess_file = open("test/example-guess.txt")
    # board = gen_board(placement_file)
    placement_file = open(input())
    guess_file = open(input())
    board = gen_board(placement_file)

    if len(board.ships().keys()) != 5 or board.duplicate():
        print("ERROR: fleet composition incorrect")
        sys.exit(0)

    # print(board)
    # print(board._ships)

    process_guesses(guess_file, board)

main()
