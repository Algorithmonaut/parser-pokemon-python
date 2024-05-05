# Typescript being a regular language, I still want to parse it without the
# use of regular expressions using single pass parsing.

# single underscores _ for protected attributes and methods, and double underscores __ for private attributes and methods

from typing import Any, Dict, List, Union


def error(error: str):
    print(error + ", line " + str(scanner.get_current_line_number))


class Scanner:
    _pokedex_src: List[str]
    _pokedex_readable: Dict[str, Dict[str, Any]]
    _current_line_number: int = 0
    _current_pokemon_identifier: str
    _current: int = 0
    _start: int = 0

    def __init__(self, source_file) -> None:
        self._pokedex_src = source_file.readlines()
        for line in self._pokedex_src:
            line.replace("\t", "").replace("\n", "").replace(" ", "")

    def scan_lines(self) -> Dict[str, Dict[str, Any]]:
        for line in self._pokedex_src:
            # The first line is the ds declaration
            if self._current_line_number > 0:
                self._scan_line(line)

            self._current_line_number += 1
            self._start, self._current = 0, 0

        return self._pokedex_readable

    def _scan_line(self, line: str) -> None:
        if line[len(line) - 1] == "{":
            self._current_pokemon_identifier = self._get_identifier(line)
            return

        property_identifier = self._get_identifier(line)
        self._advance()

        # elif line[0] == "[":
        #     self._commit_prop_list()
        # elif line[0] == "{":
        #     self._commit_prop_map()
        if self._is_digit(line[0]):
            value = self._get_number(line)
        elif line[0] == '"':
            value = self._get_str(line)
        else:
            error("Unable to infer type")
            value = None

        print(
            self._current_pokemon_identifier
            + " - "
            + property_identifier
            + " - "
            + str(value)
        )

        self._pokedex_readable[self._current_pokemon_identifier][
            property_identifier
        ] = value

    def get_current_line_number(self):
        return self._current_line_number

    ############################################################################

    def _is_at_EOL(self) -> bool:
        return self._current >= len(self._pokedex_src[self._current_line_number])

    def _is_digit(self, char: str) -> bool:
        assert len(char) == 1
        return char >= "0" and char <= "9"

    def _is_alpha(self, char: str) -> bool:
        assert len(char) == 1
        return (
            (char >= "a" and char <= "z")
            or (char >= "A" and char <= "Z")
            or (char == "_")
        )

    def _is_alpha_numeric(self, char: str) -> bool:
        return self._is_alpha(char) or self._is_digit(char)

    ############################################################################

    def _peek(self):
        if self._is_at_EOL():
            return "\0"
        return self._pokedex_src[self._current]

    def _peek_next(self) -> str:
        if self._current + 1 >= len(self._pokedex_src):
            return "\0"
        return self._pokedex_src[self._current + 1]

    def _advance(self) -> str:
        self._current += 1
        return self._pokedex_src[self._current]

    def _stick_current(self) -> None:
        self._start = self._current

    ############################################################################

    def _get_number(self, line) -> Union[int, float]:
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

    def _get_str(self, line) -> str:
        while self._peek() != '"' and not self._is_at_EOL():
            self._advance()
        if self._is_at_EOL():
            error("Unterminated string")

        return line[self._start : self._current]

    def _get_map(self):
        pass

    def _get_list(self):
        pass

    def _get_identifier(self, line: str) -> str:
        while self._peek() != ":" and not self._is_at_EOL():
            self._advance()
        if self._is_at_EOL():
            error("Unterminated identifier")
        return line[self._start : self._current]


################################################################################

if __name__ == "__main__":
    with open("pokedex.ts", "r") as pokedex_source:
        scanner = Scanner(pokedex_source)
        scanner.scan_lines()
