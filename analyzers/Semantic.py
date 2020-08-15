from Analyzer import Analyzer
from utils import Error

class Semantic(Analyzer):
    VALID_OPERATIONS = {
        "entero := entero" : "entero", "entero > entero" : "booleano",
        "entero < entero" : "booleano", "entero >= entero" : "booleano",
        "entero <= entero" : "booleano", "entero <> entero" : "booleano",
        "entero = entero" : "booleano", "entero + entero" : "entero",
        "entero - entero" : "entero", "entero * entero" : "entero",
        "entero / entero" : "entero", "real := real" : "real",
        "real > real" : "booleano", "real < real" : "booleano",
        "real >= real" : "booleano", "real <= real" : "booleano",
        "real <> real" : "booleano", "real = real" : "real",
        "real + real" : "real", "real - real" : "real",
        "real * real" : "real", "real / real" : "real",
        "cadena := cadena" : "cadena", "cadena > cadena" : "booleano",
        "cadena < cadena" : "booleano", "cadena >= cadena" : "booleano",
        "cadena <= cadena" : "booleano", "cadena <> cadena" : "booleano",
        "cadena = cadena" : "booleano", "cadena + cadena" : "cadena",
        "caracter := caracter" : "caracter", "caracter > caracter" : "booleano",
        "caracter < caracter" : "booleano", "caracter >= caracter" : "booleano",
        "caracter <= caracter" : "booleano","caracter <> caracter" : "booleano",
        "caracter = caracter" : "booleano", "booleano y booleano" : "booleano",
        "booleano o booleano" : "booleano", "booleano no booleano" : "booleano",
        "booleano := booleano" : "booleano", "booleano > booleano" : "booleano",
        "booleano < booleano" : "booleano", "booleano >= booleano" : "booleano",
        "booleano <= booleano" : "booleano", "booleano <> booleano" : "booleano",
        "cadena + caracter" : "cadena", "cadena := caracter" : "cadena",
        "entero := real" : "entero", "entero > real" : "booleano",
        "entero < real" : "booleano", "entero >= real" : "booleano",
        "entero <= real" : "booleano", "entero <> real" : "booleano",
        "entero = real" : "booleano", "entero + real" : "real",
        "entero - real" : "real", "entero * real" : "real",
        "entero / real" : "real", "real := entero" : "real",
        "real > entero" : "booleano", "real < entero" : "booleano",
        "real >= entero" : "booleano", "real <= entero" : "booleano",
        "real <> entero" : "booleano", "real = entero" : "booleano",
        "real + entero" : "real", "real - entero" : "real",
        "real * entero" : "real", "real / entero" : "real",
    }

    CONSTANT_TYPES = (
        "int_const",
        "float_const",
        "string_const",
        "boolean_const",
        "char_const"
    )

    def __init__(self):
        super(Semantic, self).__init__()
        self.__symbols    = None
        self.__statements = None
        self.__scope      = None
        self.__operands   = []

    def parse(self, symbol_tree, syntactic_tree):
        self.__scope      = (syntactic_tree.data().label(), "global")[syntactic_tree.data().label() == "program"]
        self.__symbols    = symbol_tree
        self.__statements = syntactic_tree

        for statement in syntactic_tree.children():
            self.__block(statement)


    def __block(self, statement):
        if statement.data().label() == "si":
            self.__if(statement)
        elif statement.data().label() == "para":
            self.__for(statement)
        elif statement.data().label() == "verifica":
            self.__switch(statement)
        elif statement.data().label() == "mientras":
            self.__while(statement)
        elif statement.data().token() == "identifier":
            self.__assignment(statement)
        elif statement.data().label() == "lee":
            self.__input(statement)
        elif statement.data().label() == "escribe":
            self.__output(statement)
        elif statement.data().label() == ":=":
            self.__expression(statement)
        else:
            self.__var_declaration(statement)

    def __error(self, operation, statement):
        self._raise_error(Error (
            _type  = "Semantic",
            desc   = "invalid operation < {} >".format(operation),
            line   = statement.data().line(),
            column = statement.data().column()
        ))

    def __if(self, statement_root):
        print statement_root.data().label()

    def __for(self, statement_root):
        print statement_root.data().label()

    def __switch(self, statement_root):
        print statement_root.data().label()

    def __while(self, statement_root):

        for i in range(len(statement_root.children())):

            if i == 0:
                self.__expression(statement_root.children()[i])
            else:
                self.__block(statement_root.children()[i])

    def __assignment(self, statement_root):
        print statement_root.data().label()

    def __input(self, statement_root):
        self.__expression(statement_root.children()[0])

    def __output(self, statement_root):
        self.__expression(statement_root.children()[0])

    def __expression(self, statement_root):

        if statement_root.children():
            self.__expression(statement_root.children()[0])

        if len(statement_root.children()) > 1:
            self.__expression(statement_root.children()[1])

        if not statement_root.data().token():
            op1 = self.__operands.pop()
            op2 = self.__operands.pop()
            result_type = "undefined"
            operation   = "{} {} {}".format(op1, statement_root.data().label(), op2)

            if self.VALID_OPERATIONS.get(operation):
                result_type = self.VALID_OPERATIONS.get(operation)
            else:
                self.__error(operation, statement_root)

            self.__operands.append(result_type)

        else:
            if statement_root.data().token() == "identifier":
                symbol = self.__symbols.find(statement_root.data().label())

                if not symbol:
                    symbol = self.__symbols.find(statement_root.data().label() + "@" + self.__scope)

                if not symbol:
                    self._raise_error(Error (
                        line   = statement_root.data().line(),
                        column = statement_root.data().column(),
                        _type  = "Semantic",
                        desc   = "Undefined identifier < {} > in {} scope".format(
                            statement_root.data().label(),
                            self.__scope
                        )
                    ))

                    self.__operands.append("undefined")
                else:
                    self.__operands.append(symbol.data().type())
            else:
                self.__operands.append(statement_root.data().token())

    def __var_declaration(self, statement):
        for assignment in statement.children():

            if assignment.children():
                self.__expression(assignment)

    def __assignment(self, statement):
        pass
        # IDEA: if statement has zero or more than two childs, it must be
        #       a function call

    def __function_call(self, statement_root):
        pass
        # TODO: get parameters from symbol tree
        # IDEA: add scope search function to tree?
