from os import read, write
from sock_util import *
import math
from dataclasses import dataclass

__all__ = [
    "handle"
]

@dataclass
class Error:
    error_message: str

@dataclass
class Success:
    success_message: str

NOT_ENOUGH_ARGUMENTS = "Not enough arguments: expected %s, found %s"
VALUE_ERROR = "Value Error: Expected string but got \"%s\""
UNKNOWN_COMMAND = "Unknown Command: %s" 

def main():
    s = server_connect("127.0.0.1", 8080)
    while True:
        server_accept()
        while (True):

            tokens = s.recv(1024).decode().split()
            if len(tokens) == 0:
                continue
            command = tokens[0]
            match command:
                case "help":
                    s.send(__print_help().encode())
                    continue
                case "floor":
                    result = __handle_floor(tokens)
                case "ceil":
                    result = __handle_ceil(tokens)
                case "cos": 
                    result = __handle_cos(tokens)
                case "sin":
                    result = __handle_sin(tokens)
                case _:
                    result = Error(UNKNOWN_COMMAND % command)
            if type(result) is Error:
                msg = f"error: {result.error_message}"
            else:
                msg = f"success: {result.success_message}"
            s.send(msg.encode())

def __print_help() -> str:
    return  """
    floor <float>       : Floors a number
    ceil <float>        : Ceils a number
    cos <float>         : Cosine of a number
    sin <float>         : Sin of a number""" 

def __validate(tokens: list[str], num_tokens: int) -> Error|list[int]:
    size = len(tokens) - 1
    if size != num_tokens:
        return Error(NOT_ENOUGH_ARGUMENTS % (num_tokens, size))
    out = [0] * size
    try:
        for i in range(size):
            out[i] = float(tokens[i+1])
    except ValueError:
        return Error(VALUE_ERROR % tokens[i+1])
    return out

def __handle_floor(tokens) -> Error|Success:
    clean_tokens = __validate(tokens, 1)
    if type(clean_tokens) is Error:
        return clean_tokens
    return Success(str(math.floor(*clean_tokens)))

def __handle_ceil(tokens) -> Error|Success:
    clean_tokens = __validate(tokens, 1)
    if type(clean_tokens) == Error:
        return clean_tokens
    return Success(str(math.ceil(*clean_tokens)))

def __handle_cos(tokens) -> Error|Success:
    clean_tokens = __validate(tokens, 1)
    if type(clean_tokens) == Error:
        return clean_tokens
    return Success(str(math.cos(*clean_tokens)))

def __handle_sin(tokens) -> Error|Success:
    clean_tokens = __validate(tokens, 1)
    if type(clean_tokens) == Error:
        return clean_tokens
    return Success(str(math.sin(*clean_tokens)))

main()