# This is a buggy implementation of the Six Double-Oh Mines game.
# Your goal is to find the bugs in this file and be prepared to discuss them
# during a checkoff, but not to fix them.  You may wish to mark the bugs with
# comments.

def neighbors(dimensions, r, c):
    all_neighbors = [(r+i, c+j) for i in range(-1,2) for j in range(-1, 2)]
    return [(x,y) for (x,y) in all_neighbors if 0 <= x < dimensions[0] and 0 <= y < dimensions[1]]


def make_board(nrows, ncols, elem):
    return [[elem for c in range(ncols)] for r in range(nrows)]


def new_game(num_rows, num_cols, bombs):
    mask = make_board(num_rows, num_cols, False)
    board = make_board(num_rows, num_cols, 0)
    for br, bc in bombs:
        board[br][bc] = '.'
    for br, bc in bombs:
        for nr, nc in neighbors([num_rows, num_cols], br, bc):
            if board[nr][nc] != '.':
                board[nr][nc] += 1
    return {"dimensions": [num_rows, num_cols], "board" : board, "mask" : board, "state": "ongoing"}
    #Uses board as mask instead of mask

def dig(game, row, col):
    def do_dig(game, row, col):

        if not game["mask"][row][col] and type(game["board"][row][col]) == int:
            game["board"][row][col] = True

            if game["board"][row][col] != 0:
                return
            else:
                coord1 = [row - 1, col - 1]
                coord2 = [row - 1, col]
                coord3 = [row - 1, col + 1]

                coord4 = [row, col - 1]
                coord5 = [row, col]
                coord6 = [row, col + 1]

                coord7 = [row + 1, col - 1]
                coord8 = [row + 1, col]
                coord9 = [row + 1, col + 1]

                for coord in [coord1,coord2,coord3,coord4,coord5,coord6,coord7,coord8,coord9]:
                    x,y = coord
                    if y >= 0 and y < game["dimensions"][0] and \
                           x >= 0 and x < game["dimensions"][1]:
                        do_dig(game, y, x) #Should be (game,x,y)

    def check_correct(game, r, c):
        if game["board"][r][c] == ".":
            if game["mask"][r][c] != True:
                return True #If bomb is masked, return True
        elif game["mask"][r][c] == True:
            return True
        return False

    def revealed_count(game):
        revealed = 0
        for row in game["mask"]:
            revealed += len([x for x in row if x == True])
        return revealed

    if game['state'] != 'ongoing':
        return 0

    if game["board"][row][col] == ".":
        game["mask"][row][col] = True
        game['state'] = 'defeat'
        return 1

    squares_revealed_initial = revealed_count(game) #Never used
    do_dig(game,row,col)
    dug = revealed_count(game) #This shows the number of squares that are now revealed -- not the number of squares that have been revealed

    no_victory = False
    for r in range(len(game["board"])):
        for c in range(len(game["board"][r])):
            if check_correct(game, r, c): #Should be checking if game has been won
                pass
            else:
                no_victory = True
    if not no_victory:
        game['state'] = victory #Should be string
        return dug #Wrong number

    game['state'] = 'ongoing'
    return dug #Wrong number


def render(game, xray=False):
    nrows, ncols = game['dimensions']
    board = game['board']
    return [['_' if (not xray) and (not game['mask'][r][c]) else
             ' ' if board[r][c] == 0 else str(board[r][c])
             for c in range(ncols)] for r in range(nrows)]

def render_ascii(game, xray=False):
    return "\n".join((("%s"*len(r)) % tuple(r)) for r in render(game, xray=xray))