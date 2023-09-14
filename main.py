
from lpp.token import (
    Token,
    TokenType,
)

from lpp.lexer import Lexer


def main():
        
        source: str = '''
            variable suma = procedimiento(x, y) {
                x + y;
            };
        '''
        lexer: Lexer = Lexer(source)

        tokens = []
        for i in range(16):
            tokens.append(lexer.next_token())

        print(tokens)

main()

      