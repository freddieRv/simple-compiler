class StatementComponent:

    def __init__(self, label=None, token=None, line=0, column=0):
        self.__label  = label
        self.__token  = token
        self.__line   = line
        self.__column = column

    def label(self):
        return self.__label

    def token(self):
        return self.__token

    def line(self):
        return self.__line

    def column(self):
        return self.__column
