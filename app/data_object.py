import collections
import pickle


class DataObject:

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        hashes = []
        for value in self.__dict__.values():
            if isinstance(value, collections.Iterable):
                hashes.append(hash(pickle.dumps(value, -1)))
            else:
                hashes.append(hash(value))

        return hash(tuple(hashes))

    def __repr__(self):
        return repr(self.__dict__)

    def __str__(self):
        return str(self.__dict__)
