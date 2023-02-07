from unittest import TestCase
from typing import List

from lp.token import (
  Token,
  TokenType
)

from lp.lexer import Lexer

class TexerTest(TestCase):
  def test_illegal(self) -> None:
    source: str = '¡¿@'
    lexer: Lexer = Lexer(source)


    tokens: List[Token] = []
    for i in range(len(source)):
      tokens.append(lexer.next_token())

    expected_tokens: List[Token] = [
      Token(TokenType.ILLEGAL, '¡'),
      Token(TokenType.ILLEGAL, '¿'),
      Token(TokenType.ILLEGAL, '@'),
    ]

    self.assertEquals(tokens, expected_tokens)
  
  def test_one_character_operator(self) -> None:
    source: str = '=+-*/<>!%'
    lexer: Lexer = Lexer(source)
    
    tokens: List[Token] = []
    for i in range(len(source)):
      tokens.append(lexer.next_token())
      
    expected_tokens: List[Token] = [
      Token(TokenType.ASSING, '='),
      Token(TokenType.PLUS, '+'),
      Token(TokenType.MINUS, '-'),
      Token(TokenType.MULTIPLICATION, '*'),
      Token(TokenType.DIVISION, '/'),
      Token(TokenType.LT, '<'),
      Token(TokenType.GT, '>'),
      Token(TokenType.NEGATION, '!'),
      Token(TokenType.MOD, '%'),
    ]
    
    self.assertEquals(tokens, expected_tokens)
    
  def test_eof(self) -> None:
    source: str = '+'
    lexer: Lexer = Lexer(source)
    
    tokens: List[Token] = []
    for i in range(len(source) + 1):
      tokens.append(lexer.next_token())

    expected_tokens: List[Token] = [
      Token(TokenType.PLUS, '+'),
      Token(TokenType.EOF, ''),
    ]
    
    self.assertEquals(tokens, expected_tokens)
  
  def test_delimiters(self) -> None:
    source: str = '(){},;'
    lexer: Lexer = Lexer(source)
    
    tokens: List[Token] = []
    for _ in range(len(source)):
      tokens.append(lexer.next_token())
      
    expected_tokens: List[Token] = [
      Token(TokenType.LPAREN, '('),
      Token(TokenType.RPAREN, ')'),
      Token(TokenType.LBRACE, '{'),
      Token(TokenType.RBRACE, '}'),
      Token(TokenType.COMMA, ','),
      Token(TokenType.SEMICOLON, ';'),
    ]
    
    self.assertEquals(tokens, expected_tokens)
    
  def test_assignment(self) -> None:
    source: str = '''
      variable cinco = 5;
      variable num_1 = 1;
    '''
    lexer: Lexer = Lexer(source)
    
    tokens: List[Token] = []
    for _ in range(10):
      tokens.append(lexer.next_token())
      
    expected_tokens: List[Token] = [
      Token(TokenType.LET, 'variable'),
      Token(TokenType.IDENT, 'cinco'),
      Token(TokenType.ASSING, '='),
      Token(TokenType.INT, '5'),
      Token(TokenType.SEMICOLON, ';'),
      Token(TokenType.LET, 'variable'),
      Token(TokenType.IDENT, 'num_1'),
      Token(TokenType.ASSING, '='),
      Token(TokenType.INT, '1'),
      Token(TokenType.SEMICOLON, ';'),
    ]
    
    self.assertEquals(tokens, expected_tokens)
    
  def test_function_declaration(self) -> None:
    source: str = '''
      variable suma = procedimiento(x, y) {
        x + y;
      };
    '''
    lexer: Lexer = Lexer(source)
    
    tokens: List[Token] = []
    for _ in range(16):
      tokens.append(lexer.next_token())

    expected_tokens: List[Token] = [
      Token(TokenType.LET, 'variable'),
      Token(TokenType.IDENT, 'suma'),
      Token(TokenType.ASSING, '='),
      Token(TokenType.FUNCTION, 'procedimiento'),
      Token(TokenType.LPAREN, '('),
      Token(TokenType.IDENT, 'x'),
      Token(TokenType.COMMA, ','),
      Token(TokenType.IDENT, 'y'),
      Token(TokenType.RPAREN, ')'),
      Token(TokenType.LBRACE, '{'),
      Token(TokenType.IDENT, 'x'),
      Token(TokenType.PLUS, '+'),
      Token(TokenType.IDENT, 'y'),
      Token(TokenType.SEMICOLON, ';'),
      Token(TokenType.RBRACE, '}'),
      Token(TokenType.SEMICOLON, ';'),
    ]
    
    self.assertEquals(tokens, expected_tokens)

  def test_function_call(self) -> None:
    source: str = 'variable resultado = suma(dos, tres);'
    lexer: Lexer = Lexer(source)
    
    tokens: List[Token] = []
    for _ in range(10):
      tokens.append(lexer.next_token())
      
    expected_tokens: List[Token] = [
      Token(TokenType.LET, 'variable'),
      Token(TokenType.IDENT, 'resultado'),
      Token(TokenType.ASSING, '='),
      Token(TokenType.IDENT, 'suma'),
      Token(TokenType.LPAREN, '('),
      Token(TokenType.IDENT, 'dos'),
      Token(TokenType.COMMA, ','),
      Token(TokenType.IDENT, 'tres'),
      Token(TokenType.RPAREN, ')'),
      Token(TokenType.SEMICOLON, ';'),
    ]
    
    self.assertEquals(tokens, expected_tokens)
    
  def test_control_statement(self) -> None:
    source: str = '''
      si (5 < 10) {
        regresa verdadero;
      } si_no {
        regresa falso;
      }
    '''
    lexer: Lexer = Lexer(source)
    
    tokens: List[Token] = []
    for _ in range(17):
      tokens.append(lexer.next_token())
      
    expected_tokens: List[Token] = [
      Token(TokenType.IF, 'si'),
      Token(TokenType.LPAREN, '('),
      Token(TokenType.INT, '5'),
      Token(TokenType.LT, '<'),
      Token(TokenType.INT, '10'),
      Token(TokenType.RPAREN, ')'),
      Token(TokenType.LBRACE, '{'),
      Token(TokenType.RETURN, 'regresa'),
      Token(TokenType.TRUE, 'verdadero'),
      Token(TokenType.SEMICOLON, ';'),
      Token(TokenType.RBRACE, '}'),
      Token(TokenType.ELSE, 'si_no'),
      Token(TokenType.LBRACE, '{'),
      Token(TokenType.RETURN, 'regresa'),
      Token(TokenType.FALSE, 'falso'),
      Token(TokenType.SEMICOLON, ';'),
      Token(TokenType.RBRACE, '}'),
    ]
    
    self.assertEquals(tokens, expected_tokens)
    
  def test_two_character_operator(self) -> None:
    source: str = '''
      10 == 10;
      10 != 9;
      10 >= 10;
      9 <= 10;
    '''
    lexer: Lexer = Lexer(source)
    
    tokens: List[Token] = []
    for _ in range(16):
      tokens.append(lexer.next_token())
      
    expected_tokens: List[Token] = [
      Token(TokenType.INT, '10'),
      Token(TokenType.EQ, '=='),
      Token(TokenType.INT, '10'),
      Token(TokenType.SEMICOLON, ';'),
      Token(TokenType.INT, '10'),
      Token(TokenType.NOT_EQ, '!='),
      Token(TokenType.INT, '9'),
      Token(TokenType.SEMICOLON, ';'),
      Token(TokenType.INT, '10'),
      Token(TokenType.G_OR_EQ, '>='),
      Token(TokenType.INT, '10'),
      Token(TokenType.SEMICOLON, ';'),
      Token(TokenType.INT, '9'),
      Token(TokenType.L_OR_EQ, '<='),
      Token(TokenType.INT, '10'),
      Token(TokenType.SEMICOLON, ';'),
    ]

    self.assertEquals(tokens, expected_tokens)
    
  def test_string(self) -> None:
    source: str = '''
      "foo";
      "No me esperaba encontrar este proyecto en platzi";
    '''
    
    lexer: Lexer = Lexer(source)
    
    tokens: List[Token] = []
    for i in range(4):
      tokens.append(lexer.next_token())
    
    expected_token: List[Token] = [
      Token(TokenType.STRING, 'foo'),
      Token(TokenType.SEMICOLON, ';'),
      Token(TokenType.STRING, 'No me esperaba encontrar este proyecto en platzi'),
      Token(TokenType.SEMICOLON, ';'),
    ]
    
    self.assertEquals(tokens, expected_token)
