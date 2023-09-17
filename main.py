
from lpp.repl import start_repl
from lpp.parser import Parser
from lpp.parser import Lexer
from lpp.parser import Program

def main():
#     print("""
#                 []
#                 ||
#                 ||
#                .'`.
#                |  |                       db     db  .d8b.  db    db d888888b d8b   db
#                |  |                        `8b  d8' d8' `8b 88    88   `88'   888o  88
#    |           |  |           |             `8bd8'  88ooo88 Y8    8P    88    88V8o 88
#    |           |  |           |               88    88~~~88 `8b  d8'    88    88 V8o88
#    |           |  |           |               88    88   88  `8bd8'    .88.   88  V888
#    |       _  /    \  _       |               YP    YP   YP    YP    Y888888P VP   V8P
#   |~|____.| |/      \| |.____|~|
#   |                            |                                        Version: 0.0.1
#   `-`-._                  _.-'-'                   
#         `-.           _.-'                                           
#           ||\________/||                               
#           `'          `'
#  --------------------------------------------------------------------------------------------    
# """)


#     start_repl()       
    source: str = '''
            variable x = 5;
            variable y = 10;
            variable foo = 20;
        '''
    lexer: Lexer = Lexer(source)
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()

if __name__ == '__main__':
    main()

      