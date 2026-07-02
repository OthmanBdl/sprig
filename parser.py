from lexer import (NUMBER, PLUS, MINUS, STAR, SLASH, LPAREN, RPAREN, EOF,
                   IDENT, ASSIGN, TRUE, FALSE, LT, GT, LE, GE, EQ, NE,
                   IF, ELSE, LBRACE, RBRACE, WHILE, FUN, RETURN, COMMA,
                   AND, OR, NOT, FOR, SEMICOLON, STRING)
from ast_nodes import (Number, BinaryOp, Variable, Assign, Boolean,
                       Block, If, While, FunctionDef, Call, Return,
                       LogicalOp, UnaryOp, String)


# Turns a flat list of tokens into an AST using recursive descent.
# Each method handles one precedence level and calls the next one down.
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # Look at the current token without consuming it.
    def peek(self):
        return self.tokens[self.pos]

    # Return the current token and advance past it.
    def advance(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    # Consume the current token, but only if it matches the expected type.
    def expect(self, type_):
        token = self.peek()
        if token.type != type_:
            raise Exception(f"Expected {type_}, but found {token.type}")
        return self.advance()

    # A statement: if / while / for / function / return / block, or a bare expression.
    def statement(self):
        token = self.peek()

        if token.type == IF:
            return self.if_statement()
        if token.type == WHILE:
            return self.while_statement()
        if token.type == FOR:
            return self.for_statement()
        if token.type == FUN:
            return self.function_def()
        if token.type == RETURN:
            return self.return_statement()
        if token.type == LBRACE:
            return self.block()

        return self.assignment()

    def if_statement(self):
        self.expect(IF)
        self.expect(LPAREN)
        condition = self.assignment()
        self.expect(RPAREN)
        then_branch = self.block()

        else_branch = None
        if self.peek().type == ELSE:
            self.advance()
            else_branch = self.block()

        return If(condition, then_branch, else_branch)

    def while_statement(self):
        self.expect(WHILE)
        self.expect(LPAREN)
        condition = self.assignment()
        self.expect(RPAREN)
        body = self.block()
        return While(condition, body)

    # A for loop is desugared into an equivalent while loop:
    #   for (init; cond; incr) { body }  ->  { init; while (cond) { body; incr } }
    def for_statement(self):
        self.expect(FOR)
        self.expect(LPAREN)
        init = self.assignment()
        self.expect(SEMICOLON)
        condition = self.assignment()
        self.expect(SEMICOLON)
        increment = self.assignment()
        self.expect(RPAREN)
        body = self.block()

        new_body = Block(body.statements + [increment])
        the_while = While(condition, new_body)
        return Block([init, the_while])

    def function_def(self):
        self.expect(FUN)
        name_token = self.expect(IDENT)
        self.expect(LPAREN)

        # Read the comma-separated parameter list (may be empty).
        params = []
        if self.peek().type != RPAREN:
            params.append(self.expect(IDENT).value)
            while self.peek().type == COMMA:
                self.advance()
                params.append(self.expect(IDENT).value)

        self.expect(RPAREN)
        body = self.block()
        return FunctionDef(name_token.value, params, body)

    def return_statement(self):
        self.expect(RETURN)
        value = self.assignment()
        return Return(value)

    def block(self):
        self.expect(LBRACE)
        statements = []
        while self.peek().type != RBRACE and self.peek().type != EOF:
            statements.append(self.statement())
        self.expect(RBRACE)
        return Block(statements)

    # Assignment has the lowest precedence of all expressions.
    def assignment(self):
        node = self.logic_or()

        if self.peek().type == ASSIGN:
            self.advance()
            value = self.assignment()
            if isinstance(node, Variable):
                return Assign(node.name, value)
            raise Exception("Invalid assignment target")

        return node

    def logic_or(self):
        node = self.logic_and()
        while self.peek().type == OR:
            self.advance()
            right = self.logic_and()
            node = LogicalOp(node, "or", right)
        return node

    def logic_and(self):
        node = self.comparison()
        while self.peek().type == AND:
            self.advance()
            right = self.comparison()
            node = LogicalOp(node, "and", right)
        return node

    def comparison(self):
        node = self.expression()
        while self.peek().type in (LT, GT, LE, GE, EQ, NE):
            op_token = self.advance()
            ops = {LT: "<", GT: ">", LE: "<=", GE: ">=", EQ: "==", NE: "!="}
            op = ops[op_token.type]
            right = self.expression()
            node = BinaryOp(node, op, right)
        return node

    # Addition and subtraction.
    def expression(self):
        node = self.term()
        while self.peek().type in (PLUS, MINUS):
            op_token = self.advance()
            op = "+" if op_token.type == PLUS else "-"
            right = self.term()
            node = BinaryOp(node, op, right)
        return node

    # Multiplication and division.
    def term(self):
        node = self.unary()
        while self.peek().type in (STAR, SLASH):
            op_token = self.advance()
            op = "*" if op_token.type == STAR else "/"
            right = self.unary()
            node = BinaryOp(node, op, right)
        return node

    # Unary "not" (recurses to allow "not not x").
    def unary(self):
        if self.peek().type == NOT:
            self.advance()
            operand = self.unary()
            return UnaryOp("not", operand)
        return self.factor()

    # The highest precedence: literals, variables, calls, and parentheses.
    def factor(self):
        token = self.peek()

        if token.type == NUMBER:
            self.advance()
            return Number(token.value)

        if token.type == STRING:
            self.advance()
            return String(token.value)

        if token.type == IDENT:
            self.advance()
            # An identifier followed by "(" is a function call.
            if self.peek().type == LPAREN:
                self.advance()
                args = []
                if self.peek().type != RPAREN:
                    args.append(self.assignment())
                    while self.peek().type == COMMA:
                        self.advance()
                        args.append(self.assignment())
                self.expect(RPAREN)
                return Call(token.value, args)
            return Variable(token.value)

        # A parenthesized expression: re-parse from the top, then expect ")".
        if token.type == LPAREN:
            self.advance()
            node = self.expression()
            self.expect(RPAREN)
            return node

        if token.type == TRUE:
            self.advance()
            return Boolean(True)

        if token.type == FALSE:
            self.advance()
            return Boolean(False)

        raise Exception(f"Unexpected token: {token.type}")

    # Entry point: parse the whole program as a sequence of statements.
    def parse(self):
        statements = []
        while self.peek().type != EOF:
            statements.append(self.statement())
        return Block(statements)


if __name__ == "__main__":
    from lexer import Lexer

    source = "3 + 4 * 2"
    tokens = Lexer(source).tokenize()
    tree = Parser(tokens).parse()
    print(tree)