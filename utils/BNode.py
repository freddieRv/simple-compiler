class BNode:
    def __init__(self, data):
        self.__data        = data
        self.__left_child  = None
        self.__right_child = None

    def data(self):
        return self.__data

    def left_child(self, new_data=None):
        if new_data:
            self.__left_child = new_data
        else:
            return self.__left_child

    def right_child(self, new_data=None):
        if new_data:
            self.__right_child = new_data
        else:
            return self.__right_child
