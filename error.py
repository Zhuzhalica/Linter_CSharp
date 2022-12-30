from error_type import Error_type
from colorama import init, Fore


class Error:
    def __init__(self, error_type: Error_type, number_line: int,
                 interval: tuple[int, int], text: str, line: str):
        self.error_type = error_type
        self.number_line = number_line
        self.interval = interval
        self.text = text
        self.line = line

    def __str__(self):
        string = Fore.BLUE + f'{self.number_line}: {self.text}\n' + Fore.RESET
        s = self.line[:self.interval[0]] + Fore.MAGENTA + self.line[
                                                          self.interval[0]:
                                                          self.interval[
                                                              1]] + Fore.RESET \
            + self.line[self.interval[1]:].strip()
        string += s
        return string
