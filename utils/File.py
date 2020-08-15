import linecache

class File:
    def __init__(self, filename):
        self._filename = filename
        self._index    = 0
        self._line     = ''
        self._eof      = False

        try:
            f = open(filename)
            f.close()
        except:
            raise IOError("Couldn't open file '" + filename + "'")

    def next_line(self):
        if self._index == 0 or (self._line and self._index != 0):
            self._index += 1
            self._line   = linecache.getline(self._filename, self._index)
            self._eof    = not self._line

        return self._line

    def index(self):
        return self._index

    def line(self):
        return self._line

    def eof(self):
        return self._eof

    def rewind(self):
        if self._index:
            self._index -= 1
