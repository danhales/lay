from collections.abc import Iterable

def validated(method):
    def wrapper(self, other):
        self._validate(other)
        return method(self, other)
    return wrapper

class Vector:
    def __init__(self, *entries):
        if len(entries) == 1 and isinstance(entries[0], Iterable):
            self._entries = tuple(entries[0])
        else:
            self._entries = tuple(entries)

    @validated
    def __add__(self, u):
        self._validate(u)
        return Vector((self._entries[i] + u._entries[i] for i in range(len(self._entries))))

    @validated
    def __sub__(self, u):
        self._validate(u)
        return Vector((self._entries[i] - u._entries[i] for i in range(len(self._entries))))

    @validated
    def __mul__(self, other):
        if isinstance(other, Vector):
            return self._dot(other)
        elif isinstance(other, (int, float)):
            return self._scale(other)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self._scale(other)
        return NotImplemented

    def _validate(self, u):
        if not isinstance(u, Vector):
            raise TypeError(f'Object {u} of type {type(u)} is not a Vector')
        
        if len(self.entries()) != len(u.entries()):
            raise IndexError(f'Incompatible vector lengths: {len(self.entries())} != {len(u.entries())}')

    def entries(self):
        return tuple(self._entries)

    def _scale(self, scalar: float):
        return Vector(e * scalar for e in self.entries())

    def _dot(self, u):
        dot_product = 0

        for i in range(len(self.entries())):
            dot_product += self._entries[i] * u._entries[i]

        return dot_product

    def norm(self):
        return (self * self)**0.5

    def __repr__(self):
        string = '['

        for i in range(len(self._entries)):
            string += str(self._entries[i])

            if i < len(self._entries) - 1:
                string += ','

        string += ']'

        return string
    
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        if not len(self._entries) == len(other._entries):
            return False

        for idx in range(len(self._entries)):
            if self._entries[idx] != other._entries[idx]:
                return False

        return True

    def _repr_latex_(self):
        entries = r" \\ ".join(str(e) for e in self._entries)
        return rf"\[ \begin{{bmatrix}} {entries} \end{{bmatrix}} \]"

class Matrix:
    def __init__(self, rows):
        # working under the assumption that entries is a tuple of tuples
        entries = list()

        for row in rows:
            entries.append(tuple(row))

        self._entries = tuple(entries)

    def __repr__(self):
        output = ""
        for row in self._entries:
            for item in row:
                output += str(item) + " "
            output += "\n"

        return output