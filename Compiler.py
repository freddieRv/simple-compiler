import sys
from analyzers import *
from utils import File
from utils import print_statement_tree

class Compiler:
    def __init__(self, lexic=None, syntactic=None, semantic=None):
        self._lexic     = lexic
        self._syntactic = syntactic
        self._semantic  = semantic

    def compile(self):
        '''Main method to compile a file'''

        # Main parsing
        symbol_tree, syntactic_tree, functions = self._syntactic.parse()

        for function in functions:
            self._semantic.parse(symbol_tree, function)

        self._semantic.parse(symbol_tree, syntactic_tree)

        # Print errors
        self._lexic.dump_errors()
        self._syntactic.dump_errors()
        self._semantic.dump_errors()

        print "Compilation complete."

        print "Symbol Tree:"
        self._syntactic.symbol_tree().printTree()
        print "==========================="

        # Plot trees
        # print_statement_tree(syntactic_tree)
        # for function in functions:
        #     print_statement_tree(function)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise IOError("No input file")

    f  = File(sys.argv[1])
    l  = Lexic(f)
    sy = Syntactic(l)
    se = Semantic()
    c  = Compiler(lexic=l, syntactic=sy, semantic=se)

    c.compile()
