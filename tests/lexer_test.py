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