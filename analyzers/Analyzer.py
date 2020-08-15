from abc import ABCMeta, abstractmethod

class Analyzer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        self._errors = []

    def _raise_error(self, error):
        '''Adds error to the error list'''
        self._errors.append(error)

    def errors(self):
        return self._errors

    def dump_errors(self):
        for e in self._errors:
            print e
