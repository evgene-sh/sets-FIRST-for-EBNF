class SyntaxError(Exception):
    def __init__(self, token):
        self.text = token.__str__()


class Formula:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression


class Atom():
    def __init__(self, type, val, eps = False):
        self.type = type
        self.val = val
        self.eps = eps
    
    def __repr__(self):
        return str(self.repeat)


class Parser:
    def split_for_sentences(self, tokens):
        start, end = 0, 1
        sentences = []
        while start < len(tokens):
            end = start + 1
            try:
                while tokens[end].domain != '.': end += 1
            except IndexError:
                raise SyntaxError(tokens[start])
            sentences.append(tokens[start:end])
            start = end + 1
        return sentences

    def set_eps_atom(self, atom):
        if atom.type == 'eps':
            atom.eps = True
            return True
        if atom.type == 'expression':
            return self.set_eps_expr(atom)
        return False

    def set_eps_expr(self, atom):
        for t in atom.val:
            flag = True
            for a in t:
               if not self.set_eps_atom(a):
                   flag = False
            if flag: atom.eps = True
        return atom.eps

    def parse(self, sentence):
        self.pos = 0
        self.seq = sentence
        if self.seq[self.pos].domain != 'noterm': raise SyntaxError(self.seq[self.pos])
        name = self.seq[self.pos].attr
        self.pos += 1
        if self.seq[self.pos].domain != '=': raise SyntaxError(self.seq[self.pos])
        self.pos += 1
        return Formula(name, self.parse_expr())

    def parse_expr(self):
        expression = []
        expression.append(self.parse_term())
        while self.pos < len(self.seq) and self.seq[self.pos].domain == '|':
            self.pos += 1
            expression.append(self.parse_term())
        return expression

    def parse_term(self):
        term = []
        term.append(self.parse_atom())
        self.pos += 1
        while self.pos < len(self.seq) and self.seq[self.pos].domain in ('noterm', 'term', '[', 'eps'):
            term.append(self.parse_atom())
            self.pos += 1
        return term

    def parse_atom(self):
        if self.seq[self.pos].domain in ('term', 'noterm', 'eps'):
            return Atom(self.seq[self.pos].domain, self.seq[self.pos].attr)

        elif self.seq[self.pos].domain == '[':
            self.pos += 1
            expression =(self.parse_expr())
            if self.seq[self.pos].domain != ']': 
                raise SyntaxError(self.seq[self.pos])
            self.pos += 1
            if self.pos < len(self.seq) and self.seq[self.pos].domain in ('+', '*', '?'):
                return Atom('expression', expression, self.seq[self.pos].domain != '+')
            else:
                self.pos -= 1
                return Atom('expression', expression)

        else: raise SyntaxError(self.seq[self.pos])      

    def get_formulas(self, tokens):
        sentences = self.split_for_sentences(tokens)
        formulas = [self.parse(s) for s in sentences]
        for f in formulas:
            for t in f.expression:
                for a in t:
                    self.set_eps_atom(a)
        return formulas