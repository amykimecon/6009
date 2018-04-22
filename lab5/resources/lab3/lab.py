"""6.009 Lab 3 -- Six Double-Oh Mines"""

import unittest
import importlib, importlib.util
# NO ADDITIONAL IMPORTS ALLOWED!

## CODE FOR MINES IMPLEMENTATION

def dump(game):
    """Print a human-readable representation of game.

    Arguments:
       game (dict): Game state


    >>> dump({'dimensions': [1, 2], 'mask': [[False, False]], 'board': [['.', 1]], 'state': 'ongoing'})
    dimensions: [1, 2]
    board: ['.', 1]
    mask:  [False, False]
    state: ongoing
    """
    lines = ["dimensions: %s" % (game["dimensions"], ),
             "board: %s" % ("\n       ".join(map(str, game["board"])), ),
             "mask:  %s" % ("\n       ".join(map(str, game["mask"])), ),
             "state: %s" % (game["state"], ),
             ]
    print("\n".join(lines))


def create_board(num_rows,num_cols,func,bombs=[]):
    ''' Helper function to create board by iterating through rows and columns,
        values are initialized using func

        Returns board initialized according to functions

        Takes in number of rows and columns, a function that should take in
            three parameters (row, col, bombs), and a list of bombs (optional)
    '''

    board = []
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            row.append(func(r,c,bombs))
        board.append(row)
    return board

def iterate_neighbors(row,col,dims):
    '''For a given cell, iterates through nine surrounding squares and
        returns a list of all cells that are valid cells (e.g. within board)

    Takes in row number, column number, and dimensions of board (in list)

    Dimensions are passed in in the form [num_rows, num_cols]
    '''
    valid_coords = []
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if 0 <= r < dims[0] and 0 <= c < dims[1]:
                valid_coords.append([r,c])
    return valid_coords

def get_gamestate(game):
    '''Returns the game state in the form (bombs, covered_squares)

    Parameters:
        game (dictionary): game state dictionary
    '''
    bombs = 0 #number of VISIBLE bombs on board
    covered_squares = 0 #number of COVERED non-bombs on board
    rows = game["dimensions"][0]
    cols = game["dimensions"][1]
    for r in range(rows):
        for c in range(cols):
            if game["board"][r][c] == ".": #If square is a bomb
                if  game["mask"][r][c] == True: #If square is uncovered (Basically if bomb is showing)
                    bombs += 1
            elif game["mask"][r][c] == False: #If square is not a bomb and is covered (Basically if non-bomb is covered)
                covered_squares += 1
    return (bombs, covered_squares)

def new_game(num_rows, num_cols, bombs):
    """Start a new game.

    Return a game state dictionary, with the "dimensions", "state", "board" and
    "mask" fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which can be
                     either tuples or lists

    Returns:
       A game state dictionary

    >>> dump(new_game(2, 4, [(0, 0), (1, 0), (1, 1)]))
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, False, False, False]
           [False, False, False, False]
    state: ongoing
    """
    #MOD: changes bombs into list of lists (no tuples)
    for i in range(len(bombs)):
        bombs[i] = list(bombs[i])

    board = create_board(num_rows,num_cols,lambda r, c, b: '.' if [r,c] in b else 0,bombs)
    mask = create_board(num_rows,num_cols,lambda r, c, b: False)

    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == 0:
                neighbor_bombs = 0
                #Calls a function to return list of all neighbors around [r,c] that are on the game board
                for [i,j] in iterate_neighbors(r,c,[num_rows,num_cols]):
                    if board[i][j] == '.':
                        neighbor_bombs += 1
                board[r][c] = neighbor_bombs

    return {"dimensions": [num_rows, num_cols], "board" : board, "mask" : mask, "state": "ongoing"}

def reveal_squares(game, row, col):
    """Helper function: recursively reveal squares on the board, and return
    the number of squares that were revealed."""

    rows = game["dimensions"][0]
    cols = game["dimensions"][1]

    if game["board"][row][col] != 0:
        if game["mask"][row][col]:
            return 0
        else:
            game["mask"][row][col] = True
            return 1
    else:
        if game["board"][row][col] != 0: #If square hasn't been revealed and square has surrounding bomb
            game["mask"][row][col] = True
            return 1
        else:
            revealed = set()
            for [r,c] in iterate_neighbors(row,col,[rows,cols]):
                if game["board"][r][c] != '.' and not game["mask"][r][c] == True:
                    game["mask"][r][c] = True
                    revealed.add((r, c))
            total = len(revealed)
            for (r,c) in revealed:
                if game["board"][r][c] != "." :
                    total += reveal_squares(game, r, c)
            return total

def dig(game, row, col):
    """Recursively dig up (row, col) and neighboring squares.

    Update game["mask"] to reveal (row, col); then recursively reveal (dig up)
    its neighbors, as long as (row, col) does not contain and is not adjacent
    to a bomb.  Return an integer indicating how many new squares were
    revealed.

    The state of the game should be changed to "defeat" when at least one bomb
    is visible on the board after digging (i.e. game["mask"][bomb_location] ==
    True), "victory" when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and "ongoing" otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         "state": "ongoing"}
    >>> dig(game, 0, 3)
    4
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, True, True, True]
           [False, False, True, True]
    state: victory

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         "state": "ongoing"}
    >>> dig(game, 0, 0)
    1
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [True, True, False, False]
           [False, False, False, False]
    state: defeat
    """
    state = game["state"]
    if state=="defeat" or state=="victory":
        return 0

    gamestate = get_gamestate(game)
    bombs = gamestate[0]
    covered_squares = gamestate[1]

    if bombs != 0: #Checks if current state of game is defeat (if there are open bombs)
        game["state"] = "defeat"
        return 0

    if covered_squares == 0: #Checks if current state of game is victory
        game["state"] = "victory"
        return 0

    #If you've clicked on a bomb, reveals square, sets game state to defeat, and returns 1
    if game["board"][row][col] == '.':
        game["mask"][row][col] = True
        game["state"] = "defeat"
        return 1

    revealed = reveal_squares(game, row, col)
    gamestate = get_gamestate(game)
    bombs = gamestate[0]
    covered_squares = gamestate[1]
    bad_squares = bombs + covered_squares

    if bad_squares > 0:
        game["state"] = "ongoing"
        return revealed

    else:
        game["state"] = "victory"
        return revealed

def render(game, xray=False):
    """Prepare a game for display.

    Returns a two-dimensional array (list of lists) of "_" (hidden squares), "."
    (bombs), " " (empty squares), or "1", "2", etc. (squares neighboring bombs).
    game["mask"] indicates which squares should be visible.  If xray is True (the
    default is False), game["mask"] is ignored and all cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A 2D array (list of lists)

    >>> render({"dimensions": [2, 4],
    ...         "state": "ongoing",
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render({"dimensions": [2, 4],
    ...         "state": "ongoing",
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    rendered = []
    for r in range(game['dimensions'][0]):
        row = []
        for c in range(game['dimensions'][1]):
            if xray or game['mask'][r][c]: #Checks if all tiles are being revealed (xray) or if specific tile is not masked
                boardnum = game['board'][r][c]
                if boardnum == 0:
                    row.append(" ")
                else:
                    row.append(str(boardnum))
            else:
                row.append('_')
        rendered.append(row)
    return rendered

def render_ascii(game, xray=False):
    """Render a game as ASCII art.

    Returns a string-based representation of argument "game".  Each tile of the
    game board should be rendered as in the function "render(game)".

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A string-based representation of game

    >>> print(render_ascii({"dimensions": [2, 4],
    ...                     "state": "ongoing",
    ...                     "board": [[".", 3, 1, 0],
    ...                               [".", ".", 1, 0]],
    ...                     "mask":  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    rendered = render(game, xray)
    result = ""
    for row in rendered:
        for tile in row:
            result += tile
        result += "\n"
    return result[0:-1]

# board = [[1,".",1,0,1,1,1],[1,1,1,1,2,".",1],[0,0,0,1,".",2,1]]
# mask = [[True,False,False,True,True,True,True],[False,True,True,True,True,False,True],[True,True,True,True,False,True,True]]
# game = {"dimensions": [3, 7], "board" : board, "mask" : mask, "state": "ongoing"}
# print(game)
# dig(game,0,1)
# print(game)

## CODE FOR BUG HUNT / TESTING

class TestMinesImplementation(unittest.TestCase):
    """
    This class defines testing methods for each of the behaviors described in
    the lab handout.  In the methods below, self.test_mines will be the module
    you are testing.  For example, to call the "dig" function from the
    implementation being tested, you can use:

        self.test_mines.dig(game, r, c)

    You are welcome to use your methods from above as a "gold standard" to
    compare against, or to manually construct test cases, or a mix of both.
    """

    def test_newgame_dimensions(self):
        """
        Tests that the dimensions of the game are initialized correctly.
        """
        game = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])
        result_dims = [len(game['board']),len(game['board'][0])]
        self.assertEqual(result_dims,[3,7])

    def test_newgame_board(self):
        """
        Tests that the board is initialized correctly.
        """
        game = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])
        board = [[1,".",1,0,1,1,1],[1,1,1,1,2,".",1],[0,0,0,1,".",2,1]]
        self.assertEqual(game["board"],board)

    def test_newgame_mask(self):
        """
        Tests that the mask is initialized correctly (so that, if used with a
        working implementation of the dig function, it would behave as expected
        in all cases.
        """
        game = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])
        mask = [[False,False,False,False,False,False,False],[False,False,False,False,False,False,False],[False,False,False,False,False,False,False]]
        self.assertEqual(game["mask"],mask)

    def test_newgame_state(self):
        """
        Tests that the state of a new game is always "ongoing".
        """
        game = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])
        self.assertEqual(game["state"],"ongoing")

    def test_dig_mask(self):
        """
        Tests that, in situations that should modify the game, dig affects the
        mask, and not the board.  (NOTE that this should not test for the
        correctness of dig overall, just that it modifies mask and does not
        modify board.)
        """
        game = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])
        self.test_mines.dig(game,2,2)
        result_board = [[1,".",1,0,1,1,1],[1,1,1,1,2,".",1],[0,0,0,1,".",2,1]]
        self.assertEqual(game["board"],result_board)

    def test_dig_reveal(self):
        """
        Tests that dig reveals the square that was dug.
        """
        game = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])
        game2 = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])

        self.test_mines.dig(game2,0,0)

        self.assertFalse(game["mask"][0][0])
        self.assertTrue(game2["mask"][0][0])

    def test_dig_neighbors(self):
        """
        Tests that dig properly reveals other squares when appropriate (if a 0
        is revealed during digging, all of its neighbors should automatically
        be revealed as well).
        """
        mask = [[False,False,False,False,False,False,False],[True,True,True,True,False,False,False],[True,True,True,True,False,False,False]]
        game = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])
        self.test_mines.dig(game,2,0)
        self.assertEqual(game["mask"],mask)

    def test_completed_dig_nop(self):
        """
        Tests that dig does nothing when performed on a game that is not
        ongoing.
        """
        game_const = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])
        game_won = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])
        game_lost = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])

        game_won["state"] = "victory"
        game_lost["state"] = "defeat"

        self.assertEqual(game_const["mask"],game_won["mask"])
        self.assertEqual(game_const["mask"],game_lost["mask"])

    def test_multiple_dig_nop(self):
        """
        Tests that dig does nothing when performed on a square that has already
        been dug.
        """
        game = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])
        game2 = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])

        game["mask"][0][0]=True
        game2["mask"][0][0]=True

        dig(game,0,0)

        for key in game.keys():
            self.assertEqual(game2[key], game[key])

    def test_dig_count(self):
        """
        Tests that dig returns the number of squares that were revealed (NOTE
        this that should always report the number that were revealed, even if
        that is different from the number that should have been revealed).
        """
        game = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])
        self.test_mines.dig(game,1,0)
        visible = 0
        for row in game["mask"]:
            for item in row:
                if item:
                    visible += 1
        revealed = self.test_mines.dig(game,2,2)
        visible2 = 0
        for row in game["mask"]:
            for item in row:
                if item:
                    visible2 += 1
        self.assertEqual(visible2,visible+revealed)

    def test_defeat_state(self):
        """
        Tests that the game state switches to "defeat" when a mine is dug, and
        not in other situations.
        """
        game = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])
        self.test_mines.dig(game,0,1)

        game2 = self.test_mines.new_game(3,7,[[1,5],[2,4],(0,1)])
        self.test_mines.dig(game2,0,0)

        self.assertEqual(game["state"],"defeat")
        self.assertNotEqual(game2["state"],"defeat")

    def test_victory_state(self):
        """
        Tests that the game state switches to "victory" when there are no more
        safe squares to dig, and not in other situations.
        """
        game = self.test_mines.new_game(3,7,[[2,6],(0,1)])
        self.test_mines.dig(game,2,2)
        self.test_mines.dig(game,0,0)
        self.test_mines.dig(game,0,5)
        self.test_mines.dig(game,0,6)
        self.test_mines.dig(game,1,6)

        game2 = self.test_mines.new_game(3,7,[[2,6],(0,1)])
        self.test_mines.dig(game,2,1)

        self.assertEqual(game["state"],"victory")
        self.assertNotEqual(game2["state"],"victory")

class TestResult6009(unittest.TestResult):
    """ Extend unittest framework for this 6.009 lab """
    def __init__(self, *args, **kwargs):
        """ Keep track of test successes, in addition to failures and errors """
        self.successes = []
        super().__init__(*args, **kwargs)

    def addSuccess(self, test):
        """ If a test succeeds, add it to successes """
        self.successes.append((test,))

    def results_dict(self):
        """ Report out names of tests that succeeded as 'correct', and those that
        either failed (e.g., a self.assert failure) or had an error (e.g., an uncaught
        exception during the test) as 'incorrect'.
        """
        return {'correct': [test[0]._testMethodName for test in self.successes],
                'incorrect': [test[0]._testMethodName for test in self.errors + self.failures]}


def run_implementation_tests(imp):
    """Test whether an implementation of the mines game correctly implements
    all the desired behaviors.

    Returns a dictionary with two keys: 'correct' and 'incorrect'.  'correct'
    maps to a list containing the string names of the behaviors that were
    implemented correctly (as given in the readme); and 'incorrect' maps to a
    list containing the string descriptions of the behaviors that were
    implemented incorrectly.

    Parameters:
        imp: a string containing the name of the module to be tested.

    Returns:
       A dictionary mapping strings to sequences.
    """
    spec = importlib.util.spec_from_file_location(imp.split('/')[-1].rsplit('.', 1)[0], imp)
    mines_imp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mines_imp)
    TestMinesImplementation.test_mines = mines_imp
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestMinesImplementation)
    res = unittest.TextTestRunner(resultclass=TestResult6009,verbosity=3).run(suite).results_dict()
    return {'correct': [tag[5:] for tag in res['correct']],
            'incorrect': [tag[5:] for tag in res['incorrect']]}


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    doctest.testmod()

    # Test of my unit tests (on my own lab.py). Helpful to debug the
    # unit tests themselves.

    #print(run_implementation_tests('lab.py'))
    import resources.mines1 as test_mines
    TestMinesImplementation.test_mines = test_mines
    res = unittest.main(verbosity=3, exit=False)

    # Test of resources/mines* with my implementation tests. Helpful
    # to detect bugs in those mines* implementations.
    # for fname in ["mines1", "mines2", "mines3", "mines4"]:
    #     res = run_implementation_tests('resources/%s.py' % fname)
    #     print("\nTESTED", fname)
    #     print(" correct:", res['correct'])
    #     print(" incorrect:", res['incorrect'])
