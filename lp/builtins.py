from typing import (
  cast,
  Dict
)

from lp.object import (
  Builtin,
  Error,
  Integer,
  Object,
  String
)

_WRONG_NUMBER_OF_ARGS = 'Numero incorrecto de argumentos para longitud, se recibieron {}, se requieren {}'
_UNSUPPORTED_ARGUMENT_TYPE = 'Argumento para longitud sin soporte, se recibio {}'

def longitud(*args: Object) -> Object:
  if len(args) != 1:
    return Error(_WRONG_NUMBER_OF_ARGS.format(len(args), 1))
  elif type(args[0]) == String:
    argument = cast(String, args[0])
    
    return Integer(len(argument.value))
  else:
    return Error(_UNSUPPORTED_ARGUMENT_TYPE.format(args[0].type().name))
  return Integer(22)

BUILTINS: Dict[str, Builtin] = {
  'longitud': Builtin(fn=longitud)
}