# NO IMPORTS!

#############
# Problem 1 #
#############

def runs(L):
    """ return a new list where runs of consecutive numbers
        in L have been combined into sublists. """
    runs = []
    current_run = []
    if len(L)>0:
        current_run = [L[0]]
    for i in range(len(L)-1):
        if L[i]+1==L[i+1]:
            current_run.append(L[i+1])
        else:
            if len(current_run)==1:
                runs.append(current_run[0])
            else:
                runs.append(current_run)
            current_run = [L[i+1]]
    if len(current_run)>0:
        if len(current_run)==1:
            runs.append(current_run[0])
        else:
            runs.append(current_run)
    return runs

#############
# Problem 2 #
#############

def is_cousin(parent_db, A, B):
    """ If A and B share at least one grandparent but do not share a parent,
        return one of the shared grandparents, else return None. """
    parent_dict = {}
    for item in parent_db:
        if item[0] in parent_dict: #If parent is already in the dictionary, add this child to value (set of children)
            parent_dict[item[0]].add(item[1])
        else:
            parent_dict[item[0]] = {item[1]}

    child_dict = {}
    for item in parent_db:
        if item[1] in child_dict: #If child is already in the dictionary, add this parent to value (set of parents)
            child_dict[item[1]].add(item[0])
        else:
            child_dict[item[1]] = {item[0]}

    if A==B:
        return None

    for parent in parent_dict:
        if A in parent_dict[parent] and B in parent_dict[parent]: #Checking if they share the same parent
            return None

    grandparents_A = set()
    for parent in child_dict[A]: #Iterating through parents of A
        for grandparent in child_dict[parent]: #Iterating through parents of parents of A (grandparents of A)
            grandparents_A.add(grandparent)

    for parent in child_dict[B]: #Iterating through parents of B
        for grandparent in child_dict[parent]: #Iterating through parents of parents of B (grandparents of B)
            if grandparent in grandparents_A:
                return grandparent

    return None


#############
# Problem 3 #
#############

def all_phrases(grammar, root):
    """ Using production rules from grammar expand root into
        all legal phrases. """
    #
    # if root not in grammar:
    #     return [[root]]
    #
    # phrases = []
    # for structure in grammar[root]:
    #     for fragment in structure:
    #         phrases = phrases + all_phrases(grammar,fragment)
    # print(phrases)
    # return phrases

    if root not in grammar:
        return [[root]]
    phrases = []
    for structure in grammar[root]:
        phrase_template = []
        for speech_part in structure:
            if speech_part not in grammar:
                if len(phrase_template)>0:
                    new_phrase_template = []
                    for phrase in phrase_template:
                        if type(phrase)==str:
                            phrase = [phrase]
                        new_phrase_template.append(phrase+[speech_part])
                    phrase_template = new_phrase_template
                else:
                    phrase_template.append([speech_part])
            else:
                if len(phrase_template)>0:
                    new_phrase_template = []
                    for phrase in phrase_template:
                        if type(phrase)==str:
                            phrase = [phrase]
                        for fragment in grammar[speech_part]:
                            fragmented_bool = False
                            for fragmented in fragment:
                                if fragmented in grammar:
                                    fragmented_bool = True
                                    for subfragment in grammar[fragmented]:
                                        new_phrase_template.append(phrase+subfragment)
                            if not fragmented_bool:
                                new_phrase_template.append(phrase+fragment)
                    phrase_template = new_phrase_template
                else:
                    for fragment in grammar[speech_part]:
                        if fragment[0] in grammar:
                            for subfragment in grammar[fragment[0]]:
                                phrase_template.append(subfragment)
                        else:
                            phrase_template.append(fragment)
        phrases = phrases + phrase_template
    return phrases
