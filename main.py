# Typescript being a regular language, I still want to parse it without the
# use of regular expressions using single pass parsing.

# single underscores _ for protected attributes and methods, and double underscores __ for private attributes and methods

from typing import Any, Dict, List
import string


with open("pokedex.ts", "r") as file:
    # Read file line by line
    for line in file:
        print(line.strip())  # strip() removes leading/trailing whitespace


def main():
    print("hello world")
    myVar = 2
    print(myVar)


class Scanner:
    _pokedex_src: List[str]
    _pokedex_readable: Dict[str, Dict[str, Any]]
    _current_line_index: int = 0
    _current_pokemon_identifier: str
    _current: int = 0
    _start: int = 0

    def __init__(self, source_file) -> None:
        self._pokedex_src = source_file.readlines()
        for line in self._pokedex_src:
            line.strip("\n\t ")

    def _is_at_EOL(self) -> bool:
        return self._current >= len(self._pokedex_src[self._current_line_index])

    def _is_digit(self, char: str):
        assert len(char) == 1
        return char >= "0" and char <= "9"

    def _is_alpha(self, char: str):
        assert len(char) == 1
        return (
            (char >= "a" and char <= "z")
            or (char >= "A" and char <= "Z")
            or (char == "_")
        )

    def _is_alpha_numeric(self, char: str):
        return self._is_alpha(char) or self._is_digit(char)

    def _peek(self):
        if self._is_at_EOL():
            return "\0"
        return self._pokedex_src[self._current]

    def _peek_next(self):
        if self._current + 1 >= len(self._pokedex_src):
            return "\0"
        return self._pokedex_src[self._current + 1]

    def _commit_pokemon(self):
        pass

    def _commit_prop_number(self, line):
        is_float: bool = False

        while self._is_digit(self._peek()):
            self._advance()
        if self._peek() == "." and self._is_digit(self._peek_next()):
            is_float = True
        while self._is_digit(self._peek()):
            self._advance()

        if is_float:
            return float(line[self._start : self._current])
        return int(line[self._start : self._current])

    def _commit_prop_str(self):
        while(self._peek() != '"' and not self._is_at_EOL):


    def _commit_prop_map(self):
        pass

    def _commit_prop_list(self):
        pass

    def _advance(self) -> str:
        self._current += 1
        return self._pokedex_src[self._current]

    def _record_identifier(self, line: str) -> None:
        while self._advance != ":":
            continue
        self._current_pokemon_identifier = line[: self._current]

    def scan_lines(self) -> Dict[str, Dict[str, Any]]:
        for line in self._pokedex_src:
            if self._current_line_index > 0:
                self._scan_line(line)

            self._current_line_index += 1

    def _scan_line(self, line: str) -> None:
        if line[len(line) - 1] == "{":
            self._record_identifier(line)
        elif line == "},":
            self._commit_pokemon()

        elif line[0] == "[":
            self._commit_prop_list()
        elif line[0] == "{":
            self._commit_prop_map()
        elif line[0] == '"':
            self._commit_prop_str()
        else:
            print("Unable to infer type line " + str(self._current_line_index))


if __name__ == "__main__":
    with open("pokedex.ts", "r") as pokedex_source:
        scanner = Scanner(file)
