"""
AST node definitions.

Each class is a node in the abstract syntax tree the parser builds.
Nodes hold other nodes in their fields, which is what forms the tree.
The __repr__ methods exist only to print trees readably when debugging.
"""


# --- Literals ---

# A number literal, e.g. 42.
class Number:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


# A string literal, e.g. "hello".
class String:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"String({self.value!r})"


# A boolean literal: true or false.
class Boolean:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Boolean({self.value})"


# --- Expressions ---

# Reading a variable, e.g. x.
class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name!r})"


# A binary operation: arithmetic (+ - * /) or comparison (< > <= >= == !=).
class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left}, {self.op!r}, {self.right})"


# A unary operation: not.
class UnaryOp:
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp({self.op!r}, {self.operand})"


# A logical operation: and, or (evaluated with short-circuiting).
class LogicalOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"LogicalOp({self.left}, {self.op!r}, {self.right})"


# A function call, e.g. square(5).
class Call:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"Call({self.name!r}, {self.args})"


# --- Statements ---

# An assignment: x = expression.
class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assign({self.name!r}, {self.value})"


# A block: a sequence of statements between { }.
class Block:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"


# An if statement, with an optional else branch.
class If:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"If({self.condition}, {self.then_branch}, {self.else_branch})"


# A while loop.
class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"While({self.condition}, {self.body})"


# A function definition: fun name(params) { body }.
class FunctionDef:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDef({self.name!r}, {self.params}, {self.body})"


# A return statement.
class Return:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return({self.value})"