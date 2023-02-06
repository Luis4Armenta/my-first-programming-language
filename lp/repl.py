import readline
from typing import List
from os import system, name

from lp.ast import Program
from lp.evaluator import evaluate
from lp.lexer import Lexer
from lp.parser import Parser
from lp.token import Token, TokenType
from lp.object import Environment

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
  scanned: List[str] = []
  
  while (source := input('>> ')) != 'salir()':
    if source == 'limpiar()':
      _clear_screen()
    else:
      scanned.append(source)
      lexer: Lexer = Lexer(' '.join(scanned))
      parser: Parser = Parser(lexer)
      
      program: Program = parser.parse_program()
      env: Environment = Environment()
      
      if len(parser.errors) > 0:
        _print_parse_errors(parser.errors)
        continue

      evaluated = evaluate(program, env)
      
      if evaluated is not None:
        print(evaluated.inspect())
