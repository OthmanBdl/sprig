# Token types. Each is just a string label used to tag a token.
IDENT     = "IDENT"      # variable/function name: x, total, myFunc
NUMBER    = "NUMBER"     # integer literal: 42
STRING    = "STRING"     # string literal: "hello"
ASSIGN    = "ASSIGN"     # =
PLUS      = "PLUS"       # +
MINUS     = "MINUS"      # -
STAR      = "STAR"       # *
SLASH     = "SLASH"      # /
LPAREN    = "LPAREN"     # (
RPAREN    = "RPAREN"     # )
LBRACE    = "LBRACE"     # {
RBRACE    = "RBRACE"     # }
COMMA     = "COMMA"      # ,
SEMICOLON = "SEMICOLON"  # ;
LT        = "LT"         # 
GT        = "GT"         # >
LE        = "LE"         # <=
GE        = "GE"         # >=
EQ        = "EQ"         # ==
NE        = "NE"         # !=
TRUE      = "TRUE"       # true
FALSE     = "FALSE"      # false
IF        = "IF"         # if
ELSE      = "ELSE"       # else
WHILE     = "WHILE"      # while
FOR       = "FOR"        # for
FUN       = "FUN"        # fun
RETURN    = "RETURN"     # return
AND       = "AND"        # and
OR        = "OR"         # or
NOT       = "NOT"        # not
EOF       = "EOF"        # end of input


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type}, {self.value})"
        return f"Token({self.type})"


# Turns raw source text into a flat list of tokens, one character-scan at a time.
class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0

    def tokenize(self):
        tokens = []

        while self.pos < len(self.source):
            char = self.source[self.pos]

            # Skip whitespace.
            if char in " \t":
                self.pos += 1

            # A number: read all consecutive digits at once.
            elif char.isdigit():
                tokens.append(Token(NUMBER, self.read_number()))

            # A string: read everything between the quotes.
            elif char == '"':
                tokens.append(Token(STRING, self.read_string()))

            # Single-character operators and punctuation.
            elif char == "+":
                tokens.append(Token(PLUS))
                self.pos += 1
            elif char == "-":
                tokens.append(Token(MINUS))
                self.pos += 1
            elif char == "*":
                tokens.append(Token(STAR))
                self.pos += 1
            elif char == "/":
                tokens.append(Token(SLASH))
                self.pos += 1
            elif char == "(":
                tokens.append(Token(LPAREN))
                self.pos += 1
            elif char == ")":
                tokens.append(Token(RPAREN))
                self.pos += 1
            elif char == "{":
                tokens.append(Token(LBRACE))
                self.pos += 1
            elif char == "}":
                tokens.append(Token(RBRACE))
                self.pos += 1
            elif char == ",":
                tokens.append(Token(COMMA))
                self.pos += 1
            elif char == ";":
                tokens.append(Token(SEMICOLON))
                self.pos += 1

            # Operators that may be one or two characters: look ahead to decide.
            elif char == "<":
                if self.peek_char() == "=":
                    tokens.append(Token(LE))
                    self.pos += 2
                else:
                    tokens.append(Token(LT))
                    self.pos += 1
            elif char == ">":
                if self.peek_char() == "=":
                    tokens.append(Token(GE))
                    self.pos += 2
                else:
                    tokens.append(Token(GT))
                    self.pos += 1
            elif char == "=":
                if self.peek_char() == "=":
                    tokens.append(Token(EQ))
                    self.pos += 2
                else:
                    tokens.append(Token(ASSIGN))
                    self.pos += 1
            elif char == "!":
                if self.peek_char() == "=":
                    tokens.append(Token(NE))
                    self.pos += 2
                else:
                    raise Exception("Unexpected character: '!'")

            # An identifier or keyword: read the word, then check if it's reserved.
            elif char.isalpha() or char == "_":
                name = self.read_identifier()
                keywords = {
                    "true": TRUE, "false": FALSE,
                    "if": IF, "else": ELSE,
                    "while": WHILE, "for": FOR,
                    "fun": FUN, "return": RETURN,
                    "and": AND, "or": OR, "not": NOT,
                }
                if name in keywords:
                    tokens.append(Token(keywords[name]))
                else:
                    tokens.append(Token(IDENT, name))

            else:
                raise Exception(f"Unknown character: {char!r}")

        tokens.append(Token(EOF))
        return tokens

    # Read consecutive digits and return them as an int.
    def read_number(self):
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            self.pos += 1
        return int(self.source[start:self.pos])

    # Read a string literal's contents (the surrounding quotes are dropped).
    def read_string(self):
        self.pos += 1  # skip opening quote
        start = self.pos
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            self.pos += 1
        if self.pos >= len(self.source):
            raise Exception("Unterminated string (missing closing quote)")
        text = self.source[start:self.pos]
        self.pos += 1  # skip closing quote
        return text

    # Read an identifier: letters, digits, and underscores.
    def read_identifier(self):
        start = self.pos
        while self.pos < len(self.source) and \
              (self.source[self.pos].isalnum() or self.source[self.pos] == "_"):
            self.pos += 1
        return self.source[start:self.pos]

    # Return the character right after the cursor, or "" at end of input.
    def peek_char(self):
        next_pos = self.pos + 1
        if next_pos < len(self.source):
            return self.source[next_pos]
        return ""


if __name__ == "__main__":
    source = 'x = "Hello, World!"'
    for token in Lexer(source).tokenize():
        print(token)