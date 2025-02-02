class JSONParser:
    def __init__(self, s):
        self.s = s
        self.i = 0

    def parse(self):
        value = self.parse_value()
        self.skip_whitespace()
        if self.i != len(self.s):
            raise ValueError("Dane JSON zawierają dodatkowe znaki")
        return value

    def skip_whitespace(self):
        while self.i < len(self.s) and self.s[self.i] in " \t\n\r":
            self.i += 1

    def parse_value(self):
        self.skip_whitespace()
        if self.i >= len(self.s):
            raise ValueError("Nieoczekiwany koniec danych")
        char = self.s[self.i]
        if char == '"':
            return self.parse_string()
        elif char == '{':
            return self.parse_object()
        elif char == '[':
            return self.parse_array()
        elif char in "-0123456789":
            return self.parse_number()
        elif self.s.startswith("true", self.i):
            self.i += 4
            return True
        elif self.s.startswith("false", self.i):
            self.i += 5
            return False
        elif self.s.startswith("null", self.i):
            self.i += 4
            return None
        else:
            raise ValueError(f"Znak '{char}' nieoczekiwany w tym miejscu")

    def parse_string(self):
        # Zakładamy, że obecny znak to cudzysłów otwierający
        self.i += 1
        result = ""
        while self.i < len(self.s):
            char = self.s[self.i]
            if char == '"':
                self.i += 1  # pomijamy zamykający cudzysłów
                return result
            elif char == '\\':
                self.i += 1
                if self.i >= len(self.s):
                    raise ValueError("Niepoprawna sekwencja ucieczki")
                escape_char = self.s[self.i]
                if escape_char == '"':
                    result += '"'
                elif escape_char == '\\':
                    result += '\\'
                elif escape_char == '/':
                    result += '/'
                elif escape_char == 'b':
                    result += '\b'
                elif escape_char == 'f':
                    result += '\f'
                elif escape_char == 'n':
                    result += '\n'
                elif escape_char == 'r':
                    result += '\r'
                elif escape_char == 't':
                    result += '\t'
                elif escape_char == 'u':
                    # Obsługa sekwencji Unicode
                    if self.i + 4 >= len(self.s):
                        raise ValueError("Niepoprawna sekwencja Unicode")
                    hex_digits = self.s[self.i + 1:self.i + 5]
                    try:
                        result += chr(int(hex_digits, 16))
                    except ValueError:
                        raise ValueError("Niepoprawna sekwencja Unicode")
                    self.i += 4
                else:
                    raise ValueError(f"Niepoprawny znak ucieczki: {escape_char}")
            else:
                result += char
            self.i += 1
        raise ValueError("Niezamknięty łańcuch znaków")

    def parse_number(self):
        start = self.i
        if self.s[self.i] == '-':
            self.i += 1
        while self.i < len(self.s) and self.s[self.i].isdigit():
            self.i += 1
        if self.i < len(self.s) and self.s[self.i] == '.':
            self.i += 1
            if self.i >= len(self.s) or not self.s[self.i].isdigit():
                raise ValueError("Niepoprawny format liczby")
            while self.i < len(self.s) and self.s[self.i].isdigit():
                self.i += 1
        if self.i < len(self.s) and self.s[self.i] in "eE":
            self.i += 1
            if self.i < len(self.s) and self.s[self.i] in "+-":
                self.i += 1
            if self.i >= len(self.s) or not self.s[self.i].isdigit():
                raise ValueError("Niepoprawny format wykładnika")
            while self.i < len(self.s) and self.s[self.i].isdigit():
                self.i += 1
        num_str = self.s[start:self.i]
        try:
            if '.' in num_str or 'e' in num_str or 'E' in num_str:
                return float(num_str)
            else:
                return int(num_str)
        except ValueError:
            raise ValueError("Niepoprawna liczba: " + num_str)

    def parse_array(self):
        # Zakładamy, że obecny znak to '['
        self.i += 1
        self.skip_whitespace()
        array = []
        if self.i < len(self.s) and self.s[self.i] == ']':
            self.i += 1
            return array
        while True:
            item = self.parse_value()
            array.append(item)
            self.skip_whitespace()
            if self.i >= len(self.s):
                raise ValueError("Niezamknięta tablica")
            if self.s[self.i] == ']':
                self.i += 1
                break
            elif self.s[self.i] == ',':
                self.i += 1
            else:
                raise ValueError("Oczekiwano ',' lub ']' w tablicy")
            self.skip_whitespace()
        return array

    def parse_object(self):
        # Zakładamy, że obecny znak to '{'
        self.i += 1
        self.skip_whitespace()
        obj = {}
        if self.i < len(self.s) and self.s[self.i] == '}':
            self.i += 1
            return obj
        while True:
            self.skip_whitespace()
            if self.i >= len(self.s) or self.s[self.i] != '"':
                raise ValueError("Oczekiwano klucza w postaci łańcucha znaków")
            key = self.parse_string()
            self.skip_whitespace()
            if self.i >= len(self.s) or self.s[self.i] != ':':
                raise ValueError("Oczekiwano ':' po kluczu")
            self.i += 1  # pomijamy dwukropek
            self.skip_whitespace()
            value = self.parse_value()
            obj[key] = value
            self.skip_whitespace()
            if self.i >= len(self.s):
                raise ValueError("Niezamknięty obiekt")
            if self.s[self.i] == '}':
                self.i += 1
                break
            elif self.s[self.i] == ',':
                self.i += 1
            else:
                raise ValueError("Oczekiwano ',' lub '}' w obiekcie")
            self.skip_whitespace()
        return obj


def parse_json(s):
    parser = JSONParser(s)
    return parser.parse()


# Przykładowe użycie:
if __name__ == "__main__":
    test_json = '''
    {
        "name": "Jan",
        "age": 25,
        "isStudent": false,
        "scores": [88, 92, 79],
        "address": {
            "city": "Warszawa",
            "zip": "00-001"
        },
        "notes": null
    }
    '''
    try:
        result = parse_json(test_json)
        print("Wynik parsowania:")
        print(result)
    except ValueError as e:
        print("Błąd parsowania:", e)
