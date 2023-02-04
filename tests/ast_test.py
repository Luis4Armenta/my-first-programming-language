from unittest import TestCase
from lp.ast import(
  Identifier,
  LetStatement,
  ReturnStatement,
  Program,
  Expression,
  ExpressionStatement,
  Integer
)
from lp.token import Token, TokenType

class ASTTest(TestCase):
  
  def test_let_statement(self) -> None:
    # variable mi_var = otra_var;
    
    program: Program = Program(statements=[
      LetStatement(
        token=Token(TokenType.LET, 'variable'),
        name=Identifier(Token(TokenType.IDENT, 'mi_var'), 'mi_var'),
        value=Identifier(Token(TokenType.IDENT, 'otra_var'), 'otra_var')
      )
    ])
    
    program_str = str(program)

    self.assertEquals(program_str, 'variable mi_var = otra_var;')
    
  def test_return_statement(self) -> None:
    # regresa x;
    
    program: Program = Program(statements=[
      ReturnStatement(
        token=Token(TokenType.RETURN, 'regresa'),
        return_value = Expression(Token(TokenType.IDENT, 'x'))
      )
    ])
    
    program_str = str(program)

    self.assertEquals(program_str, 'regresa x;')
  
  def test_identifier_expression(self) -> None:
    # variable total = 5;
    
    program: Program = Program(statements=[
      LetStatement(
        token=Token(TokenType.LET, 'variable'),
        name=Identifier(Token(TokenType.IDENT, 'total'), 'total'),
        value=Integer(Token(TokenType.INT, '5'), value=5)
      )
    ])
    
    program_str = str(program)
    self.assertEquals(program_str, 'variable total = 5;')