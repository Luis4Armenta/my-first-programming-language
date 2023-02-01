from lp.lexer import Lexer
from lp.ast import Program

class Parser:
  
  def __init__(self, lexer: Lexer) -> None:
    self._lexer = lexer

  def parse_program(self) -> Program:
    program: Program = Program(statements=[])
    
    return program
