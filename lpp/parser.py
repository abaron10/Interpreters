
from typing import (
    Callable,
    Dict,
    Optional,
    List
    )

from lpp.ast import (
    Expression,
    Program,
    Statement,
    LetStatement,
    ReturnStatement,
    Identifier
)
from lpp.lexer import Lexer
from lpp.token import (
    Token,
    TokenType
)

PrefixParsFn = Callable[[], Optional[Expression]] # def sth(): return expression
InfixParseFn = Callable[[Expression], Optional[Expression]]
PrefixParseFns = Dict[TokenType, PrefixParsFn]
InfixParseFns = Dict[TokenType, InfixParseFn]

class Parser:
    
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None
        self._errors: List[str] = []

        self._prefix_parse_fns: PrefixParseFns = self._register_prefix_fns()
        self._infix_parse_fns: InfixParseFns = self._register_infix_fns()

        self._advance_tokens()
        self._advance_tokens()

    @property
    def errors(self) -> List[str]:
        return self._errors

    def parse_program(self) -> Program:
        program: Program = Program(statements=[])

        assert self._current_token is not None
        # while there are tokens left, we can process an statement
        while self._current_token.token_type != TokenType.EOF:
            statement = self._parse_statement()
            if statement is not None:
                program.statements.append(statement)

            self._advance_tokens()
        return program

    def _advance_tokens(self) -> None:
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    #this method helps to verify that after a LET statement, there is a IDENT; variable x where x should be the ident
    def _expected_token(self, token_type: TokenType) -> bool:
        assert self._peek_token is not None
        if self._peek_token.token_type == token_type:
            self._advance_tokens()

            return True

        self._expected_token_error(token_type)
        return False

    def _expected_token_error(self, token_type: TokenType) -> None:
        assert self._peek_token is not None
        error = f'Se esperaba que el siguiente token fuera {token_type} pero se obtuvo {self._peek_token.token_type}' 
        self.errors.append(error)

    # this code verifies that assignation is correct  for LET 
    def _parse_let_statement(self) -> Optional[LetStatement]:
        assert self._current_token is not None
        let_statement = LetStatement(token=self._current_token)

        if not self._expected_token(TokenType.IDENT):
            return None
        # if code reached this line, means that validation for asignation is correct so id can now process the name of the variable
        let_statement.name =  Identifier(token=self._current_token, value=self._current_token.literal)

        if not self._expected_token(TokenType.ASSIGN):
            return None
        
        #TODO terminar cuando sepamos parsear expresiones
        while self._current_token.token_type != TokenType.SEMICOLON:
            self._advance_tokens()
        
        return let_statement

    def _parse_return_statement(self) -> Optional[ReturnStatement]:
        assert self._current_token is not None
        return_statement = ReturnStatement(token=self._current_token)

        self._advance_tokens()

        # TODO terminar cuando sepamos parsear expresiones
        while self._current_token.token_type != TokenType.SEMICOLON:
            self._advance_tokens()

        return return_statement


    def _parse_statement(self) -> Optional[Statement]:
        assert self._current_token is not None
        if self._current_token.token_type == TokenType.LET:
            return self._parse_let_statement()
        elif self._current_token.token_type == TokenType.RETURN:
            return self._parse_return_statement()
        else:
            return None
    
    def _register_infix_fns(self) -> InfixParseFns:
        return {}
    
    def _register_prefix_fns(self) -> PrefixParseFns:
        return {}

'''
    Parsing function order:
    1. _parse_statement: Valida que el primer token sea un  'variable'm si es asi, lo envia al metodo _parse_let_statement 
    2. _parse_let_statement: acá se crea una instancia de LetStatement debido a que paso la validación de arriba. Luego se
    valida el token siguiente al actual (variable). El siguiente deberia corresponder a un IDENT (nombre de la variable), si
    cumple con esta regla de asiganción, se avanzan los tokens +1. Luego de este movimiento, el current token corresponde con 
    el nombre de la variable, se crea una instancia de Identifier para asignar el nombre del let_statement. Luego se valida nuevamente
    con el _expected_token que el siguiente caracter sea de asignación.

'''