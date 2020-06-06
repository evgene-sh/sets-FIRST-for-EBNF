import re


class LexerError(Exception):
    def __init__(self, line, pos):
        self.text = f'({line}, {pos})'


class Token:
    def __init__(self, domain, coords, attr):
        self.domain = domain
        self.coords = coords
        self.attr = attr

    def __str__(self):
        return '{} {}: {}'.format(self.domain, self.coords, self.attr)
    
    def __repr__(self):
        return self.attr


class Position:
    def __init__(self, data):
        self.data = data
        self.line, self.pos_line, self.pos_data = 1, 0, 0
    
    def scroll(self, count):
        for ch in self.data[self.pos_data:self.pos_data+count]:
            if ch == '\n':
                self.line += 1
                self.pos_line = 0
            else: self.pos_line += 1
        self.pos_data += count
    
    def has_next(self):
        return self.pos_data < len(self.data)


class Lexer:
    lexems = (('[', r'\['),(']', r'\]'), ('noterm', '\([A-Z]\)'), ('=', r'\='), ('|', r'\|'), 
    ('+', r'\+'), ('*', r'\*'), ('?', r'\?'), ('.', r'\.'), ('eps', 'eps'), ('term', '(\\\\[^\n \t]|[^\n \t])'))
    tokens = []

    def get_tokens(self):
        return(t for t in self.tokens)

    def match_all(self):
        for lexem in self.lexems:
            match = re.match(lexem[1], self.position.data[self.position.pos_data:])
            if match:
                self.tokens.append(Token(lexem[0], (self.position.line, self.position.pos_line), match.group()))
                return match
        return re.match('[\t \n]+', self.position.data[self.position.pos_data:])

    def __init__(self, file):
        with open(file) as f:
            self.position = Position(f.read())

        while self.position.has_next():
            match = self.match_all()
            if match:
                self.position.scroll(match.end())
            else: raise LexerError(self.position.line, self.position.pos_line)