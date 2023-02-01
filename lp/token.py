from enum import (
  auto,
  Enum,
  unique,
)
from typing import Dict, NamedTuple

@unique
class TokenType(Enum):
  ASSING = auto()
  COMMA = auto()
  ELSE = auto()
  EOF = auto()
  FALSE = auto()
  FUNCTION = auto()
  IDENT = auto()
  IF = auto()
  ILLEGAL = auto()
  INT = auto()
  LBRACE = auto()
  LET = auto()
  LPAREN = auto()
  LT = auto()
  PLUS = auto()
  RBRACE = auto()
  RPAREN = auto()
  RETURN = auto()
  SEMICOLON = auto()
  TRUE = auto()

class Token(NamedTuple):
  token_type: TokenType
  literal: str

  def __str__(self) -> str:
    return f'Type: {self.token_type}, Literal: {self.literal}'

def lookup_token_type(literal: str) -> TokenType:
  keywords: Dict[str, TokenType] = {
    'falso': TokenType.FALSE,
    'procedimiento': TokenType.FUNCTION,
    'regresa': TokenType.RETURN,
    'si': TokenType.IF,
    'si_no': TokenType.ELSE,
    'variable': TokenType.LET,
    'verdadero': TokenType.TRUE,
  }
  
  return keywords.get(literal, TokenType.IDENT)