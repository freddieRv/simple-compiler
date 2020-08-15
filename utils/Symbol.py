class Symbol:
    def __init__(self, symbol=None, _type=None, _class=None):
        self.__symbol = symbol
        self.__type   = _type
        self.__class  = _class

    def _class(self):
        return self.__class

    def symbol(self):
        return self.__symbol

    def type(self):
        return self.__type

    def __lt__(self, other):
        try:
            return  self.__symbol < other.__symbol
        except AttributeError as e:
            return self.__symbol < other

    def __le__(self, other):
        try:
            return  self.__symbol <= other.__symbol
        except AttributeError as e:
            return self.__symbol <= other

    def __eq__(self, other):
        try:
            return  self.__symbol == other.__symbol
        except AttributeError as e:
            return self.__symbol == other

    def __ne__(self, other):
        try:
            return  self.__symbol != other.__symbol
        except AttributeError as e:
            return self.__symbol != other

    def __gt__(self, other):
        try:
            return  self.__symbol > other.__symbol
        except AttributeError as e:
            return self.__symbol > other

    def __ge__(self, other):
        try:
            return  self.__symbol >= other.__symbol
        except AttributeError as e:
            return self.__symbol >= other

    def __str__(self):
        return "\t{}: {}, {}".format(self.__symbol, self.__class, self.__type)
