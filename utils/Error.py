class Error:
    def __init__(self, line=0, _type=0, column=0, desc=""):
        self._line   = line
        self._type   = _type
        self._column = column
        self._desc   = desc

    def __str__(self):
        '''Overrides string representation of Error object'''
        return self._type + " error on " + "(" + str(self._line) + "," + str(self._column) + "): " + self._desc
