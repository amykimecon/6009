# NO IMPORTS!

####################
## Problem 01
####################

def solve_latin_square(grid):

    def empty_cell(grid):
        for row in range(len(grid)):
            for cell in range(len(grid[row])):
                if grid[row][cell] == -1:
                    return (row,cell)
        return None

    def find_solutions(grid):
        n = len(grid)
        empty = empty_cell(grid)

        if empty == None:
            return []

        row = empty[0]
        col = empty[1]

        for num in range(1,n+1):
            valid = True
            for check in range(n):
                if grid[check][col] == num or grid[row][check] == num:
                    valid = False
            if valid:
                new_grid = grid[:]
                new_grid[row][col] = num
                if find_solutions(new_grid) != None:
                    print(new_grid)
                    return new_grid

        return None

    result = find_solutions(grid)
    if result == None:
        return False

    return result

grid = [
            [-1,  3, -1, -1, -1],
            [-1, -1,  1, -1, -1],
            [ 1, -1, -1,  4, -1],
            [ 2, -1, -1, -1, -1],
            [-1, -1,  4, -1,  5]
        ]

####################
## Problem 02
####################

def is_proper(root):
    # return number of black nodes on all paths if proper, else False
    def helper(root):
        if root == -1:
            return 0

        left = helper(root['left'])
        right = helper(root['right'])
        # print(root, left,right)
        if isinstance(left,int) and isinstance(right,int) and (left == right or (left in {1,0} and right in {1,0})):
            # print('good')
            if root['color'] == 'black':
                return left + 1
            return left
        else:
            return False

    if isinstance(helper(root),bool):
        return False
    return True


####################################################
## Problem 03. Prairie Dog Housing Lottery
####################################################

# Please implement the function lottery(prairie_dogs, capacities), which assigns
# prairie dogs to available burrows.  Not all prairie dogs are willing to live
# in all burrows; they have idiosyncratic individual preferences.  Furthermore,
# each borrow can only fit so many prairie dogs.  The first input value is a
# list with one element per prairie dog, where each element is itself a list of
# numbers, each number standing for an available burrow.  The second input value
# is a list giving burrow capacities.  Indices in this list correspond to
# numbers from the prairie-dog-preference lists.
#
# If an assignment exists from prairie dogs to burrows, satisfying everyone's
# preferences, then return that assignment, as a list of numbers, following
# the same order as the original list.  If no satisfactory assignment exists,
# return None.
def lottery(prairie_dogs, capacities):
    def helper(prefs, caps):
        if len(prefs) == 0:
            return []
        for burrow in prefs[0]:
            if caps[burrow] > 0:
                new_caps = caps[:]
                new_caps[burrow] -= 1
                next_assignment = helper(prefs[1:],new_caps)
                if next_assignment != None:
                    return [burrow] + next_assignment

        return None
    return helper(prairie_dogs, capacities)



####################################################
## Problem 04. Advanced Forestry
####################################################

def one_node_tree(data):
    return {"data": data, "left": None, "right": None, "prev": None, "next": None}

def print_tree(tree):
    def tweak_indent(indent):
        if indent == "":
            return "|_"
        else:
            return "  " + indent

    def print_tree_indented(prefix, tree, indent):
        if tree == None:
            return

        print(indent + prefix + " " + str(tree["data"]))
        if tree["prev"]:
            print(indent + "Prev: " + str(tree["prev"]["data"]))
        if tree["next"]:
            print(indent + "Next: " + str(tree["next"]["data"]))

        print_tree_indented("Left:", tree["left"], tweak_indent(indent))
        print_tree_indented("Right:", tree["right"], tweak_indent(indent))

    print_tree_indented("Root:", tree, "")

# Given a tree of the kind explained in the readme, modify it to add the new
# data value.
def insert(tree, data):
    raise NotImplementedError


####################
## Problem 05
####################

def solve_magicsquare_recursive(grid, magic_sum, choices):
    # return True if square is still solvable
    raise NotImplementedError


####################
## Problem 06
####################

# The code determines if a graph can be colored using two colors or not.
# Return {} if the graph cannot be colored.
# Return coloring_dict if the graph can be colored,
# where the coloring_dict maps vertices in the graph to 'Red' or 'Blue'.
def alternating_colors(graph, start):
    raise NotImplementedError


####################
## Problem 07
####################

# Given a binary tree, check if it is a Binary Search Tree (BST).
# In a BST, for every vertex, the value of the vertex is greater than the
# value of any vertex in its left subtree, and less than the value of any
# vertex in its right subtree.
# return True or False depending on whether tree is a BST or not.
def check_BST(btree, start):
    raise NotImplementedError


####################
## Problem 08
####################

# return minimum number of pipes of length stock_length
# that can be cut to satisfy the list of requested pipe_lengths
def pipe_cutting(requests,stock_length):
    raise NotImplementedError
