def is_alpha_lower(char):
    if not char:
        return False
    if "a" <= char <= "z":#This compares ASCII values
        return True
    return False

def is_alpha_upper(char):
    if not char:
        return False
    if "A" <= char <= "Z":#This compares ASCII values
        return True
    return False

def is_digit(char):
    if not char:
        return False
    if "0" <= char <= "9":#This compares ASCII values
        return True
    return False

def is_aldigit(char):
    if is_alpha_lower(char) or is_alpha_upper(char):
        return True
    elif is_alpha_upper(char):
        return True
    elif is_digit(char):
        return True
    else:
        return False


def isspace(s):
    for char in s:
        # print(char)
        if char not in (" ", "\n", "\r"): # each line end with \r\n, carriage return(moves cursor to end of line) + newline
            return False
    return True


def is_identifier(token: str) -> bool:
    # Constants
    Q0 = 0
    F = [2]
    Q = range(3)

    SIGMA = {
        "LETTER_UPPER": 0,
        "LETTER_LOWER": 1,
        "UNDERSCORE": 2,
        "DIGIT": 3,
        "OTHER": 4,
    }

    # Transition table
    DELTA = [
        [2, 2, 2, 1, 1], # Transitions from state 0
        [1, 1, 1, 1, 1],  # Transitions from state 1 (trap state)
        [2, 2, 2, 2, 1],  # Transitions from state 2 
    ]

    # Evaluate Char
    def carasimbolo(char: str) -> int:
        if is_alpha_upper(char): 
            return SIGMA["LETTER_UPPER"]
        if is_alpha_lower(char): 
            return SIGMA["LETTER_LOWER"]
        elif is_digit(char): 
            return SIGMA["DIGIT"]
        elif char == "_":
            return SIGMA["UNDERSCORE"]
        else:
            return SIGMA["OTHER"]

    estado_actual = Q0
    i1 = 0

    while i1 < len(token) and estado_actual != 1:
        estado_actual = DELTA[estado_actual][carasimbolo(token[i1])]
        i1 += 1

    return estado_actual in F

def is_integer(token : str)-> bool:
    # Constants
    Q0 = 0
    F = [3]
    Q = range(4)

    SIGMA = {
        "DIGIT": 0,
        "MINUS": 1,
        "OTHER": 2,
    } 
    # Transition Table

    DELTA = [
        [3, 1, 2],  # Trans Q0
        [3, 2, 2],  # Trans Q1
        [2, 2, 2],  # Trans Q2, trap state
        [3, 2, 2],  # Trans Q3
    ]

    # Evaluate Char

    def carasimbolo(char: str) -> int:
        if is_digit(char):  # if char in [A..z] might be replaced by custom
            return SIGMA["DIGIT"]
        elif char == "-":
            return SIGMA["MINUS"]
        else:
            return SIGMA["OTHER"]

    # Iterate
    estado_actual = Q0
    i1 = 0

    while i1 < len(token) and estado_actual != 2:
        estado_actual = DELTA[estado_actual][carasimbolo(token[i1])]
        i1 += 1

    return estado_actual in F

def is_real(token : str)->bool:
    Q0 = 0
    F = [6,7]
    Q = range(9)

    SIGMA = {
        "DIGIT": 0,
        "MINUS": 1,
        "POINT": 2,
        "E": 3,
        "e": 4,
        "OTHER": 5,
    }

    # Transition table
    DELTA = [
        [2, 8, 1, 1, 1, 1],  # Trans Q0
        [1, 1, 1, 1, 1, 1],  # Trans Q1, trap state
        [2, 1, 5, 3, 3, 1],  # Trans Q2
        [7, 4, 1, 1, 1, 1],  # Trans Q3
        [7, 1, 1, 1, 1, 1],  # Trans Q4
        [6, 1, 1, 1, 1, 1],  # Trans Q5
        [6, 1, 1, 3, 3, 1],  # Trans Q6
        [7, 1, 1, 1, 1, 1],  # Trans Q7
        [2, 1, 1, 1, 1, 1],  # Trans Q8
    ]

    def carasimbolo(char: str) -> int:
        if is_digit(char):
            return SIGMA["DIGIT"]
        elif char == "-":
            return SIGMA["MINUS"]
        elif char == ".":
            return SIGMA["POINT"]
        elif char == "E":
            return SIGMA["E"]
        elif char == "e":
            return SIGMA["e"]
        else:
            return SIGMA["OTHER"]

    # Iterate
    estado_actual = Q0
    i1 = 0

    while i1 < len(token) and estado_actual != 1:
        estado_actual = DELTA[estado_actual][carasimbolo(token[i1])]
        i1 += 1

    return estado_actual in F

class LexicalAnalyzer:
    FinArch = '\0'

    def __init__(self, filename):
        self.source_code = self.load_source_code(filename)
        self.control = 0

    def load_source_code(self, filename):
        with open(filename, 'r') as file:
            return file.read()

    def read_car(self):
        """
        Reads the next character from the source code.
        Returns the special end-of-file character if the end of the file is reached.
        """
        if self.control < len(self.source_code):
            car = self.source_code[self.control]
            self.control += 1
        else:
            car = self.FinArch
        return car

    def read_token(self):
        """
        Reads the next token from the source code.
        A token is defined as a sequence of alphanumeric characters and underscores.
        Non-alphanumeric characters are treated as separate tokens.
        """
        token = ""
        while True:
            car = self.read_car()
            # print(car)
            if car == self.FinArch or isspace(car):
                if token:
                    return token
                if car == self.FinArch:
                    return None
            elif not is_aldigit(car) and car not in {"_","."}:
                if token:
                    self.control -= 1  # Put back the non-alphanumeric character for next token rea)
                    return token
                else:
                    token = car
                    return token
            else:
                token += car

    def analyze(self):
        """
        Analyzes the source code by reading and classifying tokens.
        """
        while True:
            token = self.read_token()
            if token is None:
                break
            elif is_identifier(token):
                print(f"{token} : Identifier")
            elif is_integer(token):
                print(f"{token} : Integer")
            elif is_real(token):
                print(f"{token} : Real")
            else:
                print(f"{token} : Invalid")


# Example usage:
analyzer = LexicalAnalyzer("tokens.txt")
analyzer.analyze()
