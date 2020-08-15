from Analyzer import Analyzer
from utils import BST
from utils import Symbol
from utils import Error
from utils import NNode
from utils import StatementComponent

class Syntactic(Analyzer):
    TOKEN_TO_TYPE = {
        "int_const"     : "entero",
        "float_const"   : "real",
        "string_const"  : "cadena",
        "boolean_const" : "booleano",
        "char_const"    : "caracter",
        "identifier"    : "identifier"
    }

    def __init__(self, lexic_parser):
        super(Syntactic, self).__init__()
        self.__symbol_tree         = BST()
        self.__statement_index     = 0
        self.__statement_tree_root = NNode(data=StatementComponent(label="program"), _id=self.__statement_index)
        self.__current_statement   = self.__statement_tree_root
        self.__functions           = []
        self.__lexic               = lexic_parser
        self.__lexeme              = None
        self.__operators_stack     = []
        self.__operands_stack      = []
        self.__scope               = "global"
        self.SOs                   = ("win", "linux", "macos", "*")
        self.ARCHITECTURES         = ("32", "64", "*")
        self.DATA_TYPES            = (
            "entero",
            "real",
            "cadena",
            "caracter",
            "booleano",
            "byte"
        )

    def symbol_tree(self):
        return self.__symbol_tree

    def statement_tree(self):
        return self.__statement_tree_root

    def __add_statement(self, statement_component, token, next_statement=False):
        self.__statement_index += 1

        new_node = NNode(
            _id    = self.__statement_index,
            data   = StatementComponent(
                label  = statement_component,
                token  = token,
                line   = self.__lexic.line(),
                column = self.__lexic.column()
            ),
            father = self.__current_statement
        )

        self.__current_statement.add_child(new_node)

        if next_statement:
            self.__current_statement = new_node

    def __statement_end(self):
        self.__current_statement = self.__current_statement.father()

    def parse(self):
        '''main method for parsing a file syntactically'''

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != "so":
            self.__error("so")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme not in self.SOs:
            self.__error("SO name")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != "arq":
            self.__error("arq")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme not in self.ARCHITECTURES:
            self.__error("architecture name")

        self.__lexeme = self.__lexic.next_lexeme()
        while self.__lexeme == "importar":
            self.__import()

        while self.__lexeme == "funcion":
            self.__func_declaration()

        if self.__lexeme != "main":
            self.__error("main")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != "(":
            self.__error("(")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != ")":
            self.__error(")")

        self.__lexeme = self.__lexic.next_lexeme()
        self.__block()

        return self.__symbol_tree, self.__statement_tree_root, self.__functions

    def __error(self, expected):
        self._raise_error(Error (
            line   = self.__lexic.line(),
            column = self.__lexic.column(),
            _type  = "Syntactic",
            desc   = "< {} > expected, {} < {} > received".format(expected, self.__lexic.token(), self.__lexeme)
        ))

    def __block(self):
        if self.__lexeme != "inicio":
            self.__error("inicio")

        self.__lexeme = self.__lexic.next_lexeme()
        while self.__lexeme != "fin" and self.__lexeme != "eof":

            if self.__lexeme == "si":
                self.__if()
            elif self.__lexeme == "para":
                self.__for()
            elif self.__lexeme == "verifica":
                self.__switch()
            elif self.__lexeme == "mientras":
                self.__while()
            elif self.__lexic.token() == "identifier":
                self.__assignment()
            elif self.__lexeme == "lee":
                self.__input()
            elif self.__lexeme == "escribe":
                self.__output()
            elif self.__lexeme in self.DATA_TYPES:
                self.__var_declaration()
            else:
                self.__error("statement")
                self.__lexeme = self.__lexic.next_lexeme()

        if self.__lexeme != "fin":
            self.__error("fin")

    def __import(self):
        if self.__lexeme != "importar":
            self.__error("importar")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != "<":
            self.__error("<")

        raw_input(self.__lexeme)
        self.__lexeme = self.__lexic.next_lexeme()
        raw_input(self.__lexeme)
        if self.__lexic.token() != "file_name":
            self.__error("file name")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != ">":
            self.__error(">")

        self.__lexeme = self.__lexic.next_lexeme()

    def __if(self):
        self.__add_statement(self.__lexeme, self.__lexic.token(), True)

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != "(":
            self.__error("(")

        self.__lexeme = self.__lexic.next_lexeme()
        self.__expression()

        if self.__lexeme != ")":
            self.__error(")")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != "entonces":
            self.__error("entonces")

        self.__add_statement(self.__lexeme, self.__lexic.token(), True)

        self.__lexeme = self.__lexic.next_lexeme()
        self.__block()
        self.__lexeme = self.__lexic.next_lexeme()

        self.__statement_end()

        if self.__lexeme == "sino":
            self.__add_statement(self.__lexeme, self.__lexic.token(), True)
            self.__lexeme = self.__lexic.next_lexeme()
            self.__block()
            self.__lexeme = self.__lexic.next_lexeme()
            self.__statement_end()

        self.__statement_end()

    def __for(self):
        self.__add_statement(self.__lexeme, self.__lexic.token(), True)
        self.__lexeme = self.__lexic.next_lexeme()

        self.__assignment()

        if self.__lexeme != "hasta":
            self.__error("hasta")

        self.__add_statement(self.__lexeme, self.__lexic.token())

        self.__lexeme = self.__lexic.next_lexeme()
        self.__expression()

        if self.__lexeme != "haz":
            self.__error("haz")

        self.__add_statement(self.__lexeme, self.__lexic.token(), True)
        self.__lexeme = self.__lexic.next_lexeme()

        self.__block()
        self.__lexeme = self.__lexic.next_lexeme()

        self.__statement_end()
        self.__statement_end()

    def __switch(self):
        self.__add_statement(self.__lexeme, self.__lexic.token(), True)

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != "(":
            self.__error("(")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexic.token() != "identifier":
            self.__error("identifier")

        self.__add_statement(self.__lexeme, self.__lexic.token())

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != ")":
            self.__error(")")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != "inicio":
            self.__error("inicio")

        self.__lexeme = self.__lexic.next_lexeme()

        while self.__lexeme == "caso":
            self.__add_statement(self.__lexeme, self.__lexic.token(), True)
            self.__lexeme = self.__lexic.next_lexeme()
            self.__expression()
            self.__block()
            self.__lexeme = self.__lexic.next_lexeme()
            self.__statement_end()

        if self.__lexeme == "no_caso":
            self.__add_statement(self.__lexeme, self.__lexic.token(), True)
            self.__lexeme = self.__lexic.next_lexeme()
            self.__block()
            self.__lexeme = self.__lexic.next_lexeme()
            self.__statement_end()

        if self.__lexeme != "fin":
            self.__error("fin")

        self.__lexeme = self.__lexic.next_lexeme()
        self.__statement_end()

    def __while(self):
        self.__add_statement(self.__lexeme, self.__lexic.token(), True)
        self.__lexeme = self.__lexic.next_lexeme()

        self.__expression()

        if self.__lexeme != "haz":
            self.__error("haz")

        self.__add_statement(self.__lexeme, self.__lexic.token(), True)

        self.__lexeme = self.__lexic.next_lexeme()
        self.__block()
        self.__lexeme = self.__lexic.next_lexeme()

        self.__statement_end()
        self.__statement_end()

    def __assignment(self):
        identifier = None

        if self.__lexic.token() != "identifier":
            self.__error("identifier")

        identifier = self.__lexeme

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme == "(":
            self.__function_call(identifier)
            return
        elif self.__lexeme != ":=":
            self.__error(":= or '('")

        self.__add_statement(self.__lexeme, self.__lexic.token(), True)
        self.__add_statement(identifier, "identifier")

        self.__lexeme = self.__lexic.next_lexeme()
        self.__expression()

        self.__statement_end()

    def __input(self):
        self.__add_statement(self.__lexeme, self.__lexic.token(), True)

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != "(":
            self.__error("(")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexic.token() != "identifier":
            self.__error("identifier")

        self.__add_statement(self.__lexeme, self.__lexic.token())

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != ")":
            self.__error(")")

        self.__lexeme = self.__lexic.next_lexeme()
        self.__statement_end()

    def __output(self):
        self.__add_statement(self.__lexeme, self.__lexic.token(), True)

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != "(":
            self.__error("(")

        self.__lexeme = self.__lexic.next_lexeme()
        self.__expression()

        if self.__lexeme != ")":
            self.__error(")")

        self.__lexeme = self.__lexic.next_lexeme()
        self.__statement_end()

    def __var_declaration(self):
        variable   = True
        var_type   = None
        identifier = None

        if self.__lexeme not in self.DATA_TYPES:
            self.__error("data type")
        else:
            var_type = self.__lexeme

        self.__add_statement(self.__lexeme, self.__lexic.token(), True)
        self.__lexeme = self.__lexic.next_lexeme()

        while variable:
            variable = False

            if self.__lexic.token() != "identifier":
                self.__error("identifier")
            else:
                identifier = self.__lexeme + "@" + self.__scope

            self.__symbol_tree.add(Symbol(
                symbol = identifier,
                _type  = var_type,
                _class = "variable"
            ))

            self.__lexeme = self.__lexic.next_lexeme()

            if self.__lexeme == ":=":
                self.__add_statement(self.__lexeme, None, True)
                self.__add_statement(identifier, "identifier")
                self.__lexeme = self.__lexic.next_lexeme()
                self.__expression()
                self.__statement_end()
            else:
                self.__add_statement(identifier, "identifier")

            if self.__lexeme == ",":
                self.__lexeme = self.__lexic.next_lexeme()
                variable = True

        self.__statement_end()

    def __func_declaration(self):
        var_type   = None
        identifier = None
        main_tree  = None
        main_index = 0

        if self.__lexeme != "funcion":
            self.__error("funcion")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexic.token() != "identifier":
            self.__error("identifier")
        else:
            identifier               = self.__lexeme
            self.__scope             = self.__lexeme
            main_tree                = self.__current_statement
            main_index               = self.__statement_index
            self.__current_statement = NNode(data=StatementComponent(label=identifier), _id=0)
            self.__statement_index   = 0
            self.__functions.append(self.__current_statement)

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != "(":
            self.__error("(")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != ")":
            self.__parameters() #TODO: declare parameters

        if self.__lexeme != ")":
            self.__error(")")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme != "regresa":
            self.__error("regresa")

        self.__lexeme = self.__lexic.next_lexeme()
        if self.__lexeme not in self.DATA_TYPES:
            self.__error("data type")
        else:
            var_type = self.__lexeme

        self.__symbol_tree.add(Symbol(
            symbol = identifier,
            _type  = var_type,
            _class = "function"
        ))

        self.__lexeme = self.__lexic.next_lexeme()
        self.__block()
        self.__lexeme = self.__lexic.next_lexeme()

        self.__scope = "global"
        self.__current_statement = main_tree
        self.__statement_index   = main_index

    def __parameters(self):
        param      = True
        var_type   = None
        identifier = None

        while param:
            param = False

            if self.__lexeme not in self.DATA_TYPES:
                self.__error("data type")
            else:
                var_type = self.__lexeme

            self.__lexeme = self.__lexic.next_lexeme()
            if self.__lexic.token() != "identifier":
                self.__error("identifier")
            else:
                identifier = self.__lexeme + "@" + self.__scope

            self.__symbol_tree.add(Symbol(
                symbol = identifier,
                _type  = var_type,
                _class = "parameter"
            ))

            self.__add_statement(var_type, "data_type", True)
            self.__add_statement(identifier, "parameter", True)
            self.__statement_end()
            self.__statement_end()

            self.__lexeme = self.__lexic.next_lexeme()
            if self.__lexeme == ",":
                param = True
                self.__lexeme = self.__lexic.next_lexeme()

    def __dump_expression(self):

        started_statement = False

        if self.__operators_stack:
            self.__add_statement(self.__operators_stack.pop(0), None, True)
            operand = self.__operands_stack.pop(0)
            self.__add_statement(operand[0], self.TOKEN_TO_TYPE[operand[1]])
            started_statement = True

        if not self.__operators_stack and self.__operands_stack:
            operand = self.__operands_stack.pop(0)
            self.__add_statement(operand[0], self.TOKEN_TO_TYPE.get(operand[1]))

        if self.__operators_stack:
            self.__dump_expression()

        if started_statement:
            self.__statement_end()

    def __expression(self):
        if self.__lexic.token() not in ("identifier", "int_const", "float_const", "string_const", "boolean_const", "char_const"):
            self.__error("identifier or constant")

        self.__operands_stack.append((self.__lexeme, self.__lexic.token()))

        self.__lexeme = self.__lexic.next_lexeme()

        while self.__lexic.token() in ("logic_oper", "relational_oper", "arithmetic_oper"):
            self.__operators_stack.append(self.__lexeme)
            self.__lexeme = self.__lexic.next_lexeme()

            if self.__lexic.token() not in ("identifier", "int_const", "float_const", "string_const", "boolean_const", "char_const"):
                self.__error("identifier or constant")

            self.__operands_stack.append((self.__lexeme, self.__lexic.token()))
            self.__lexeme = self.__lexic.next_lexeme()

        if len(self.__operands_stack) <= len(self.__operators_stack):
            self.__error("identifier or constant")
        # elif self.__lexic.token() in ("identifier", "int_const", "float_const", "string_const", "boolean_const", "char_const"):
        #     self.__operands_stack.append((self.__lexeme, self.__lexic.token()))

        self.__dump_expression()

    def __function_call(self, func_name):
        self.__add_statement(func_name, "identifier", True)
        self.__lexeme = self.__lexic.next_lexeme()

        while self.__lexic.token() in (
            "identifier",
            "int_const",
            "float_const",
            "string_const",
            "boolean_const",
            "char_const"
        ):
            self.__add_statement(self.__lexeme, self.__lexic.token())
            self.__lexeme = self.__lexic.next_lexeme()
            if self.__lexeme == ",":
                self.__lexeme = self.__lexic.next_lexeme()

        if self.__lexeme != ")":
            self.__error(")")

        self.__statement_end()
        self.__lexeme = self.__lexic.next_lexeme()

# Clases: Constante, Funcion, Procedimiento, Local, R parametro, Indefinido
# Tipos: R decimal, Entero, Logico, Alfabetico, Indefinido
# print self.__current_statement.data().label()
# TODO: return statement
