import pathlib
import os
def is_integer(token):
    state = 0
    for char in token:
        if state == 0:
            if char == '-':
                state = 1
            elif char.isdigit():
                state = 2
            else:
                return False
        elif state == 1:
            if char.isdigit():
                state = 2
            else:
                return False
        elif state == 2:
            if not char.isdigit():
                return False
    return state == 2

# def is_real(token):
#     state = 0
#     for char in token:
#         if state == 0:
#             if char == '-':
#                 state = 1
#             elif char.isdigit():
#                 state = 2
#             else:
#                 return False
#         elif state == 1:
#             if char.isdigit():
#                 state = 2
#             else:
#                 return False
#         elif state == 2:
#             if char.isdigit():
#                 state = 2
#             elif char == '.':
#                 state = 3
#             else:
#                 return False
#         elif state == 3:
#             if char.isdigit():
#                 state = 4
#             else:
#                 return False
#         elif state == 4:
#             if char.isdigit():
#                 state = 4
#             elif char in 'eE':
#                 state = 5
#             else:
#                 return False
#         elif state == 5:
#             if char in '+-':
#                 state = 6
#             elif char.isdigit():
#                 state = 6
#             else:
#                 return False
#         elif state == 6:
#             if not char.isdigit():
#                 return False
#     return state in {2, 4, 6}

def is_identifier(token):
    state = 0
    for char in token:
        if state == 0:
            if char.isalpha() or char == '_':
                state = 1
            else:
                return False
        elif state == 1:
            if not (char.isalnum() or char == '_'):
                return False
    return state == 1

def identify_token(token):
    if is_integer(token):
        return 'Entero'
    # elif is_real(token):
    #     return 'Real'
    elif is_identifier(token):
        return 'Identificador'
    else:
        return 'Desconocido'

def read_tokens_from_file_token(filename):
        with open(os.path.join(BASE_DIR,filename), 'r') as file:
            content = file.read()
        return content.split()

def read_tokens_from_file_lines(filename):
        with open(os.path.join(BASE_DIR,filename), 'r') as file:
            lines = file.readlines()
        return lines

if __name__ == "__main__":

    BASE_DIR = pathlib.Path(__file__).resolve().parent

    # def read_tokens_from_file(filename):
    #     with open(filename,"r")as file:
    #         content = file.read()
    #     return content.split()

    filename = 'tokens.txt'  # Make sure this file exists and has the tokens
    tokens = read_tokens_from_file_token(filename)
    lines = read_tokens_from_file_lines(filename)

    print("Tokenization")
    print(tokens)
    print("Linezation")
    print(lines)

    for token in tokens:
        tipo = identify_token(token)
        print(f'Token: {token}, Tipo: {tipo}')

    