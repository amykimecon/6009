"""6.009 Lab 8A: carlae Interpreter"""

import sys


class EvaluationError(Exception):
    """Exception to be raised if there is an error during evaluation."""
    pass


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

carlae_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
}

def evaluate(tree):
    """
    Evaluate the given syntax tree according to the rules of the carlae
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    raise NotImplementedError


if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)
    pass