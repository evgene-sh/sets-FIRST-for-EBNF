from lexer import Lexer
from parser import Parser
from first import get_first
from sys import argv


lexer = Lexer(argv[1])
parser = Parser()
mass = parser.get_formulas(lexer.tokens)
print(get_first(mass))