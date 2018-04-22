"""6.009 Lab 5 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(100)
# NO ADDITIONAL IMPORTS

def satisfying_assignment(formula):
    """Find a satisfying assignment for a given CNF formula.a
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> sa = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> ('a' in sa and sa['a']) or ('b' in sa and not sa['b']) or ('c' in sa and sa['c'])
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]]) is None
    True
    """
    #print('new_recursion:')
    #print(formula)
    if len(formula)==0: #Base case: empty formula returns empty assignments
        return {}

    assignments = {}

    ind = 0 #Which literal are we looking at?
    boolVal = True #What value does the variable in our current literal have?

    while ind < len(formula[0]): #Look at all variables in first clause until valid assignment is found
        new_formula = simplify_formula(formula,{formula[0][ind][0]:boolVal}) #Try setting first variable to True
        if new_formula[0] != None:
            assignments[formula[0][ind][0]] = boolVal
            assignments.update(new_formula[1])
            #print(assignments)
            try:
                assignments.update(dict(satisfying_assignment(new_formula[0])))
                break
            except TypeError:
                ind += 1
                continue
        else: #If invalid assignment,
            if boolVal: #Try assigning variable to False
                boolVal = False
            else:
                boolVal = True
                ind += 1

    if new_formula[0]==None:
        return None

    return assignments

def simplify_formula(formula, assignments):
    '''
      Input: a boolean formula in the CNF format described above.
            a set of assignments to boolean variables represented as a dictionary
            from variables to boolean values.
      Output: a pair (Formula, Changed), where Formula is
      the new simplified formula, and Changed is a boolean
      that determines whether or not the simplification added new
      assignments. If the assignment causes the formula to
      evaluate to False, you should return (None, False).
      Effects: the operation potentially adds new assignments to
      assignments. However, the operation should NOT modify
      the input formula when creating the output (although it is ok
        for the output formula to share unchanged clauses with the input formula).

      Note that when the simplification creates new assignments,
      those assignments may themselves enable further simplification.
      You should make sure all those newly enabled simplifications
      are performed as well.

      It is advised that you write your own tests for this function.

      >>> simplify_formula([[("a", True), ("b", False), ("c", True)], [("a", True), ("b", True)]],{'a':False})
      ([], {'b': True, 'c': True})

      >>> simplify_formula([[('a',True),('b',True),('c',False)],[('c',True),('d',True)],[('d',False),('e',True),('f',True)]],{'c':False})
      ([[('e', True), ('f', True)]], {'d': True})

      >>> simplify_formula([[('a',True),('b',True),('c',False)],[('c',True),('d',True)],[('d',False),('e',True),('f',True)]],{'c':False,'d':False})
      (None, False)

      >>> simplify_formula([[("a", True), ("b", False), ("c", True)], [("a", False)]],{"a":False})
      ([[('b', False), ('c', True)]], {})
    '''

    new_formula = formula[:]
    new_assignments = {}
    assigned_letters = list(assignments.keys())
    assigned_index = 0 #Keeping track of place in assigned_letters list
    assigned_index_cap = len(assigned_letters)-1 #Current last index in assigned_letters

    while assigned_index < len(assigned_letters):
        var = assigned_letters[assigned_index]
        temp_formula = []
        for clause in new_formula:
            new_clause = []
            new_clause_true = False #Boolean: due to current assignment, will the current clause eval to true?
            for literal in clause:
                if literal[0]== var: #Checking if the literal is about our current variable
                    if assignments[var] == literal[1]: #If not var is False or var is True, clause will eval to True
                        new_clause_true = True
                    elif len(set(clause))==1:#If literal evaluates to False and is the only literal in the clause, clause (and formula) evaluates to False
                        return (None,False)
                else:
                    new_clause.append(literal)
            if not new_clause_true:
                temp_formula.append(new_clause)
        new_formula = temp_formula
        if assigned_index == assigned_index_cap: #If current assigned_letters reaches end,
            for clause in new_formula:
                if len(set(clause))==1: #If there's only one unique literal remaining
                    assigned_letters.append(clause[0][0])
                    assignments[clause[0][0]]=clause[0][1]
                    new_assignments[clause[0][0]]=clause[0][1]
                    assigned_index_cap += 1
        assigned_index += 1
    return (new_formula,new_assignments)

#print(simplify_formula([[('c',True),('c',True),('a',False)],[('b',True),('b',True),('c',False)]],{'a':True,'b':False}))
#print(simplify_formula([[('a',True),('b',True),('c',False)],[('c',True),('d',True)]],{'c':False}))
#print(simplify_formula([[('a',True),('b',True),('c',False)],[('c',True),('d',True)],[('d',False),('e',True),('f',True)]],{'c':False}))
#
# formula = [[("a",True),("b",False),("c",False)], [("a",False),("c",False),("d",False)], [("a",False),("c",False),("d",True)],[("a",False),("c",True),("d",False)],[("a",False),("c",True),("d",True)], [("b",True),("c",True),("d",False)], [("a",True),("b",False),("c",True)], [("a",True),("b",True),("c",False)]]
# new_formula = simplify_formula(formula,{'a':False,'b':False,'c':False,'d':False})
# print(new_formula)

# formula = [[("a",True),("b",False),("c",False)], [("a",False),("c",False),("d",False)], [("a",False),("c",False),("d",True)],[("a",False),("c",True),("d",False)],[("a",False),("c",True),("d",True)], [("b",True),("c",True),("d",False)], [("a",True),("b",False),("c",True)], [("a",True),("b",True),("c",False)]]
# print(satisfying_assignment(formula))
# formula = [[('a',True),('b',True)],[('a',True),('b',False)],[('a',False),('b',True)],[('a',False),('c',False)]]
# print(satisfying_assignment(formula))

def managers_for_actors(K, film_db):
    '''
    Input:
       K , number of managers available.
       film_db, a list of [actor, actor, film] triples describing that two
       actors worked together on a film.
    Output:
        A dictionary representing an assignment of actors to managers, where
        actors are identified by their numerical id in film_db and
        managers are identified by a number from 0 to K-1.
        The assignment must satisfy the constraint that
        if two actors acted together in a film, they should not have the
        same manager.
        If no such assignment is possible, the function returns None.

    You can write this function in terms of three methods:
        make_vars_for_actors: for each actor in the db, you want an indicator
        variable for every possible manager indicating whether that manager
        is the manager for that actor.

        make_one_manager_constraints: This function should create constraints that
        ensure that each actor has one and only one manager.

        make_different_constraint: This function should create constraints
        that ensure that each actor has a different manager from other actors
        in the same movie.

    '''
    #Make dictionary mapping each actor to all actors they have worked with
    acted_with = {}
    for i in range(len(film_db)):
        #If first actor is already in database, add second actor to set of acted with
        if film_db[i][0] in acted_with:
            acted_with[film_db[i][0]].add(film_db[i][1])
        else: #Otherwise, create new set
            acted_with[film_db[i][0]] = {film_db[i][1]}
        if film_db[i][1] in acted_with:
            acted_with[film_db[i][1]].add(film_db[i][0])
        else: #Otherwise, create new set
            acted_with[film_db[i][1]] = {film_db[i][0]}
    actors = list(acted_with.keys())
    constraints = []
    actor_manager_vars = make_vars_for_actors(K, actors)
    constraints += make_one_manager_constraints(actor_manager_vars)
    constraints += make_different_constraint(actor_manager_vars,acted_with)
    sol = satisfying_assignment(constraints)
    if sol != None:
        assignments = {}
        for assignment in sol:
            if sol[assignment]:
                temp=assignment.split("_")
                assignments[int(temp[0])] = int(temp[1])
        if check_solution(assignments,K,film_db): #Valid solution
            return assignments
    return None

def make_vars_for_actors(K,actors):
    """
    For each actor in the db, you want an indicator
    variable for every possible manager indicating whether that manager
    is the manager for that actor.
    Inputs:
        K - number of managers
        actors - list of actors

    Returns dictionary of possible manager assignments for each key value of actor
    """
    #Here, actors are represented by their id, while managers are represented by numbers from 1-K
    result = {}
    for actor in actors:
        result[actor] = []
        for i in range(1,K+1):
            result[actor].append(str(actor)+"_"+str(i))
    return result


def make_one_manager_constraints(vars):
    """
    This function should create constraints that
    ensure that each actor has one and only one manager.
    Inputs:
        vars - dictionary of all possible managers for each actor

    Returns:
        list of constraints in CNF format
    """
    #We want one clause of all literals, and all other clauses of each
    constraints = []
    for actor in vars:
        managers = vars[actor]
        at_least_one_clause = [] #This clause will contain the literals ("A_1",True),...,("A_i",True) for given actor A and K=i, ensuring there is at least one manager
        for i in range(len(managers)):
            at_least_one_clause.append((managers[i],True))
            for j in range(i+1,len(managers)): #Iterating through all pairs of managers for each actor
                constraints.append([(managers[i],False),(managers[j],False)])
        constraints.append(at_least_one_clause)
    return constraints

def make_different_constraint(vars,acted_with):
    """
    This function should create constraints
    that ensure that each actor has a different manager from other actors
    in the same movie.

    Inputs:
        vars - dictionary of all possible managers for each actor
        acted_with - dictionary of all other actors that have acted in a movie with a given actor

    Returns:
        list of constraints in CNF format
    """
    constraints = []
    #(not A_i) or (not B_i) for connected actors A and B and manager i --> either one of two connected actors can have a given manager, or neither, but not both.
    #possible issue: repetition of each pair (should be okay, since cnf value doesnt change)
    for actor in acted_with:
        managers = vars[actor]
        for other_actor in acted_with[actor]:
            if actor != other_actor:
                other_managers = vars[other_actor]
                for i in range(len(managers)):
                    constraints.append([(managers[i],False),(other_managers[i],False)])
    return constraints

def check_solution(sol, K, film_db):
    '''
    Input:
        K, number of managers
        film_db, a list of [actor, actor, film] triples describing that two
        actors worked together on a film.
        sol, an assignment of actors to managers.
    Output:
        The function returns True if sol satisfies the constraint that
        if two actors acted together in a film, they should not have the
        same manager and every manager has an ID less than K.
        It returns False otherwise.
    '''
    for pair in film_db:
        if pair[0] != pair[1] and sol[pair[0]]==sol[pair[1]]:
            return False
    for actor in sol:
        if sol[actor] > K:
            return False
    return True

if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    # import doctest
    # doctest.testmod()
    pass
