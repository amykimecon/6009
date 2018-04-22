"""6.009 Lab 4 -- HyperMines"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS

class HyperMinesGame:
    def __init__(self, dims, bombs):
        """Start a new game.

        This method should properly initialize the "board", "mask",
        "dimensions", and "state" attributes.

        Args:
           dims (list): Dimensions of the board
           bombs (list): Bomb locations as a list of lists, each an
                         N-dimensional coordinate

        >>> g = HyperMinesGame([2, 4, 2], [[0, 0, 1], [1, 0, 0], [1, 1, 1]])
        >>> g.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, False], [False, False], [False, False], [False, False]]
               [[False, False], [False, False], [False, False], [False, False]]
        state: ongoing
        """
        self.dimensions = dims
        self.mask = self.create_board(dims,False)
        self.state = "ongoing"

        self.board = self.create_board(self.dimensions,0) #Creates board with dimensions according to dims, with values initialized to 0
        for bomb in bombs:
            self.set_val(self.board,bomb,".") #Alters value of squares at bomb locations to '.'

        for bomb in bombs:
            for neighbor in self.neighbors(bomb,self.dimensions): #Alters value of neighbors of each bomb
                val = self.check_val(self.board, neighbor)
                if val != ".":
                    self.set_val(self.board, neighbor, val + 1)

    def dump(self):
        """Print a human-readable representation of this game."""
        lines = ["dimensions: %s" % (self.dimensions, ),
                 "board: %s" % ("\n       ".join(map(str, self.board)), ),
                 "mask:  %s" % ("\n       ".join(map(str, self.mask)), ),
                 "state: %s" % (self.state, )]
        print("\n".join(lines))

    def reveal_squares(self, coord):
        """Helper function, reveals all squares branching from coord, and returns number of squares revealed.

            Args:
                coord (list): list containing coordinates of initial square to be revealed
        >>> g = HyperMinesGame.from_dict({"dimensions": [6,4],
        ...            "board": [[1,1,1,0],[1,'.',1,0],[1,1,1,0],[1,1,0,0],['.',1,0,0],[1,1,0,0]],
        ...            "mask": [[False,False,True,False],[False,False,False,False],[False,False,False,False],[True,False,False,False],[False,False,False,False],[False,False,False,False]],
        ...            "state": "ongoing"})
        >>> g.reveal_squares([3,3])
        15
        """
        if self.check_val(self.board,coord) != 0: #If value of coord is not 0
            if self.check_val(self.mask,coord): #Check if square has already been opened
                return 0
            else:
                self.set_val(self.mask, coord, True) #Set square mask to True, return 1
                return 1

        revealed = []
        for neighbor in self.neighbors(coord,self.dimensions): #Opens each valid neighbor that is not a bomb and has not already been opened, adds to revealed
            if self.check_val(self.board,neighbor) != '.' and not self.check_val(self.mask, neighbor):
                self.set_val(self.mask, neighbor, True)
                revealed.append(neighbor)
        total = len(revealed)
        for revealed_square in revealed:
            total += self.reveal_squares(revealed_square) #Recursively reveals squares around each square that has been revealed
        return total

    def dig(self, coords):
        """Recursively dig up square at coords and neighboring squares.

        Update the mask to reveal square at coords; then recursively reveal its
        neighbors, as long as coords does not contain and is not adjacent to a
        bomb.  Return a number indicating how many squares were revealed.  No
        action should be taken and 0 returned if the incoming state of the game
        is not "ongoing".

        The updated state is "defeat" when at least one bomb is visible on the
        board after digging, "victory" when all safe squares (squares that do
        not contain a bomb) and no bombs are visible, and "ongoing" otherwise.

        Args:
           coords (list): Where to start digging

        Returns:
           int: number of squares revealed

        >>> g = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
        ...                  [[False, False], [False, False], [False, False], [False, False]]],
        ...         "state": "ongoing"})
        >>> g.dig([0, 3, 0])
        8
        >>> g.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, False], [False, True], [True, True], [True, True]]
               [[False, False], [False, False], [True, True], [True, True]]
        state: ongoing
        >>> g = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
        ...                  [[False, False], [False, False], [False, False], [False, False]]],
        ...         "state": "ongoing"})
        >>> g.dig([0, 0, 1])
        1
        >>> g.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, True], [False, True], [False, False], [False, False]]
               [[False, False], [False, False], [False, False], [False, False]]
        state: defeat
        """
        if self.state != "ongoing": #If gamestate is defeat or victory, doesn't dig
            return 0

        if self.check_val(self.board,coords) == '.': #If clicked square is a bomb, game over
            self.set_val(self.mask,coords,True)
            self.state = "defeat"
            return 1

        revealed_squares = self.reveal_squares(coords) #Reveals squares

        if self.is_victory(): #Checks if game is in victory state
            self.state = "victory"

        return revealed_squares

    def render(self, xray=False):
        """Prepare the game for display.

        Returns an N-dimensional array (nested lists) of "_" (hidden squares),
        "." (bombs), " " (empty squares), or "1", "2", etc. (squares
        neighboring bombs).  The mask indicates which squares should be
        visible.  If xray is True (the default is False), the mask is ignored
        and all cells are shown.

        Args:
           xray (bool): Whether to reveal all tiles or just the ones allowed by
                        the mask

        Returns:
           An n-dimensional array (nested lists)

        >>> g = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...            "mask": [[[False, False], [False, True], [True, True], [True, True]],
        ...                     [[False, False], [False, False], [True, True], [True, True]]],
        ...            "state": "ongoing"})
        >>> g.render(False)
        [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
         [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

        >>> g.render(True)
        [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
         [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
        """
        display_board = self.create_board(self.dimensions,'_') #Creates new 'render board'
        for coord in self.get_all_coords(self.dimensions):
            if xray or self.check_val(self.mask,coord): #If square should be revealed (xray == True or mask == True)
                boardnum = self.check_val(self.board,coord) #Gets value of square
                if boardnum == 0: #If value is 0, sets display to " "
                    display_board = self.set_val(display_board,coord," ")
                else: #Otherwise, displays string representation of tile
                    display_board = self.set_val(display_board,coord,str(boardnum))
        return display_board


    @classmethod
    def from_dict(cls, d):
        """Create a new instance of the class with attributes initialized to
        match those in the given dictionary."""
        game = cls.__new__(cls)
        for i in ('dimensions', 'board', 'state', 'mask'):
            setattr(game, i, d[i])
        return game

    ### Helper Functions ###
    def create_board(self, dims, elem):
        """Creates a new board.

        This method recursively creates an n-dimensional board according to dims,
        and initializes each element to value elem.

        Args:
            dims (list): Dimensions of the board
            elem: Value to initialize every element

        >>> g = HyperMinesGame([6,4],[[1,1],[4,0]])
        >>> g.dump()
        dimensions: [6, 4]
        board: [1, 1, 1, 0]
                [1, '.', 1, 0]
                [1, 1, 1, 0]
                [1, 1, 0, 0]
                ['.', 1, 0, 0]
                [1, 1, 0, 0]
        mask:  [False, False, False, False]
                [False, False, False, False]
                [False, False, False, False]
                [False, False, False, False]
                [False, False, False, False]
                [False, False, False, False]
        state: ongoing
        """
        if len(dims) == 0: #Base case: if dimensions has length zero, just return default element
            return elem
        #Otherwise, creates new list (representing list level of current dimension)
        dim = []
        for dim2 in range(dims[0]): #Creates as many lists as current dimension
            dim.append(self.create_board(dims[1:],elem)) #Within this list, create lists of next dimensions
        return dim

    def set_val(self, board, coord, item):
        """Places an item at specified coordinate and returns the altered board

        This method places any element at the coordinate specified by variable bomb on the board.

        Args:
            board (array): n-dimensional Game board
            coord (list): n-dimensional coordinate representing location of item
            item: whatever item to be placed at coord

        >>> g = HyperMinesGame.from_dict({"dimensions": [6,4],
        ...            "board": [[1,1,1,0],[1,'.',1,0],[1,1,1,0],[1,1,0,0],['.',1,0,0],[1,1,0,0]],
        ...            "mask": [[False,False,True,False],[False,False,False,False],[False,False,False,False],[True,False,False,False],[False,False,False,False],[False,False,False,False]],
        ...            "state": "ongoing"})
        >>> g.set_val(g.mask,[3,2],True)
        [[False, False, True, False], [False, False, False, False], [False, False, False, False], [True, False, True, False], [False, False, False, False], [False, False, False, False]]
        """
        if len(coord) == 0: #Base case: if coord is empty, return the item to be set
            return item

        #Otherwise, set current dimension of board to set_val(next dimension of board)
        board[coord[0]] = self.set_val(board[coord[0]],coord[1:],item)
        return board

    def check_val(self,board, coord):
        """Returns value at coord.

        Args:
            board (array): n-dimensional game board
            coord (list): n-dimensional coordinate of which to retrieve value

        >>> g = HyperMinesGame.from_dict({"dimensions": [6,4],
        ...            "board": [[1,1,1,0],[1,'.',1,0],[1,1,1,0],[1,1,0,0],['.',1,0,0],[1,1,0,0]],
        ...            "mask": [[False,False,True,False],[False,False,False,False],[False,False,False,False],[True,False,False,False],[False,False,False,False],[False,False,False,False]],
        ...            "state": "ongoing"})
        >>> g.check_val(g.board,[3,0])
        1
        >>> g.check_val(g.mask,[3,0])
        True
        """
        if len(coord) == 1: #Base case: if coord has one dimension, get that value on board
            return board[coord[0]]
        #Otherwise, call check_val on next dimension of board
        return self.check_val(board[coord[0]],coord[1:])

    def neighbors(self,coord, dims):
        """Returns a list of valid neighbors of a given coordinate.

        Args:
            coord (list): n-dimensional coordinate of which to find neighbors
            dims (list): list of the dimensions of the game board

        >>> g = HyperMinesGame.from_dict({"dimensions": [6,4],
        ...            "board": [[1,1,1,0],[1,'.',1,0],[1,1,1,0],[1,1,0,0],['.',1,0,0],[1,1,0,0]],
        ...            "mask": [[False,False,True,False],[False,False,False,False],[False,False,False,False],[True,False,False,False],[False,False,False,False],[False,False,False,False]],
        ...            "state": "ongoing"})
        >>> g.neighbors([2,0],g.dimensions)
        [[1, 0], [1, 1], [2, 0], [2, 1], [3, 0], [3, 1]]
        """
        if len(coord)==1: #Base case: When we reach the FIRST coordinate, we return all valid neighbors
            return [x for x in range(coord[0]-1,coord[0]+2) if 0 <= x < dims[0]]

        #Otherwise, we create a list of neighbors
        neighbors_list = []
        for dim in self.neighbors(coord[:-1],dims[:-1]): #Recurses through coordinate in backwards order, adding neighbors
            for x in range(coord[-1]-1,coord[-1]+2):
                if 0 <= x < dims[-1]:
                    if type(dim)==int:
                        dim = [dim]
                    neighbors_list.append(dim+[x]) #Adds the new coordinate to the END of the existing coordinates
        return neighbors_list

    def get_all_coords(self, dims):
        """Returns a list of all valid coordinates in a game of given dimensions

        Args:
            dims (list): list of the dimensions of the game board

        >>> g = HyperMinesGame.from_dict({"dimensions": [6,4],
        ...            "board": [[1,1,1,0],[1,'.',1,0],[1,1,1,0],[1,1,0,0],['.',1,0,0],[1,1,0,0]],
        ...            "mask": [[False,False,True,False],[False,False,False,False],[False,False,False,False],[True,False,False,False],[False,False,False,False],[False,False,False,False]],
        ...            "state": "ongoing"})
        >>> g.get_all_coords(g.dimensions)
        [[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3], [2, 0], [2, 1], [2, 2], [2, 3], [3, 0], [3, 1], [3, 2], [3, 3], [4, 0], [4, 1], [4, 2], [4, 3], [5, 0], [5, 1], [5, 2], [5, 3]]
        """
        if len(dims)==1: #Base case: When we reach the FIRST coordinate, we return all valid neighbors
            return [x for x in range(dims[0])]

        #Otherwise, we create a list of coordinates
        coords_list = []
        for dim in self.get_all_coords(dims[:-1]): #Recurses through dimensions in backwards order
            for x in range(dims[-1]):
                if type(dim)==int:
                    dim = [dim]
                coords_list.append(dim+[x]) #Adds the new coordinate to the END of the existing coordinates
        return coords_list

    def is_victory(self):
        """ Returns state of current game object

            Returns True if game has been won, False otherwise

        >>> g = HyperMinesGame.from_dict({"dimensions": [6,4],
        ...            "board": [[1,1,1,0],[1,'.',1,0],[1,1,1,0],[1,1,0,0],['.',1,0,0],[1,1,0,0]],
        ...            "mask": [[False,False,True,False],[False,False,False,False],[False,False,False,False],[True,False,False,False],[False,False,False,False],[False,False,False,False]],
        ...            "state": "ongoing"})
        >>> g.is_victory()
        False

        >>> g2 = HyperMinesGame.from_dict({"dimensions": [6,4],
        ...            "board": [[1,1,1,0],[1,'.',1,0],[1,1,1,0],[1,1,0,0],['.',1,0,0],[1,1,0,0]],
        ...            "mask": [[True,True,True,True],[True,False,True,True],[True,True,True,True],[True,True,True,True],[False,True,True,True],[True,True,True,True]],
        ...            "state": "ongoing"})
        >>> g2.is_victory()
        True
        """
        for coord in self.get_all_coords(self.dimensions): #Checks all coordinates on board
            if self.check_val(self.board, coord) == '.' and self.check_val(self.mask, coord): #If uncovered bomb, return False
                return False
            if self.check_val(self.board, coord) != '.' and not self.check_val(self.mask, coord): #If covered non-bomb, return False
                return False
        return True

if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
