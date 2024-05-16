#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'

#######################################
# ERRORS
#######################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

#######################################
# POSITION
#######################################

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#######################################
# TOKENS
#######################################

INT		= 'INT'
FLOAT    = 'FLOAT'
PLUS     = 'PLUS'
MINUS    = 'MINUS'
MUL      = 'MUL'
DIV      = 'DIV'
LPAREN   = 'LPAREN'
RPAREN   = 'RPAREN'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(INT, int(num_str))
        else:
            return Token(FLOAT, float(num_str))

#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0

    def eat(self, token_type):
        if self.token_index < len(self.tokens) and self.tokens[self.token_index].type == token_type:
            self.token_index += 1
        else:
            expected_token = self.tokens[self.token_index - 1] if self.token_index > 0 else None
            raise Exception(f"Expected token {token_type}, got {expected_token}")

    def factor(self):
        token = self.tokens[self.token_index]
        if token.type in (INT, FLOAT):
            self.eat(token.type)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
        result = self.factor()
        while self.token_index < len(self.tokens) and self.tokens[self.token_index].type in (MUL, DIV):
            if self.tokens[self.token_index].type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif self.tokens[self.token_index].type == DIV:
                self.eat(DIV)
                result /= self.factor()
        return result

    def expr(self): 
        result = self.term()
        while self.token_index < len(self.tokens) and self.tokens[self.token_index].type in (PLUS, MINUS):
            if self.tokens[self.token_index].type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif self.tokens[self.token_index].type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result

#######################################
# INTERPRETER
#######################################

def interpret(tokens):
    parser = Parser(tokens)
    return parser.expr()

#######################################
# RUN
#######################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    if error: return None, error

    result = interpret(tokens)
    return result, None

# Test the language
if __name__ == '__main__':
    while True:
        text = input('calc > ')
        result, error = run('<stdin>', text)

        if error: print(error.as_string())
        else: print(result)