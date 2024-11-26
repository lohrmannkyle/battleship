import sys

SHIP_SIZES = { "A":5, "B":4, "S":3, "D":3, "P":2 } 

class GridPos:
    """ 
    Represents a grid square on the game board. 
    Each grid squares has an x and a y value, can store a ship, 
    and tracks if it has been guessed already
    """
    def __init__(self, x, y):
        """
        Constructor
        Parameters: x(int) -> x coord
                    y(int) -> y coord
        """
        self._x = x
        self._y = y
        self._ship = None
        self._guessed = False

    def guessed(self):
        """ Getter for guessed attribute """
        return self._guessed
    
    def mark_guessed(self):
        """ Sets guessed atrribute to True """
        self._guessed = True
    
    def ship(self):
        """ Getter for ship attribute """
        return self._ship
    
    def add_ship(self, ship):
        """
        Updates ship attribute for gridpos ship param if not already set
        Parameters: ship(Ship) -> ship to set on gridpos
        Return: Bool -> False if a ship already exists, else True
        """
        if self._ship == None:
            self._ship = ship
            return True
        return False
    
    def __str__(self):
        """ str method for aiding in printing board """
        if self._ship is None:
            return "[{},{}]".format(self._x, self._y) 
        else:
            "[{}]".format(self._ship.get_type() * 3)
    
class Board:
    """
    Represents the game board which is always a (10x10) grid.
    Contains a dictionary of each ship that exists on the board.
    Tracks if more than one of a ship type exists and if so exits the program.
    """
    def __init__(self):
        """ contructor for board, no params """
        self._board = []
        self._ships = {}
        self._duplicate = False
        self.gen_board()

    def duplicate(self):
        """ getter for duplicate """
        return self._duplicate

    def ships(self):
        """ getting for ships on board """
        return self._ships
    
    def gen_board(self):
        """ Called in constructor and creates playing board """
        for i in range(10):
            row = []
            for j in range(10):
                row.append(GridPos(i,j))
            self._board.append(row)

    def get_board(self):
        """ getter for board """
        return self._board
        
    def __str__(self):
        """ str method to allow for printing of board """
        string = ""
        for i in range (9, -1, -1):
            for j in range(10):
                string += str(self._board[j][i])
            string += "\n"
        return string
    
    def get_gridpos(self, x, y):
        """ getter for grippos at (x,y) """
        return self._board[x][y]
    
    def valid_guess(self, x, y):
        """ returns True if guess is within bounds of board, else False """
        return (x < 10 and x > -1) and (y < 10 and y > -1)
    
    def game_over(self):
        """ returns True if ships dict is empty, else False """
        return len(self._ships) == 0
    
    def guess(self, x, y):
        """
        Called for each guess in guess_file. 
        Calls helper functions to keep track of prviously guessed squares.
        After each guess checks for gameover or ship sunk condition.
        Parameters: x(int) -> x value to check at
                    y(int) -> y value to check at
        """
        if not self.valid_guess(x, y):
            print("illegal guess")
            return 

        gridpos = self.get_gridpos(x,y)
        ship = gridpos.ship()
        if ship:
            ship.hit(gridpos.guessed())
            if ship.sunk():
                self._ships.pop(ship.get_type())
                print("{} sunk".format(ship))
            
            if self.game_over():
                print("all ships sunk: game over") 
                sys.exit(0)
        else:
            string = "miss"
            if gridpos.guessed():
                string += " (again)"
            print(string)
            
        if not gridpos.guessed():
            gridpos.mark_guessed()

    def add_ship_to_grid(self, ship, x, y):
        """ 
        Updates the ship for the gridsquare at (i,j) 
            by calling the gridsquare function
        Parameters: ship (Ship) -> ship to set 
                    x(int) -> x int of gridpos
                    y(int) -> y int of gridpos    
        """
        return self.get_gridpos(x,y).add_ship(ship)
    
    def add_ship_to_ships(self, ship):
        """
        Adds pased in ship to ships dict and checks if the type of ship
            already exists on the board
        Parameters: ship (Ship) -> ship to add to ships dict
        """
        if ship.get_type() in self.ships().keys():
            self._duplicate = True

        self._ships[ship.get_type()] = ship


class Ship:
    """
    Represents the ship objects on the board. Proper ship size for each type
        is stored in the global SHIP_SIZES dict. When a ship is placed the
        the length of the occupies list which stores tuples of each coordinate
        the ship exists on is checked against the proper ship size. If they
        don't match the program exits. Game must start with 5 unique ships.
    """
    def __init__(self, type):
        """
        Constructor for Ship. Only takes a type parmaters and sets the size
            using the SHIP_SIZE global dict.
        """
        self._type = type
        self._size = SHIP_SIZES[type]
        self._occupies = []
        self._remaining = self._size
    
    def hit(self, guessed):
        """
        Only called if a valid guess is made on a square that contains a ship.
        Decrements lives of ship.
        Parameters: guessed (Bool) -> used to check if the guess has 
            already been made for printing purposes
        """
        string = "hit"
        if guessed:
            string += " (again)"
        else:
            self._remaining -= 1

        if self._remaining != 0:
            print(string)

    def get_type(self):
        """ getter for type """
        return self._type
    
    def sunk(self):
        """ returns True if no remaining lives, else False """
        return self._remaining == 0

    def place(self, start_x, stop_x, start_y, stop_y, board_obj, line):
        """
        Places each ship on the board.
        If start values is greater than stop value they get swapped.
        Ensures ships are placed vertically/horizontally and do not overlap.

        Parameters: start_x  (int)     -> starting x coord of ship
                    stop_x   (int)     -> ending x coord of ship
                    start_y  (int)     -> starting y coord of ship
                    stop_y   (int)     -> ending y coord of ship
                    board_obj(Board)   -> board to place ship on
                    line     (str)     -> printed if error
        """

        start_x, stop_x = min(start_x, stop_x), max(start_x, stop_x)
        start_y, stop_y = min(start_y, stop_y), max(start_y, stop_y)

        if stop_x == start_x:
            for i in range(start_y, stop_y + 1):
                self._occupies.append(start_x,i)
                board_obj.add_ship_to_grid(self, start_x, i)

        elif start_y == stop_y:
            for i in range(start_x, stop_x + 1):
                self._occupies.append(i ,start_y)
                overlap = not board_obj.add_ship_to_grid(self, i, start_y)
                if overlap:
                    print("ERROR: overlapping ship: " + line)
                    sys.exit(0)  
        else:
            print("ERROR: ship not horizontal or vertical: " + line)
            sys.exit(0)

        board_obj.add_ship_to_ships(self)

    def __str__(self):
        """ str method that uses the ship._type to represent the ship """
        return "{}".format(self.get_type())

def gen_board(placement_file):
    """
    Parses the placement file and generates the board. 
    Ensures ships are the proper size and placed within bounds of board.
    Parameters: placement_file(File) -> file to parse
    Returns:    board (Board)        -> board with ships placed
    """
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
    """
    Parses guess file and checks each guess for a hit/miss
    Parameters: guess_file (File) -> guess file to process
                board (Board)     -> board to check guesses against
    """
    for line in guess_file:
        line = line.split()
        x, y = int(line[0]), int(line[1])

        board.guess(x, y)

def main():
    placement_file = open(input())
    guess_file = open(input())
    board = gen_board(placement_file)

    if len(board.ships().keys()) != 5 or board.duplicate():
        print("ERROR: fleet composition incorrect")
        sys.exit(0)

    process_guesses(guess_file, board)

main()
