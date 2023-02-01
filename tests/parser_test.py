from unittest import TestCase

from lp.lexer import Lexer
from lp.parser import Parser
from lp.ast import Program

class ParserTest(TestCase):

  def test_parse_program(self) -> None:
    source: str = 'variable x = 5'
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)
    
    program: Program = parser.parse_program()
    
    self.assertIsNotNone(program)
    self.assertIsInstance(program, Program)

