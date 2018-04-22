# NO IMPORTS!

##############
# Problem 01 #
##############

def find_triple(ilist):
    """ If the list ilist contains three values x, y, and z such that x + y = z
        return a tuple with x and y. Otherwise return None. """
    for x in range(len(ilist)):
        for y in range(x+1,len(ilist)):
            if ilist[x]+ilist[y] in set(ilist):
                print(ilist[x],ilist[y])
                return (ilist[x],ilist[y])
    return None

##############
# Problem 02 #
##############

def is_quasidrome(s):
    """Check whether s is a quasidrome."""
    if is_palindrome(s):
        return True
    for i in range(len(s)):
        if is_palindrome(s[0:i]+s[i+1:len(s)]):
            return True
    return False

def is_palindrome(s):
    backwards_s = ""
    for letter in s:
        backwards_s = letter + backwards_s
    if backwards_s == s:
        return True
    return False

##############
# Problem 03 #
##############

def max_subsequence(ilist, is_circular = False):
    """ Return the start and end indices as a tuple of the maximum subsequence
        in the list.  If is_circular = True, imagine the list is circular.
        That is, after the end index comes the start index.  """
    if is_circular:
        ilist = ilist + ilist
    max_sum = 0
    max_start = 0
    max_end = 0
    current_sum = 0
    for i in range(len(ilist)):
        current_sum += ilist[i]
        if current_sum > max_sum:
            max_end = i
            max_sum = current_sum
        if current_sum < 0:
            current_sum = 0
            max_start = i + 1

    return (max_start,max_end)


##############
# Problem 04 #
##############

def count_triangles(edges):
    """Count the number of triangles in edges."""

    triangles = []
    for i in range(len(edges)):
        for j in range(i+1,len(edges)):
            for k1 in range(2): #Loops through two vertices in edges[i]
                for k2 in range(2): #Loops through two vertices in edges[j]
                    #Checking if the edges share a vertice and whether the other two vertices form an edge in the edges list
                    if edges[i][k1]==edges[j][k2] and ([edges[i][1-k1],edges[j][1-k2]] in edges or [edges[j][1-k2],edges[i][1-k1]] in edges):
                        already_in_triangles = False
                        #Checking if the triangle is already in the list of triangles
                        for triangle in triangles:
                            if edges[i][1-k1] in triangle and edges[i][k1] in triangle and edges[j][1-k2] in triangle:
                                already_in_triangles = True
                        if not already_in_triangles:
                            #Appending a list of coordinates to the triangles list
                            triangles.append([edges[i][1-k1],edges[i][k1],edges[j][1-k2]])
    return len(triangles)


##############
# Problem 05 #
##############

def is_unique( A ):
    """ return True if no repeated element in list A. """
    if len(set(A))==len(A):
        return True
    return False

##############
# Problem 06 #
##############

def matrix_product( A, B, m, n, k ):
    """ compute m-by-k product of m-by-n matrix A with n-by-k matrix B. """
    C = []
    for row in range(m):
        current_row = []
        for col in range(k):
            dot_prod = 0
            for cell in range(n):
                dot_prod += A[row*n + cell] * B[cell*k + col]
            current_row.append(dot_prod)
        C += current_row
    return C

##############
# Problem 07 #
##############

def mode( A ):
    """ return the most common value in list A. """
    dictA = {}
    for item in A:
        if item not in dictA:
            dictA[item] = 1
        else:
            dictA[item] += 1
    max_mode = 0
    max_num = A[0]
    for item in A:
        if dictA[item] > max_mode:
            max_mode = dictA[item]
            max_num = item
    return max_num

##############
# Problem 08 #
##############

def transpose( A, m, n ):
    """ return n-by-m transpose of m-by-n matrix A. """
    T = []
    for col in range(n):
        for row in range(m):
            T.append(A[row * n + col])
    return T

##############
# Problem 09 #
##############

def check_valid_paren(s):
    """return True if each left parenthesis is closed by exactly one
    right parenthesis later in the string and each right parenthesis
    closes exactly one left parenthesis earlier in the string."""

    while len(s)>1:
        open_par = s.index("(")
        close_par = s.index(")")
        if open_par < 0 or close_par < 0 or close_par < open_par:
            break
        s = s[:open_par] + s[open_par+1:close_par] + s[close_par+1:]
    if len(s)==0:
        return True
    return False

##############
# Problem 10 #
##############

def get_all_elements(root):
    """ Return a list of all numbers stored in root, in any order. """
    elements = []
    elements.append(root['value'])
    if root['left']:
        elements = elements + get_all_elements(root['left'])
    if root['right']:
        elements = elements + get_all_elements(root['right'])
    return elements


##############
# Problem 11 #
##############

def find_path(grid):
    """ Given a two dimensional n by m grid, with a 0 or a 1 in each cell,
        find a path from the top row (0) to the bottom row (n-1) consisting of
        only ones.  Return the path as a list of coordinate tuples (row, column).
        If there is no path return None. """

    to_check = []
    to_check_ind = 0
    success_path = []
    for i in range(len(grid[0])):
        if grid[0][i]==1:
            to_check.append([(0,i)])

    while to_check_ind < len(to_check):
        current_path = to_check[to_check_ind]
        to_check_ind += 1
        new_path = current_path
        #current_path[-1][1] represents last cell in current path's column number
        for col in range(current_path[-1][1]-1,current_path[-1][1]+2): #Checking three cells in row below
            if grid[current_path[-1][0]+1][col]==1:
                new_path.append((current_path[-1][0]+1,col))
                if len(new_path)==len(grid):
                    success_path = new_path
                    break;
                to_check.append(new_path)
            print(to_check)

    if success_path:
        return success_path
    return None



##############
# Problem 12 #
##############

def longest_sequence(s):
    """ find sequences of a single repeated character in string s.
        Return the length of the longest such sequence. """
    if len(s)==0:
        return 0
    longest_len = 1
    current_len = 1
    for i in range(len(s)-1):
        if s[i+1]==s[i]:
            current_len += 1
        else:
            current_len = 1
        if current_len > longest_len:
            longest_len = current_len
    return longest_len

##############
# Problem 13 #
##############

# straightforward enumeration
def integer_right_triangles(p):
    """Let p be the perimeter of a right triangle with integral, non-zero
       length sides of length a, b, and c.  Return a sorted list of
       solutions with perimeter p. """
    triangles = []
    for a in range(1,p):
        for b in range(a,p):
            c = p - a - b
            if c >= a and c >= b and a**2 + b**2 == c**2:
                triangles.append([a,b,c])
    return triangles

##############
# Problem 14 #
##############

def encode_nested_list(seq):
    """Encode a sequence of nested lists as a flat list."""
    if not isinstance(seq,list):
        return [seq]
    flat_list = ["up","down"]
    insert_ind = 1
    for i in range(len(seq)):
        initial_length = len(flat_list)
        flat_list = flat_list[:insert_ind]+encode_nested_list(seq[i])+flat_list[insert_ind:]
        insert_ind = insert_ind + len(flat_list)-initial_length + 1
    return flat_list
