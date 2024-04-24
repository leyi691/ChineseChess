class StepError(Exception):
    def __init__(self):
        self.message = "Invalid move."
        super().__init__(self.message)


class InvalidTurnError(Exception):
    def __init__(self, message=None):
        self.message = f"No such turn: {message}."
        super().__init__(self.message)


class ColorError(Exception):
    def __init__(self, message=None):
        self.message = f"Invalid color: {message}."
        super().__init__(self.message)


class NoneException(Exception):
    def __init__(self, obj, message=None):
        self.message = f"Object {obj} is None: {message}."
