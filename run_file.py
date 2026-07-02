import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

with open(sys.argv[1]) as f:
    source = f.read()

tokens = Lexer(source).tokenize()
tree = Parser(tokens).parse()
Interpreter(tree).interpret()