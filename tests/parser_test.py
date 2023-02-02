from unittest import TestCase
from typing import List, cast

from lp.lexer import Lexer
from lp.parser import Parser
from lp.ast import Program, LetStatement, Statement, Identifier
from lp.token import Token, TokenType

class ParserTest(TestCase):

  def test_parse_program(self) -> None:
    source: str = 'variable x = 5;'
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)
    
    program: Program = parser.parse_program()
    
    self.assertIsNotNone(program)
    self.assertIsInstance(program, Program)
    
  def test_let_statements(self) -> None:
    source: str = '''
      variable x = 5;
      variable y = 10;
      variable foo = 20;
    '''
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)
    
    program: Program = parser.parse_program()
    
    self.assertEquals(len(program.statements), 3)
    
    for statement in program.statements:
      self.assertEqual(statement.token_literal(), 'variable')
      self.assertIsInstance(statement, LetStatement)
      
  def test_correct_let_statements_identities(self) -> None:
    source: str = '''
      variable x = 5;
      variable y = 10;
      variable foo = 20;
    '''
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)
    
    program: Program = parser.parse_program()
    
    identifiers: List[str] = []
    for statement in program.statements:
      self.assertIsInstance(statement, LetStatement)
      identifiers.append(str(statement).split(' ')[1])
    
    expected_identifiers: List[str] = [
      'x', 'y', 'foo'
    ]
    
    self.assertEquals(identifiers, expected_identifiers)
  
  def test_names_in_let_statements(self) -> None:
    source: str = '''
        variable x = 5;
        variable y = 10;
        variable foo = 20;
    '''
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)
    program: Program = parser.parse_program()
    names: List[str] = []
    for statement in program.statements:
        statement = cast(LetStatement, statement)
        assert statement.name is not None
        names.append(statement.name.value)
    expected_names: List[str] = ['x', 'y', 'foo']
    self.assertEquals(names, expected_names)


