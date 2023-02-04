from enum import IntEnum
from typing import Optional, List, Callable, Dict

from lp.lexer import Lexer
from lp.ast import (
  Program,
  Statement,
  LetStatement,
  Identifier, 
  ReturnStatement,
  Expression,
  ExpressionStatement,
  Integer
)
from lp.token import Token, TokenType

PrefixParsFn = Callable[[], Optional[Expression]]
InfixParsFn = Callable[[Expression], Optional[Expression]]
PrefixParsFns = Dict[TokenType, PrefixParsFn]
InfixParsFns = Dict[TokenType, InfixParsFn]

class Precedence(IntEnum):
  LOWEST = 1
  EQUALS = 2
  LESSGRATER = 3
  SUM = 4
  PRODUCT = 5
  PREFIX = 6
  CALL = 7

class Parser:
  
  def __init__(self, lexer: Lexer) -> None:
    self._lexer = lexer
    self._current_token: Optional[Token] = None
    self._peek_token: Optional[Token] = None
    self._errors: List[str] = []
    
    self._prefix_parse_fns: PrefixParsFns = self._register_prefix_fns()
    self._infix_parse_fns: InfixParsFns = self._register_infix_fns()
    self._advance_tokens()
    self._advance_tokens()
    
  @property
  def errors(self) -> List[str]:
    return self._errors

  def parse_program(self) -> Program:
    program: Program = Program(statements=[])
    
    assert self._current_token is not None
    while self._current_token.token_type != TokenType.EOF:
      statement = self._parse_statement()
      if statement is not None:
        program.statements.append(statement)
        
      self._advance_tokens()
    
    return program

    
  def _advance_tokens(self) -> None:
    self._current_token = self._peek_token
    self._peek_token = self._lexer.next_token()
    
  def _expected_token(self, token_type: TokenType) -> bool:
    assert self._peek_token is not None
    if self._peek_token.token_type == token_type:
      self._advance_tokens()
      return True
   
    self._expected_token_error(token_type)
    return False
  
  def _expected_token_error(self, token_type: TokenType) -> None:
    assert self._peek_token is not None
    error = f'Se esperaba que el siguiente token fuera {token_type},' + \
      f' pero se obtuvo {self._peek_token.token_type}'

    self._errors.append(error)
    
  def _parse_expression(self, precedece: Precedence)  -> Optional[Expression]:
    assert self._current_token is not None
    try:
      prefix_parse_fn = self._prefix_parse_fns[self._current_token.token_type]
    except KeyError:
      return None
    
    left_expression = prefix_parse_fn()
    
    return left_expression
    
  def _parse_expression_statement(self) -> Optional[ExpressionStatement]:
    assert self._current_token is not None
    expression_statement = ExpressionStatement(self._current_token)
    
    expression_statement.expression = self._parse_expression(Precedence.LOWEST)
    
    assert self._peek_token is not None
    if self._peek_token.token_type == TokenType.SEMICOLON:
      self._advance_tokens()
      
    return expression_statement
  
  def _parse_identifier(self) -> Identifier:
    assert self._current_token is not None
    
    return Identifier(self._current_token, value=self._current_token.literal)
  
  def _parse_integer(self) -> Optional[Integer]:
    assert self._current_token is not None
    integer = Integer(self._current_token)
    
    try:
      integer.value = int(self._current_token.literal)
    except ValueError:
      message = f'No se ha podido parsear {self._current_token.literal} ' +\
        'como entero.'
        
      self._errors.append(message)
      
      return None
    
    return integer
    
  def _parse_let_statement(self) -> Optional[LetStatement]:
    assert self._current_token is not None
    let_statment: LetStatement = LetStatement(token=self._current_token)
    
    if not self._expected_token(TokenType.IDENT):
      return None
    
    let_statment.name = self._parse_identifier()
    
    if not self._expected_token(TokenType.ASSING):
      return None
    
    # TODO
    # Terinar cuando sepamos parsear expresiones
    
    while self._current_token.token_type != TokenType.SEMICOLON:
      self._advance_tokens()
      
    return let_statment
  
  def _parse_return_statement(self) -> Optional[ReturnStatement]:
    assert self._current_token is not None
    return_statement = ReturnStatement(token=self._current_token)
    
    self._advance_tokens()
    
    #TODO: Terminar cuando sepamos parsear expresiones
    
    while self._current_token.token_type != TokenType.SEMICOLON:
      self._advance_tokens()
      
    return return_statement
  
  
  def _parse_statement(self) -> Optional[Statement]:
    assert self._current_token is not None
    if self._current_token.token_type == TokenType.LET:
      return self._parse_let_statement()
    elif self._current_token.token_type == TokenType.RETURN:
      return self._parse_return_statement()
    else:
      return self._parse_expression_statement()
  
  def _register_infix_fns(self) -> InfixParsFns:
    return {}
  
  def _register_prefix_fns(self) -> PrefixParsFns:
    return {
      TokenType.IDENT: self._parse_identifier,
      TokenType.INT: self._parse_integer
    }
