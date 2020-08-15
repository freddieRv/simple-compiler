# -*- coding: utf-8 -*-

import re
from utils import Error
from Analyzer import Analyzer

class Lexic(Analyzer):
    RESERVED_WORDS = (
        "entero",
        "real",
        "cadena",
        "caracter",
        "booleano",
        "byte",
        "si",
        "entonces",
        "sino",
        "termina_si",
        "para",
        "hasta",
        "termina_para",
        "verifica",
        "inicio",
        "fin_verifica",
        "caso",
        "no",
        "mientras",
        "haz",
        "termina_mientras",
        "lee",
        "escribe",
        "fin",
        "funcion",
        "regresa",
    )

    ASSIGNMENT_OPERATOR_RE      = r':= *'
    LOGIC_OPERATORS_RE          = r'(y|o|no) *'
    RELATIONAL_OPERATORS_RE     = r'(>=|<=|<>|>|<|=) *'
    ARITHMETIC_OPERATORS_RE     = r'(\+|-|\*|/) *'
    IDENTIFIER_RE               = r'[a-z]\w* *'
    INT_CONST_RE                = r'\d+ *'
    FLOAT_CONST_RE              = r'\d*\.\d+ *'
    STRING_CONST_RE             = r'\".*\" *'
    CHAR_CONST_RE               = r'\".\" *'
    MULTI_LINE_COMMENT_START_RE = r'/\*'
    MULTI_LINE_COMMENT_END_RE   = r'\*/'
    ONE_LINE_COMMENT_RE         = r'//'
    SPECIAL_CHARACTER_RE        = r'(°|!|#|\$|%|&|\.|\(|\)|\?|¡|¨|\[|\]|{|}|@|\||¿|:|,) *'
    INVISIBLE_CHARACTERS_RE     = r'\s'
    BOOLEAN_CONST_RE            = r'verdadero|falso'
    FILE_NAME_RE                = r'[a-zA-Z_-]+\.ply'

    def __init__(self, _file):
        super(Lexic, self).__init__()
        self._lexeme = ""
        self._token  = ""
        self._file   = _file
        self._line   = ""

        # Regular expresions compiled patterns
        self._rexpressions = {
            "identifier"       : re.compile(type(self).IDENTIFIER_RE),
            "int_const"        : re.compile(type(self).INT_CONST_RE),
            "float_const"      : re.compile(type(self).FLOAT_CONST_RE),
            "string_const"     : re.compile(type(self).STRING_CONST_RE),
            "boolean_const"    : re.compile(type(self).BOOLEAN_CONST_RE),
            "char_const"       : re.compile(type(self).CHAR_CONST_RE),
            "assignment_oper"  : re.compile(type(self).ASSIGNMENT_OPERATOR_RE),
            "logic_oper"       : re.compile(type(self).LOGIC_OPERATORS_RE),
            "relational_oper"  : re.compile(type(self).RELATIONAL_OPERATORS_RE),
            "arithmetic_oper"  : re.compile(type(self).ARITHMETIC_OPERATORS_RE),
            "comment_start"    : re.compile(type(self).MULTI_LINE_COMMENT_START_RE),
            "comment_end"      : re.compile(type(self).MULTI_LINE_COMMENT_END_RE),
            "one_line_comment" : re.compile(type(self).ONE_LINE_COMMENT_RE),
            "special_char"     : re.compile(type(self).SPECIAL_CHARACTER_RE),
            "file_name"        : re.compile(type(self).FILE_NAME_RE),
            "invisible_char"   : re.compile(type(self).INVISIBLE_CHARACTERS_RE),
        }

    def lexeme(self):
        return self._lexeme

    def token(self):
        return self._token

    def next_lexeme(self):
        '''Gets and returns the next lexeme'''

        while True:
            self._fetch_lexeme()

            if self._token == 'comment_start':

                e = Error (
                    line   = self._file.index(),
                    column = len(self._file.line()) - len(self._line),
                    _type  = "Lexic",
                    desc   = "Unterminated comment"
                )

                while self._token != 'comment_end':
                    self._fetch_lexeme()

                    if self._file.eof():
                        self._raise_error(e)
                        break

            elif self._token == 'one_line_comment':
                self._fetch_line()
            elif self._token == 'invisible_char':
                continue
            else:
                break

        return self.lexeme()

    def _fetch_lexeme(self):
        while (not self._line) or self._line == '\n':
            self._fetch_line()

            if self._file.eof():
                self._token  = 'eof'
                self._lexeme = 'eof'
                return

        next_match = None
        for token in self._rexpressions.keys():

            match = self._rexpressions[token].match(self._line)

            if match:
                if not next_match or len(match.group()) > len(next_match.group()):
                    next_match  = match
                    self._token = (token, "reserved_word")[match.group().strip() in self.RESERVED_WORDS]

        if not next_match:
            super(Lexic, self)._raise_error(Error(
                line   = self._file.index(),
                _type  = "Lexic",
                column = len(self._file.line()) - len(self._line) + 1,
                desc   = "Unidentified lexeme '" + self._line[0] + "'"
            ))

            self._lexeme = self._line[0]
            self._token  = "no_token"
            self._line   = self._line[1:].strip()
        else:
            self._lexeme = next_match.group().strip()
            self._line   = self._line[next_match.end():]

    def _fetch_line(self):
        self._line = self._file.next_line()

    def line(self):
        return self._file.index()

    def column(self):
        return len(self._file.line()) - len(self._line)

    def peek(self):
        prev_lexeme = self._lexeme
        prev_token  = self._token
        prev_line   = self._line

        lexeme = self.next_lexeme()
        token  = self._token

        self._lexeme = prev_lexeme
        self._token  = prev_token
        self._line   = prev_line
        self._file.rewind()

        return (lexeme, token)
