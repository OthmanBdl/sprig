from ast_nodes import (Number, String, Boolean, Variable, Assign,
                       BinaryOp, UnaryOp, LogicalOp,
                       Block, If, While, FunctionDef, Call, Return)


# Raised by a Return node to unwind out of a function body.
# It's not a real error: it's a control-flow signal that carries the value.
class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value


# A scope: a name->value map with a link to its parent scope.
# Lookups check this scope first, then walk up the parent chain.
class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise Exception(f"Undefined variable: {name}")

    def set(self, name, value):
        self.vars[name] = value

    def has(self, name):
        if name in self.vars:
            return True
        if self.parent is not None:
            return self.parent.has(name)
        return False


# Walks the AST and evaluates it (a tree-walking interpreter).
class Interpreter:
    def __init__(self, tree, env=None):
        self.tree = tree
        self.env = env if env is not None else Environment()

    def eval(self, node):
        # --- Literals ---
        if isinstance(node, Number):
            return node.value
        if isinstance(node, String):
            return node.value
        if isinstance(node, Boolean):
            return node.value

        # --- Arithmetic and comparison ---
        if isinstance(node, BinaryOp):
            left = self.eval(node.left)
            right = self.eval(node.right)
            if node.op == "+":
                return left + right
            if node.op == "-":
                return left - right
            if node.op == "*":
                return left * right
            if node.op == "/":
                return left / right
            if node.op == "<":
                return left < right
            if node.op == ">":
                return left > right
            if node.op == "<=":
                return left <= right
            if node.op == ">=":
                return left >= right
            if node.op == "==":
                return left == right
            if node.op == "!=":
                return left != right
            if node.op == "%":
                return left % right
            raise Exception(f"Unknown operator: {node.op}")

        if isinstance(node, UnaryOp):
            value = self.eval(node.operand)
            if node.op == "not":
                return not value
            raise Exception(f"Unknown unary operator: {node.op}")

        # Logical operators short-circuit: the right side is only evaluated
        # when the left side doesn't already determine the result.
        if isinstance(node, LogicalOp):
            left = self.eval(node.left)
            if node.op == "and":
                if not left:
                    return left
                return self.eval(node.right)
            if node.op == "or":
                if left:
                    return left
                return self.eval(node.right)
            raise Exception(f"Unknown logical operator: {node.op}")

        # --- Variables ---
        if isinstance(node, Variable):
            return self.env.get(node.name)
        if isinstance(node, Assign):
            value = self.eval(node.value)
            self.env.set(node.name, value)
            return value

        # --- Control flow ---
        if isinstance(node, Block):
            result = None
            for statement in node.statements:
                result = self.eval(statement)
            return result  # value of the last statement

        if isinstance(node, If):
            if self.eval(node.condition):
                return self.eval(node.then_branch)
            if node.else_branch is not None:
                return self.eval(node.else_branch)
            return None

        if isinstance(node, While):
            result = None
            # The condition is re-evaluated before every iteration.
            while self.eval(node.condition):
                result = self.eval(node.body)
            return result

        # --- Functions ---
        if isinstance(node, FunctionDef):
            # Store the function in the environment; don't run it yet.
            self.env.set(node.name, node)
            return None

        if isinstance(node, Return):
            raise ReturnValue(self.eval(node.value))

        if isinstance(node, Call):
            # Built-in: print.
            if node.name == "print":
                values = [self.eval(arg) for arg in node.args]
                print(" ".join(str(v) for v in values))
                return None

            # User-defined function.
            if not self.env.has(node.name):
                raise Exception(f"Undefined function: {node.name}")
            function = self.env.get(node.name)
            if not isinstance(function, FunctionDef):
                raise Exception(f"{node.name} is not a function")
            if len(node.args) != len(function.params):
                raise Exception(
                    f"{node.name} expects {len(function.params)} argument(s), "
                    f"but got {len(node.args)}")

            # Evaluate args in the current scope, then run the body in a
            # fresh local scope whose parent is the current environment.
            arg_values = [self.eval(arg) for arg in node.args]
            local_env = Environment(parent=self.env)
            for param_name, value in zip(function.params, arg_values):
                local_env.set(param_name, value)

            previous_env = self.env
            self.env = local_env
            try:
                result = self.eval(function.body)
            except ReturnValue as ret:
                result = ret.value
            self.env = previous_env  # restore scope, even after a return
            return result

        raise Exception(f"Unknown node: {node}")

    def interpret(self):
        return self.eval(self.tree)


if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser

    source = "10 / 2 + 3"
    tokens = Lexer(source).tokenize()
    tree = Parser(tokens).parse()
    result = Interpreter(tree).interpret()
    print(f"{source} = {result}")