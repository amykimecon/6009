# NO IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Symbol:
    def __init__(self):
        self.repr = ""

    def deriv(self, var):
        #If symbol is a constant, return 0
        if self.repr == "Num":
            return Num(0)
        #If symbol is a variable, check if it is variable of differentiation, otherwise treat as constant
        if self.repr == "Var":
            if self.name == var:
                return Num(1)
            else:
                return Num(0)

        if self.repr == "Add":
            return self.left.deriv(var) + self.right.deriv(var)

        if self.repr == "Sub":
            return self.left.deriv(var) - self.right.deriv(var)

        if self.repr == "Mul":
            return (self.left * self.right.deriv(var)) + (self.right * self.left.deriv(var))

        if self.repr == "Div":
            return ((self.right * self.left.deriv(var)) - (self.left * self.right.deriv(var))) / (self.right * self.right)

    def simplify(self):
        expr = self
        while True:
            result = None
            if expr.repr == "Num" or expr.repr == "Var":
                return expr
            #If both sides are numbers, return binary op on those numbers
            if expr.left.repr == "Num" and expr.right.repr == "Num":
                if expr.repr == "Add":
                    return Num(expr.left.n + expr.right.n)
                if expr.repr == "Sub":
                    return Num(expr.left.n - expr.right.n)
                if expr.repr == "Mul":
                    return Num(expr.left.n * expr.right.n)
                if expr.repr == "Div":
                    return Num(expr.left.n / expr.right.n)

            if expr.repr == "Add" or expr.repr == "Sub":
                #If one side = 0, return simplification of other side
                if expr.left.repr == "Num" and expr.left.n == 0 and expr.repr=="Add":
                    result = self.right
                elif expr.right.repr == "Num" and expr.right.n == 0:
                    result = self.left

                if result == None:
                    if expr.repr == "Add":
                        result = expr.left.simplify() + expr.right.simplify()
                    else:
                        result = expr.left.simplify() - expr.right.simplify()

            elif expr.repr == "Mul":
                #If mult by 1, return simplification of other side
                #If mult by 0, return 0
                if expr.left.repr == "Num":
                    if expr.left.n == 1:
                        result = expr.right
                    elif expr.left.n == 0:
                        return Num(0)
                elif expr.right.repr == "Num":
                    if expr.right.n == 1:
                        result = expr.left
                    elif expr.right.n == 0:
                        return Num(0)
                if result == None:
                    result = expr.left.simplify() * expr.right.simplify()

            elif expr.repr == "Div":
                #If div by 1, return simplification of other side
                #If 0 on left, return 0
                if expr.left.repr == "Num":
                    if expr.left.n == 0:
                        return Num(0)
                elif expr.right.repr == "Num":
                    if expr.right.n == 1:
                        result = expr.left
                if result == None:
                    result = expr.left.simplify()/expr.right.simplify()

            if result == None:
                break

            if str(result) == str(expr):
                break

            expr = result
        return expr

    def eval(self,mapping):
        expr = self.eval_help(mapping)
        return expr.n

    def eval_help(self,mapping):
        expr = self.simplify()
        while True:
            temp = str(expr)
            if expr.repr == "Num":
                return expr
            if expr.repr == "Var":
                if str(expr) in mapping:
                    return Num(mapping[str(expr)])
                return expr
            if expr.left.repr == "Num":
                if str(expr.left) in mapping:
                    expr.left = mapping[str(expr.left)]
                expr.right = expr.right.eval_help(mapping)

            elif expr.right.repr == "Num":
                if str(expr.right) in mapping:
                    expr.right = mapping[str(expr.right)]
                expr.left = expr.left.eval_help(mapping)

            else:
                expr.left = expr.left.eval_help(mapping)
                expr.right = expr.right.eval_help(mapping)

            if str(expr) == temp:
                break

            expr = expr.simplify()

        return expr


    def __add__(self,obj):
        return Add(self,obj)

    def __sub__(self,obj):
        return Sub(self,obj)

    def __mul__(self,obj):
        return Mul(self,obj)

    def __truediv__(self,obj):
        return Div(self,obj)

    def __radd__(self,obj):
        return Add(obj,self)

    def __rsub__(self,obj):
        return Sub(obj,self)

    def __rmul__(self,obj):
        return Mul(obj,self)

    def __rtruediv__(self,obj):
        return Div(obj,self)

class Var(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n
        self.repr = "Var"

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Var(' + repr(self.name) + ')'

class Num(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n
        self.repr = "Num"

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return 'Num(' + repr(self.n) + ')'

class BinOp(Symbol):
    def __init__(self,left,right):
        if isinstance(left,int):
            left = Num(left)
        if isinstance(right,int):
            right = Num(right)
        if isinstance(left,str):
            left = Var(left)
        if isinstance(right,str):
            right = Var(right)
        self.left = left
        self.right = right
        self.operand = ""
        self.repr = ""
        self.precedence = 0

    def __repr__(self):
        return self.repr + "(" + repr(self.left) + ", " + repr(self.right) + ")"

    def __str__(self):
        left = str(self.left)
        right = str(self.right)
        if isinstance(self.left,BinOp) and self.precedence > self.left.precedence:
            left = "(" + left + ")"
        #If self.right is BinOp and has lower precedence or if self.repr is sub/div and self.right has lower or equal precedence, add parantheses
        if isinstance(self.right,BinOp) and (self.precedence > self.right.precedence or ((self.repr=="Sub" or self.repr=="Div") and self.precedence >= self.right.precedence)):
            right = "(" + right + ")"

        return left + " " + self.operand + " " + right

class Add(BinOp):
    def __init__(self,left,right):
        BinOp.__init__(self,left,right)
        self.operand = "+"
        self.repr = "Add"
        self.precedence = 1

class Sub(BinOp):
    def __init__(self,left,right):
        BinOp.__init__(self,left,right)
        self.operand = "-"
        self.repr = "Sub"
        self.precedence = 1

class Mul(BinOp):
    def __init__(self,left,right):
        BinOp.__init__(self,left,right)
        self.operand = "*"
        self.repr = "Mul"
        self.precedence = 2

class Div(BinOp):
    def __init__(self,left,right):
        BinOp.__init__(self,left,right)
        self.operand = "/"
        self.repr = "Div"
        self.precedence = 2

def tokenize(str):
    result = []
    tokens = str.split(" ")
    for token in tokens:
        if len(token) == 1:
            result.append(token)
        else:
            substr = ""
            for letter in token:
                if letter == "(" or letter == ")":
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
    def parse_expression(index):
        """
        index is starting index for traversing through expression
        tokens is a list of tokens to parse

        returns: tuple of parsed value, next index
        """
        try:
            #Checking if token is a num
            return (Num(int(tokens[index])), index + 1)
        except:
            #Checking if token is a variable
            if tokens[index] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                return Var(tokens[index]), index + 1

            if tokens[index] == "(":
                parsed_left = parse_expression(index + 1) #Next expression parsed
                parsed_right = parse_expression(parsed_left[1] + 1) #Expression after operation sign, parsed

                if tokens[parsed_right[1]] == ")": #Skip next token if it is a closed bracket
                    parsed_right = parsed_right[0],parsed_right[1] + 1

                #Returning binop on left and right expressions
                if tokens[parsed_left[1]] == "+":
                    return Add(parsed_left[0],parsed_right[0]), parsed_right[1]
                if tokens[parsed_left[1]] == "-":
                    return Sub(parsed_left[0],parsed_right[0]), parsed_right[1]
                if tokens[parsed_left[1]] == "*":
                    return Mul(parsed_left[0],parsed_right[0]), parsed_right[1]
                if tokens[parsed_left[1]] == "/":
                    return Div(parsed_left[0],parsed_right[0]), parsed_right[1]


    parsed_expression, next_index = parse_expression(0)
    return parsed_expression

def sym(str):
    return parse(tokenize(str))
# z = Add(Var('x'), Sub(Var('y'), Num(2)))
# a = Add(2,Var('x'))
# print(str(a))
# print(repr(z))  # notice that this result, if fed back into Python, produces an equivalent object.
# print(str(z))  # this result cannot necessarily be fed back into Python, but it looks nicer.
#
# print(str(Var('x') + Num(3) + Num(2)))
#
# print(Var('a') * Var('b'))
# print(2 + Var('x'))
# print(Num(3) / 2)
# print(Num(3) + 'x')

# result = ('z' * Num(3)) + 0
# print(repr(result))
# a = Add(Var('x'), Mul(Var('x'), Var('x')))
# print(a.deriv('x'))

# a = Add(Add(Num(0), Var('y')), Var('x'))
# print(a.deriv('x'))

# x = Var('x')
# y = Var('y')
# z = 2*x - x*y + 3*y
# der = z.deriv("x")
#
# symb = Add(Num(20),Mul(Num(101), Mul(Num(1), Var('z'))))
# sub = Mul(Num(1), Var('z'))
# print(symb)
# print(symb.simplify())

# z = Add(Var('x'), Sub(Var('y'), Mul(Var('z'), Num(2))))
# print(z.eval({'x': 3, 'y': 10, 'z': 2}))
# #
# tokens = tokenize("((z * 3) + 0)")
# print(tokens)
# print(parse(tokens))
#
# x = Mul(Num(-1), Add(Add(Sub(Var('B'), Num(0)), Add(Div(Div(Add(Var('J'), Var('k')), Div(Sub(Num(0), Div(Add(Div(Mul(Add(Sub(Sub(Num(1), Var('B')), Mul(Var('x'), Num(1))), Sub(Div(Num(-1), Var('F')), Mul(Var('D'), Var('s')))), Var('Q')), Div(Add(Add(Sub(Var('L'), Var('s')), Add(Num(0), Num(1))), Div(Div(Var('j'), Num(1)), Mul(Var('F'), Var('B')))), Sub(Add(Num(1), Num(1)), Div(Sub(Num(0), Var('h')), Var('I'))))), Mul(Sub(Sub(Num(0), Var('f')), Sub(Mul(Var('r'), Mul(Var('h'), Var('U'))), Div(Add(Var('A'), Num(1)), Num(1)))), Mul(Sub(Add(Mul(Num(0), Var('h')), Num(1)), Add(Sub(Var('t'), Var('b')), Sub(Num(0), Num(1)))), Num(0)))), Var('p'))), Sub(Add(Div(Mul(Var('Q'), Sub(Sub(Var('c'), Sub(Sub(Num(0), Var('I')), Mul(Var('Z'), Var('t')))), Add(Add(Num(0), Var('z')), Div(Var('h'), Div(Num(-1), Var('T')))))), Mul(Mul(Num(1), Sub(Sub(Div(Var('Q'), Num(-1)), Sub(Var('q'), Num(0))), Mul(Div(Num(1), Var('V')), Div(Var('a'), Num(1))))), Add(Div(Mul(Mul(Num(-1), Num(0)), Sub(Num(-1), Var('u'))), Div(Add(Var('T'), Var('p')), Sub(Var('D'), Var('w')))), Add(Div(Var('P'), Num(1)), Mul(Add(Num(1), Num(1)), Sub(Num(0), Num(0))))))), Div(Num(1), Sub(Mul(Div(Num(-1), Add(Num(1), Div(Num(0), Num(1)))), Sub(Sub(Sub(Var('A'), Num(1)), Mul(Num(0), Num(-1))), Sub(Num(-1), Mul(Var('Z'), Var('L'))))), Add(Add(Sub(Var('v'), Div(Num(1), Var('x'))), Div(Sub(Var('R'), Var('N')), Div(Var('X'), Var('z')))), Sub(Sub(Mul(Num(-1), Num(1)), Sub(Var('W'), Num(1))), Num(-1)))))), Add(Var('y'), Add(Var('u'), Var('n')))))), Mul(Div(Num(-1), Num(-1)), Div(Div(Div(Add(Var('L'), Add(Add(Mul(Mul(Div(Var('y'), Num(-1)), Mul(Num(0), Num(1))), Num(1)), Sub(Var('s'), Div(Mul(Var('V'), Var('J')), Div(Num(-1), Var('u'))))), Var('E'))), Mul(Mul(Div(Add(Div(Mul(Var('R'), Num(1)), Add(Num(-1), Var('d'))), Sub(Num(-1), Div(Var('I'), Var('t')))), Div(Var('m'), Var('u'))), Add(Sub(Add(Sub(Var('h'), Var('l')), Sub(Var('e'), Var('p'))), Sub(Mul(Var('R'), Num(-1)), Div(Num(1), Var('k')))), Add(Var('C'), Num(1)))), Var('b'))), Var('d')), Div(Var('a'), Sub(Sub(Div(Div(Div(Sub(Div(Num(-1), Num(1)), Add(Var('D'), Var('f'))), Add(Var('S'), Num(0))), Var('V')), Num(-1)), Sub(Num(0), Sub(Add(Sub(Div(Num(0), Var('r')), Num(1)), Sub(Mul(Num(0), Var('N')), Var('T'))), Mul(Add(Div(Var('U'), Num(-1)), Add(Var('g'), Num(-1))), Add(Mul(Num(-1), Num(0)), Div(Num(1), Var('r'))))))), Div(Num(1), Add(Num(1), Mul(Div(Var('Q'), Mul(Div(Num(1), Num(-1)), Num(-1))), Sub(Div(Add(Var('q'), Num(-1)), Add(Num(1), Num(0))), Var('W')))))))))), Sub(Mul(Num(-1), Div(Var('U'), Div(Mul(Sub(Div(Div(Add(Div(Mul(Num(-1), Var('a')), Add(Var('k'), Var('l'))), Add(Sub(Var('A'), Num(0)), Mul(Num(-1), Num(-1)))), Div(Mul(Var('c'), Num(-1)), Add(Var('N'), Add(Var('y'), Var('X'))))), Num(-1)), Add(Num(1), Num(-1))), Num(-1)), Num(-1)))), Var('r')))), Var('C')))
# print(x)
