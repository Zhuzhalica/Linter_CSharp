from error_type import Error_type


class Error:
    def __init__(self, error_type: Error_type, number_line: int, interval: tuple[int, int], text: str):
        self.error_type = error_type
        self.number_line = number_line
        self.interval = interval
        self.text = text
