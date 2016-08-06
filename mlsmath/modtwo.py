#!/usr/bin/python3

from polynomial import Term, Polynomial
from copy       import deepcopy

"""
modtwo defines a simple class for mod-2 arithmetic and provides a subclass of
Polynomial which is evaluated with mod-2 arithmetic.
"""

def _is_boolish(b):
    """
    Check if b is a 1, 0, True, or False.
    """
    if (b == 1) or (b == 0) or (b == True) or (b == False):
        return True
    else:
        return False

class ModTwo:
    """
    ModTwo -- a simple class for mod-2 arithmetic.
    """
    def __init__(self, b):
        if not _is_boolish(b):
            raise Warning("Tried to make a ModTwo with a non-boolish value")
        self.val = int(b)

    def __repr__(self):
        return str(self.val)
    
    def __str__(self):
        return repr(self)

    def __int__(self):
        return self.val

    def __bool__(self):
        return bool(int(self))

    def __add__(self, other):
        return ModTwo((int(self) + int(other)) % 2)

    def __sub__(self, other):
        self.__add__(other)

    def __mul__(self, other):
        return ModTwo((int(self) * int(other)) % 2)

    def __pow__(self, other):
        if int(other) < 1:
            return ModTwo(1)
        else:
            return deepcopy(self)

class MTPolynomial(Polynomial):
    """
    Mod-Two Polynomial. Exactly like a generic polynomial, but can be evaluated
    at a ModTwo.
    """
    def __init__(self, terms=[]):
        """
        Use Polynomial's init.
        """
        super().__init__(terms)

    def fromPoly(self, p):
        """
        Move the terms from some polynomial p to an MTPolynomial.
        """
        self.terms = p.terms

    def evaluate(self, b):
        """
        Evaluate the polynomial at a ModTwo, b.
        """
        if type(b) != type(ModTwo(0)):
            b = ModTwo(b)
        result = ModTwo(0)
        for p in self.terms:
            result += (b ** p) * self.terms[p]
        return result
