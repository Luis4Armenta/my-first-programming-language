from re import match

from lp.token import (
  Token,
  TokenType,
  lookup_token_type
)

class Lexer:
  def __init__(self, source: str) -> None:
    self._source: str = source
    self._character: str = ''
    self._read_position: int = 0
    self._position:int = 0

    self._read_character()
  
  def next_token(self) -> Token:
    self._skip_whitespace()
    
    if match(r'^=$', self._character):
      token = Token(TokenType.ASSING, self._character)
    elif match(r'^\+$', self._character):
      token = Token(TokenType.PLUS, self._character)
    elif match(r'^$', self._character):
      token = Token(TokenType.EOF, self._character)
    elif match(r'^\($', self._character):
      token = Token(TokenType.LPAREN, self._character)
    elif match(r'^\)$', self._character):
      token = Token(TokenType.RPAREN, self._character)
    elif match(r'^\{$', self._character):
      token = Token(TokenType.LBRACE, self._character)
    elif match(r'^\}$', self._character):
      token = Token(TokenType.RBRACE, self._character)
    elif match(r'^,$', self._character):
      token = Token(TokenType.COMMA, self._character)
    elif match(r'^;$', self._character):
      token = Token(TokenType.SEMICOLON, self._character)
    elif self._is_letter(self._character):
      literal = self._read_identifier()
      token_type = lookup_token_type(literal)
      
      return Token(token_type, literal)
    elif self._is_number(self._character):
      literal = self._read_number()

      return Token(TokenType.INT, literal)
    elif match(r'^<$', self._character):
      token = Token(TokenType.LT, self._character)
    else: 
      token =  Token(TokenType.ILLEGAL, self._character)

    self._read_character()

    return token
  
  def _is_letter(self, character: str) -> bool:
    return bool(match(r'^[a-záéíóúA-ZÁÉÍÓÚñÑ_]$', character))
  
  def _is_number(self, character: str) -> bool:
    return bool(match(r'^\d$', character))

  def _read_character(self) -> None:
    if self._read_position >= len(self._source):
      self._character = ''
    else:
      self._character = self._source[self._read_position]

      self._position = self._read_position
      self._read_position += 1
      
  def _read_identifier(self) -> str:
    initial_position = self._position
    
    while self._is_letter(self._character):
      self._read_character()
      
    return self._source[initial_position: self._position]
  
  def _read_number(self) -> str:
    initial_position = self._position
    
    while self._is_number(self._character):
      self._read_character()
      
    return self._source[initial_position : self._position]
  
  def _skip_whitespace(self) -> None:
    while match(r'^\s$', self._character):
      self._read_character()