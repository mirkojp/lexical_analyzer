import os
#these ones could be saved into another file then, ikmported
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
        if char not in (" ", "\n","\r"): # each line end with \r\n, carriage return(moves cursor to end of line) + newline
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

    #could had made an 
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
        A token is defined as a sequence of alphanumeric characters,dots and underscores.
        Non-alphanumeric characters are treated as separate tokens.
        """
        token = ""
        string = 0

        while True:
            car = self.read_car()
            # print(car)
            # print(string)
            # print(token)
            # input()

            #This evalutes if it is a string
            if car in ['"',"'"] and string == 0: # Opening of string
                if token: #Token exists example abc", returns abc as token preparas for start of string
                    self.control -= 1
                    return token
                else:#Tokens doesn't exists, makes string 1 to indicate that we are working with string
                    token += car
                    string = 1

            elif string == 1: #Working over a string
                if car in ['"',"'"]: # End of string, adds car ("), and updates string indicator
                    token += car
                    string = 0
                    return token
                else: #Not end of string, adds car to token
                    token += car

            elif car == self.FinArch or isspace(car): #\0  or \r\n  " "
                if token:
                    return token
                if car == self.FinArch:
                    return None
                
            elif not is_aldigit(car) and car not in {"_","."}:
                if token: #token already being build, means car is the end of the token
                    self.control -= 1  # Put back the non-alphanumeric character for next token read
                    return token
                else:  # token not being build, car is token
                    token = car
                    return token
            else:
                token += car

    # def analyze(self):
    #     """
    #     Analyzes the source code by reading and classifying tokens.
    #     """
    #     while True:
    #         token = self.read_token()
    #         if token is None:
    #             input()
    #             break
    #         elif is_identifier(token):
    #             print(f"{token} : Identifier")
    #         elif is_integer(token):
    #             print(f"{token} : Integer")
    #         elif is_real(token):
    #             print(f"{token} : Real")
    #         else:
    #             print(f"{token} : Invalid")
    #     input()


    def analyze(self):
        """
        Analyzes the source code by reading and classifying tokens.
        """
        with open("analyze_output.txt", "w") as output_file:
            while True:
                token = self.read_token()
                if token is None:
                    break
                elif is_identifier(token):
                    output_file.write(f"{token} : Identifier\n")
                elif is_integer(token):
                    output_file.write(f"{token} : Integer\n")
                elif is_real(token):
                    output_file.write(f"{token} : Real\n")
                else:
                    output_file.write(f"{token} : Invalid\n")


# Example usage:
if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    rel_path = "tokens.txt"
    abs_file_path = os.path.join(script_dir, rel_path)

    analyzer = LexicalAnalyzer(abs_file_path)
    analyzer.analyze()

    # analyzer = LexicalAnalyzer("tokens.txt")
    # analyzer.analyze()
