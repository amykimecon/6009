def test_recursion(dims,elem):
    if len(dims) == 0:
        return elem
    dim = []
    for dim2 in range(dims[0]):
        dim.append(test_recursion(dims[1:],elem))
    return dim


board = test_recursion([2,4,3],0)

def place_item(board, coord, item):
    """Places an item at specified coordinate and returns the altered board

    This method places any element at the coordinate specified by variable bomb on the board.

    Args:
        board (array): n-dimensional Game board
        coord (list): n-dimensional coordinate representing location of item
        item: whatever item to be placed at coord
    """
    if len(coord) == 0:
        return item
    board[coord[0]] = place_item(board[coord[0]],coord[1:],item)
    return board

def check_val(board,coord):
    if len(coord) == 1:
        return board[coord[0]]
    return check_val(board[coord[0]],coord[1:])

def neighbors(coord, dims):
    """Returns a list of valid neighbors of a given coordinate.

    Args:
        board (array): n-dimensional game board
        coord (list): n-dimensional coordinate of which to find neighbors
        dims (list): list of the dimensions of the game board
    """
    if len(coord)==1: #Base case: When we reach the FIRST coordinate, we return all valid neighbors
        return [x for x in range(coord[0]-1,coord[0]+2) if 0 <= x < dims[0]]

    #Otherwise, we create a list of
    neighbors_list = []
    for dim in neighbors(coord[:-1],dims[:-1]):
        for x in range(coord[-1]-1,coord[-1]+2):
            if 0 <= x < dims[-1]:
                if type(dim)==int:
                    dim = [dim]
                neighbors_list.append(dim+[x])
    return neighbors_list

def get_all_coords(dims):
    """Returns a list of all valid coordinates in a game of given dimensions

    Args:
        dims (list): list of the dimensions of the game board
    """
    if len(dims)==1: #Base case: When we reach the FIRST coordinate, we return all valid neighbors
        return [x for x in range(dims[0])]

    #Otherwise, we create a list of coordinates
    coords_list = []
    for dim in get_all_coords(dims[:-1]): #Recurses through dimensions in backwards order
        for x in range(dims[-1]):
            if type(dim)==int:
                dim = [dim]
            coords_list.append(dim+[x]) #Adds the new coordinate to the END of the existing coordinates
    return coords_list

print(get_all_coords([3,5,4]))
#print(get_elems([[[1, 0], 1], 0]))
