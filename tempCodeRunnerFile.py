
    def analyze(self):
        """
        Analyzes the source code by reading and classifying tokens.
        """
        while True:
            token = self.read_token()
            if token is None:
                input()
                break
            elif is_identifier(token):
                print(f"{token} : Identifier")
            elif is_integer(token):
                print(f"{token} : Integer")
            elif is_real(token):
                print(f"{token} : Real")
            else:
                print(f"{token} : Invalid")
        input()