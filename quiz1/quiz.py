# NO IMPORTS!

##################################################
### Problem 1: batch
##################################################

def batch(inp, size):
    """ Return a list of batches, per quiz specification """
    inp = list(inp)
    batches = []
    current_batch = []
    current_sum = 0

    for elem in inp:
        current_batch.append(elem)
        current_sum += elem
        if current_sum >= size:
            batches.append(current_batch)
            current_sum = 0
            current_batch = []
    if len(current_batch) > 0:
        batches.append(current_batch)
    return batches

##################################################
### Problem 2: order
##################################################

def order(inp):
    """ Return an ordered list of string, per quiz specification """
    output = []
    while len(inp) > 0:
        first_letter = inp[0][0]
        temp_input = []
        for word in inp:
            if word[0]==first_letter:
                output.append(word)
            else:
                temp_input.append(word)
        inp = temp_input
    return output


##################################################
### Problem 3: path_to_happiness
##################################################

def path_to_happiness(field):
    """ Return a path through field of smiles that maximizes happiness """
    rows = field["nrows"]
    cols = field["ncols"]
    smiles = field["smiles"]
    max_smiles = []
    max_paths = []
    for row in range(rows):
        max_paths.append([row])
        max_smiles.append(smiles[row][0])
    for col in range(1,cols): #For each successive column, find max path from max_paths and max_smiles
        temp_max_smiles = max_smiles[:]
        temp_max_paths = max_paths[:]
        for row in range(rows):
            max_prev_row_smiles = 0 #Maximum path of previous column
            max_prev_row = row #Previous row with maximum smiles
            for prev_row in range(row-1,row+2):
                if 0 <= prev_row < rows:
                    if temp_max_smiles[prev_row] > max_prev_row_smiles:
                        max_prev_row_smiles = temp_max_smiles[prev_row]
                        max_prev_row = prev_row
            max_smiles[row] = temp_max_smiles[max_prev_row] + smiles[row][col]
            max_paths[row] = temp_max_paths[max_prev_row] + [row]
        #print(str(max_paths)+"\n")

    max_smiles_total = 0
    max_smiles_path = []
    for row in range(rows):
        if max_smiles[row] > max_smiles_total:
            max_smiles_total = max_smiles[row]
            max_smiles_path = max_paths[row]
    return max_smiles_path

    # rows = field["nrows"]
    # max_happy = 0
    # max_happy_path = []
    # to_check = []
    # checked = set()
    # current_ind = 0
    #
    # for r in range(rows):
    #     to_check.append([r])
    #
    # while current_ind < len(to_check):
    #     current_path = to_check[current_ind]
    #     current_sum = 0
    #     if len(current_path) == field["ncols"]:
    #         for col in range(len(current_path)):
    #             current_sum += field["smiles"][current_path[col]][col]
    #         if current_sum > max_happy:
    #             max_happy = current_sum
    #             max_happy_path = current_path
    #     else:
    #         last_node = current_path[-1]
    #         for next_node in range(last_node-1,last_node+2):
    #             if 0 <= next_node < rows:
    #                 to_check.append(current_path + [next_node])
    #     current_ind += 1
    # return max_happy_path
