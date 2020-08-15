from BNode import BNode

class BST:
    def __init__(self):
        self.__root = BNode()

    def __init__(self):
        self.__root = None

    def root(self):
        return self.__root

    def add(self, new_data):
        if(not self.__root):
            self.__root = BNode(new_data)
        else:
            self._add(new_data, self.__root)

    def _add(self, new_data, node):
        if(new_data < node.data()):
            if(node.left_child()):
                self._add(new_data, node.left_child())
            else:
                node.left_child(BNode(new_data))
        else:
            if(node.right_child()):
                self._add(new_data, node.right_child())
            else:
                node.right_child(BNode(new_data))

    def find(self, data):
        if(self.__root):
            return self._find(data, self.__root)
        else:
            return None

    def _find(self, data, node):
        res = None

        if(data == node.data()):
            res = node
        elif(data < node.data() and node.left_child()):
            res = self._find(data, node.left_child())
        elif(data > node.data() and node.right_child()):
            res = self._find(data, node.right_child())

        return res

    def deleteTree(self):
        # garbage collector will do this for us.
        self.__root = None

    def printTree(self):
        if(self.__root):
            self._printTree(self.__root)

    def _printTree(self, node):
        if(node):
            self._printTree(node.left_child())
            print node.data()
            self._printTree(node.right_child())

    def get_scope(self):
        pass
