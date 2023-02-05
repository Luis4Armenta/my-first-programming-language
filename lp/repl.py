import readline
from typing import List
from os import system, name

from lp.ast import Program
from lp.evaluator import evaluate
from lp.lexer import Lexer
from lp.parser import Parser
from lp.token import Token, TokenType

EOF_TOKEN: Token = Token(TokenType.EOF, '')

def _clear_screen() -> None:
  if name == 'nt':
    _ = system('cls')
  else:
    _ = system('clear')

def _print_parse_errors(errors: List[str]) -> None:
  for error in errors:
    print(error)

def start_repl() -> None:
  while (source := input('>> ')) != 'salir()':
    if source == 'limpiar()':
      _clear_screen()
    else:
      lexer: Lexer = Lexer(source)
      parser: Parser = Parser(lexer)
      
      program: Program = parser.parse_program()
      
      if len(parser.errors) > 0:
        _print_parse_errors(parser.errors)
        continue

      evaluated = evaluate(program)
      
      if evaluated is not None:
        print(evaluated.inspect())
