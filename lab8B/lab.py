"""6.009 Lab 8B: carlae Interpreter Part 2"""

import sys


class EvaluationError(Exception):
    """Exception to be raised if there is an error during evaluation."""

    def __str__(self):
        return "EvaluationError"

class Func:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __str__(self):
        return str(self.body)

class Pair:
    def __init__(self,car,cdr):
        self.car = car
        self.cdr = cdr

    def __str__(self):
        return str(self.car)+ " " + str(self.cdr)

def mult(args):
    prod = 1
    for elem in args:
        prod *= elem
    return prod

def all_equal(args):
    for x in args:
        for y in args:
            if x!= y:
                return False
    return True

def decr(args):
    prev_arg = args[0]
    for i in range(1,len(args)):
        if args[i] >= prev_arg:
            return False
        prev_arg = args[i]
    return True

def non_incr(args):
    prev_arg = args[0]
    for i in range(1,len(args)):
        if args[i] > prev_arg:
            return False
        prev_arg = args[i]
    return True

def incr(args):
    prev_arg = args[0]
    for i in range(1,len(args)):
        if args[i] <= prev_arg:
            return False
        prev_arg = args[i]
    return True

def non_decr(args):
    prev_arg = args[0]
    for i in range(1,len(args)):
        if args[i] < prev_arg:
            return False
        prev_arg = args[i]
    return True

def car(pair):
    pair = pair[0]
    if not isinstance(pair, Pair):
        raise EvaluationError
    return pair.car

def cdr(pair):
    pair = pair[0]
    if not isinstance(pair, Pair):
        raise EvaluationError
    return pair.cdr

def new_list(args):
    #Empty List (Base Case)
    if len(args) == 0:
        return []

    return Pair(args[0],new_list(args[1:]))

def list_len(pair):
    pair = pair[0]
    if pair == []:
        return 0

    if not isinstance(pair, Pair):
        raise EvaluationError

    count = 0
    if pair.car == []:
        return count
    else:
        count += 1
    current_pair = pair
    while current_pair.cdr != []:
        count += 1
        current_pair = current_pair.cdr
    return count

def elt_at_index(args):
    goal_ind = args[1]
    pair = args[0]

    if goal_ind == 0: #If goal index is 0, return first element in the list
        return pair.car

    ind = 1
    current_pair = pair

    #While we haven't reached the goal index yet
    while ind != goal_ind:
        ind += 1
        current_pair = current_pair.cdr

    return current_pair.cdr.car

def concat(args):

    if len(args)==0:
        return []

    if args[0] == []:
        return concat(args[1:])

    if not isinstance(args[0],Pair):
        raise EvaluationError

    if len(args)==1:
        return args[0]

    result_pair = Pair([],[]) #Our new pair
    args_ind = 0 #our place in the list of arguments
    new_pair = result_pair #The start of our new pair

    while args_ind<len(args):
        pair = args[args_ind] #The current pair that we are adding to our result pair
        if pair==[]:
            args_ind += 1
            continue
        new_pair.car = pair.car
        while pair.cdr != []:
            pair = pair.cdr
            new_pair.cdr = Pair(pair.car,[])
            new_pair = new_pair.cdr
        args_ind += 1
        if args_ind < len(args) and args[args_ind] != []:
            new_pair.cdr = Pair([],[])
            new_pair = new_pair.cdr
        print(result_pair)
    return result_pair

def begin(args):
    result = None
    ind = 0
    env = local_env
    while ind < len(args):
        ans = result_and_env(args[ind],env)
        result = ans[0]
        env = ans[1]
        ind += 1
    return result

carlae_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': mult,
    '/': lambda args: args[0] if len(args) == 1 else (args[0]/mult(args[1:])),
    '=?': all_equal,
    '>': decr,
    '>=': non_incr,
    '<': incr,
    '<=': non_decr,
    '#f': False,
    '#t': True,
    'car': car,
    'cdr': cdr,
    'nil': [],
    'list': new_list,
    'length': list_len,
    'elt-at-index': elt_at_index,
    'concat': concat,
    'begin': begin
}

class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        if parent == None:
            self.assignments = carlae_builtins
        else:
            self.assignments = {}


    def __setitem__(self,key,value):
        """
        Setter function: sets key to value in CURRENT environment
        """
        self.assignments[key] = value

    def __getitem__(self,key):
        """
        Getter function: retrieves value of key in current environment,
            otherwise loops through parent environment until found or
            throws EvaluationError.
        """
        if key in self.assignments:
            return self.assignments[key]

        env = self
        while env.parent != None:
            if key in env.parent.assignments:
                return env.parent.assignments[key]
            env = env.parent

        raise EvaluationError

global_env = Environment()
local_env = Environment(global_env)

def subtokenize(str):
    """
    Splits a string with no spaces into tokens. Helper function for tokenize.
    """
    result = []
    substr = ""
    for letter in str:
        if letter == "(" or letter == ")":
            #Separate by parentheses
            if len(substr) > 0:
                result.append(substr)
                substr = ""
            result.append(letter)
        else:
            substr = substr + letter
    if len(substr) > 0:
        result.append(substr)

    return result


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a carlae
                      expression
    """
    result = []
    tokens = source.split("\n")
    #Splitting input into lines
    for token in tokens:
        if len(token) == 0:
            continue

        subtokens = token.split(" ") #Splitting each line into words

        for subtoken in subtokens:
            if ";" in subtoken: #If commented, add stuff before ; as tokens, then break
                comment_ind = subtoken.index(";")
                result += subtokenize(subtoken[:comment_ind])
                break

            if len(subtoken) == 1:
                result.append(subtoken)

            else:
                result += subtokenize(subtoken)
    return result


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    def parse_expression(index):
        """
        index is starting index for traversing through expression

        returns: tuple of parsed value, next index
        """
        try:
            #Checking if token is a num
            return (float(tokens[index]),index+1)

        except:
            result = []
            if tokens[index] == "(":
                index += 1
                while index < len(tokens) and tokens[index] != ")":
                    expr = parse_expression(index)
                    result.append(expr[0])
                    index = expr[1]

                if index == len(tokens):
                    raise SyntaxError
            else:
                return (tokens[index],index+1)
            return (result, index + 1)
    expr = parse_expression(0)
    if expr[1] != len(tokens):
        raise SyntaxError
    return parse_expression(0)[0]

def result_and_env(tree, env = None):
    #Initializing environment (if none given) to empty environment with builtins as parent
    if env == None:
        env = Environment(local_env)
        #env.assignments = {}

    if isinstance(tree,list) and len(tree)==1 and tree[0] in carlae_builtins:
        if tree[0] == '#f' or tree[0] == '#t':
            return carlae_builtins[tree[0]],env
        return carlae_builtins[tree[0]]([]),env

    #print('env',env.assignments)
    if not isinstance(tree,list):
        #Checking if tree is singular number or function
        if isinstance(tree, float) or isinstance(tree, int) or isinstance(tree, Pair) or isinstance(tree, Func):
            return (tree, env)
        return (env[tree],env)

    if isinstance(tree[0],float) or isinstance(tree[0],int):
        raise EvaluationError

    if tree[0] == "begin":
        args = tree[1:]
        result = None
        ind = 0
        while ind < len(args):
            ans = result_and_env(args[ind],env)
            result = ans[0]
            env = ans[1]
            ind += 1
        return result,env

    if tree[0] == "and":
        for item in tree[1:]:
            if result_and_env(item,env)[0] == False:
                return (False,env)
        return (True,env)

    if tree[0] == "or":
        for item in tree[1:]:
            if result_and_env(item,env)[0] == True:
                return (True,env)
        return (False,env)

    if tree[0] == "not":
        return (not result_and_env(tree[1],env)[0],env)

    #Handling conditionals
    if tree[0] == 'if':
        if result_and_env(tree[1],env)[0]: #Evaluate TRUEEXP
            return result_and_env(tree[2],env)
        return result_and_env(tree[3],env)

    #Defining variable
    if tree[0] == "define":
        if len(tree) < 3:
            raise EvaluationError

        #TOCHECK!!!!
        if isinstance(tree[1], list): #If the name is an S-expression, evaluate value as user-defined function
            return result_and_env(['define',tree[1][0],['lambda',tree[1][1:],tree[2]]],env)

        else:
            func_val = result_and_env(tree[2],env)
            #print("setting", tree[1], "to value", func_val[0])
            env[tree[1]] = func_val[0]
            return func_val

    #Creating Func object and returning (keyword lambda)
    if tree[0] == "lambda":
        if len(tree) < 3:
            raise EvaluationError
        new_func = Func(tree[1],tree[2],env)
        return (new_func, env)

    #Creating Pair object and returning (keyword cons)
    if tree[0] == "cons":
        car = result_and_env(tree[1],env)[0]
        cdr = result_and_env(tree[2],env)[0]
        cons = Pair(car,cdr)
        return cons, env

    #Mapping function to all items in list, returning new list
    if tree[0] == "map":
        new_list = ['list']
        pair = result_and_env(tree[2],env)[0]
        func = tree[1]

        if pair == []:
            return ([],env)

        if not isinstance(pair, Pair):
            raise EvaluationError

        if pair.car != []:
            new_list.append(result_and_env([func,pair.car],env)[0])
            while pair.cdr != []:
                pair = pair.cdr
                new_list.append(result_and_env([func,pair.car],env)[0])
        #print(new_list)
        return result_and_env(new_list,env)

    #Filtering list based on function
    if tree[0] == "filter":
        new_list = ['list']
        pair = result_and_env(tree[2],env)[0]
        func = tree[1]

        if not isinstance(pair, Pair):
            raise EvaluationError

        if pair.car != []:
            if result_and_env([func,pair.car],env)[0]:
                new_list.append(pair.car)
            while pair.cdr != []:
                pair = pair.cdr
                if result_and_env([func,pair.car],env)[0]:
                    new_list.append(pair.car)
        #print(new_list)
        return result_and_env(new_list,env)

    if tree[0] == "reduce":
        val = tree[3]
        pair = result_and_env(tree[2],env)[0]
        func = tree[1]

        if not isinstance(pair, Pair):
            raise EvaluationError

        if pair.car != []:
            val = result_and_env([func,val,pair.car],env)[0]
            while pair.cdr != []:
                pair = pair.cdr
                val = result_and_env([func,val,pair.car],env)[0]

        return (val,env)

    if tree[0] == "let":
        new_tree = ['begin']
        new_env = Environment(env)
        for item in tree[1]:
            new_tree.append(['define',item[0],result_and_env(item[1],env)[0]])
        result_env = result_and_env(new_tree,new_env)[1]
        return result_and_env(tree[2],result_env)[0],env

    if tree[0] == "set!":
        key = tree[1]
        val = result_and_env(tree[2],env)[0]

        if key in env.assignments:
            env.assignments[key] = val
            return val, env

        current_env = env
        while current_env.parent != None:
            if key in current_env.parent.assignments:
                current_env.assignments[key] = val
                return val, current_env
            current_env = current_env.parent

        raise EvaluationError

    #Calling function, recursively evaluating
    else:
        op = tree[0]
        #print(op)
        #print('tree:',tree)
        try:
            #print("env",env.assignments)
            #print("parent",env.parent.assignments)
            op = env[tree[0]]
            if isinstance(op,Func): #User defined function
                #print("Function:" , op, "Params", op.params, "Environment", op.env.assignments)
                #Setting environment to child of operation environment
                new_env = Environment(op.env)
                ind = 1
                try: #Trying to match parameters to values in expression following function call
                    for param in op.params:
                        #print("param",param)
                        #print("value",tree[ind])
                        new_env[param] = result_and_env(tree[ind],new_env)[0]
                        ind += 1
                except:
                    raise EvaluationError
                return (result_and_env(op.body, new_env)[0],env)

            else: #built-in function evaluation
                #print(op)
                params = tree[1:]
                new_tree = []
                #print(env.assignments)
                for param in params:
                    new_var = result_and_env(param, env)[0]
                    try:
                        new_tree.append(env[new_var])
                    except:
                        new_tree.append(new_var)
                #print("op",op,"new tree:",new_tree)
                return op(new_tree),env

        except:
            if isinstance(tree[0],Func):
                op = tree[0]
                new_env = Environment(op.env)
                ind = 1
                try: #Trying to match parameters to values in expression following function call
                    for param in op.params:
                        #print("param",param)
                        #print("value",tree[ind])
                        new_env[param] = result_and_env(tree[ind],new_env)[0]
                        ind += 1
                except:
                    raise EvaluationError
                return (result_and_env(tree[0].body,new_env))
            new_tree = []
            #Simplify each element by evaluating, re-evaluate new tree
            for subelem in tree:
                new_elem = result_and_env(subelem, env)
                #print("New element:",new_elem[0],"New Environment:",new_elem[1].assignments,"parent:",new_elem[1].parent.assignments)
                new_tree.append(new_elem[0])
            for item in new_tree:
                if isinstance(item, Func):
                    env = item.env
                    #print(item.body,item.params,item.env.parent.parent.assignments)
            #print(new_tree,env.parent.assignments)
            return result_and_env(new_tree,env)

def evaluate(tree, env = None):
    """
    Evaluate the given syntax tree according to the rules of the carlae
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
        environment: the environment to evaluate/define in
    """
    return result_and_env(tree,env)[0]

# e = Environment()
# env = Environment(e)
# print(evaluate(parse(tokenize("(define x 7)")),env))
# print(evaluate(parse(tokenize("(define foo (lambda (x) (lambda (y) (+ x y))))")),env))
# print(evaluate(parse(tokenize("(define bar (foo 3))")),env))
# print(evaluate(parse(tokenize("(bar 2)")),env))
# print(evaluate(parse(tokenize("((lambda (x) (* x x)) 3)")),env))
#(define addN(lambda (n) (lambda (i) (+ i n))))
#(define add7(addN 7))
#(add7 2)
#(add7 ((addN 3)((addN 19) 8)))

def evaluate_file(file_name,env=global_env):
    file = open(file_name)
    text = file.read()
    return result_and_env(parse(tokenize(text)),env)[0]

if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)
    #pass
    args = sys.argv
    for arg in args:
        if arg != "lab.py":
            evaluate_file(arg)

    expr = input(">>> ")
    env = local_env
    while expr != "QUIT":
        try:
            res = result_and_env(parse(tokenize(expr)),env)
            print(res[0],"environment:",res[1].assignments)
            env = res[1]
        except:
            print("error, try again")
        expr = input(">>> ")

    # expr = input(">>> ")
    # while expr != "QUIT":
    #     try:
    #         res = evaluate(parse(tokenize(expr)))
    #         print(res)
    #     except:
    #         print("error, try again")
    #     expr = input(">>> ")
