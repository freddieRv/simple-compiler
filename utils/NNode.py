class NNode:
    def __init__(self, data=None, father=None, _id=0):
        self.__data     = data
        self.__children = []
        self.__father   = father
        self.__id       = _id

    def data(self):
        return self.__data

    def id(self):
        return self.__id

    def children(self):
        return self.__children

    def father(self):
        return self.__father

    def add_child(self, new_children):
        self.__children.append(new_children)

    def count_nodes(self):
        no_nodes = 0

        for child in self.__children:
            no_nodes += child.count_nodes() + 1

        return no_nodes
