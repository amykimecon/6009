"""6.009 Lab 8A: carlae Interpreter"""

import sys


class EvaluationError(Exception):
    """Exception to be raised if there is an error during evaluation."""

    def __str__(self):
        return "EvaluationError"

def mult(args):
    prod = 1
    for elem in args:
        prod *= elem
    return prod


class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        if parent == None:
            self.assignments = {
                '+': sum,
                '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
                '*': mult,
                '/': lambda args: args[0] if len(args) == 1 else (args[0]/mult(args[1:]))
            }
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

class Func:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __str__(self):
        return str(self.body)

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
        #Skip commented line
        if len(token) == 0:
            continue

        subtokens = token.split(" ")

        for subtoken in subtokens:
            if ";" in subtoken:
                break
            if len(subtoken) == 1:
                result.append(subtoken)

            else:
                substr = ""
                for letter in subtoken:
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
        env = Environment(Environment())
        env.assignments = {}

    print('env',env.assignments)
    if not isinstance(tree,list):
        #Checking if tree is singular number or function
        if isinstance(tree, float) or isinstance(tree, int):
            return (tree, env)
        return (env[tree],env)

    #Defining variable
    if tree[0] == "define":
        if len(tree) < 3:
            raise EvaluationError

        if isinstance(tree[1], list): #If the name is an S-expression, evaluate value as user-defined function
            return result_and_env(['define',tree[1][0],['lambda',tree[1][1:],tree[2]]],env)

        else:
            print("setting", tree[1], "to value",result_and_env(tree[2],env)[0])
            env[tree[1]] = result_and_env(tree[2],env)[0]
            return result_and_env(tree[2],env)

    #Creating Func object and returning
    if tree[0] == "lambda":
        if len(tree) < 3:
            raise EvaluationError
        return (Func(tree[1],tree[2],env), env)

    #Calling function, recursively evaluating
    else:
        try:
            #print("env",env.assignments)
            #print("parent",env.parent.assignments)
            op = env[tree[0]]
            print("Function:" , op, "Params", op.params, "Environment", op.env.assignments)
        finally:
            if isinstance(tree[0],int) or isinstance(tree[0],float):
                raise EvaluationError
            try:
                #print('tree',tree)
                if tree[0][0] == "lambda":
                    first = result_and_env(tree[0],env)[0]
                    #print('first',first)
                    if isinstance(first,Func):
                        env['temp_lambda'] = first
                        op = first
            finally:
                if isinstance(op, Func):
                    if env.parent == op.env:
                        new_env = env
                    else:
                        new_env = Environment(op.env)
                    ind = 1
                    try:
                        for param in op.params:
                            print("param",param)
                            print("value",tree[ind])
                            new_env[param] = result_and_env(tree[ind],new_env)[0]
                            ind += 1
                    except:
                        raise EvaluationError
                    return (result_and_env(op.body, new_env)[0],new_env)

                tree = tree[1:]
                new_tree = []
                for subelem in tree:
                    new_tree.append(result_and_env(subelem, env)[0])
                return op(new_tree),env

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


if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)
    # pass
    expr = input(">>> ")
    env = Environment(Environment())
    while expr != "QUIT":
        try:
            res = result_and_env(parse(tokenize(expr)),env)
            print(res[0])
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
