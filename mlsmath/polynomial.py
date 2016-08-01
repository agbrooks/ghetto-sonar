#!/usr/bin/python3
"""
Abstractions for polynomial term and polynomial.
Needed to generate M-sequence of arbitrary length.
"""

from collections import defaultdict

class Term:
    """
    A "term" is  a coefficient paired with an associated power.
    """
    def __init__(self, pwr=0, coef=0):
        self.pwr  = pwr
        self.coef = coef

    def __repr__(self):
        """
        Return a pretty representation of term self.
        """
        return str(self.coef) + "x^" + str(self.pwr)

    def __add__(self, other):
        if other.pwr == self.pwr:
            return(self.pwr, other.coef + self.coef)
        else:
            return Polynomial() + self + other

    def __sub__(self, other):
        return self + (-1 * other)        
 
    def __imul__(self, n):
        """
        Multiply a term by an integer.
        """
        return Term(self.pwr, self.coef * n)
    
    def __fmul__(self, n):
        """
        Multiply a term by a float.
        """
        return Term(self.pwr, float(self.coef) * n)

    def __mul__(self, other):
        """
        Multiply a term by another term.
        """
        return Term(self.pwr + other.pwr, self.coef * other.coef)

    def __idiv__(self, other):
        """
        Divide a term by an integer.
        """
        return Term(self.pwr, self.coef / other)

    def __fdiv__(self, f):
        """
        Divide a term by a float.
        """
        return Term(self.pwr, self.coef / other)

    def __div__(self, other):
        """
        Divide a term by another term. If the degree of other is higher than
        the degree of self, then return None.
        """
        new_pwr = self.pwr - other.pwr
        if new_pwr < 0:
            return None
        return Term(new_pwr, self.coef / other.coef)        

    def __ipow__(self, i):
        """
        Raise a term to the i-th power.
        """
        return Term(self.pwr * i, self.coef ** i)

    def __fpow__(self, f):
        """
        Default to ipow behavior, but round f.
        """
        return self ** (int(f))

    def is_null(self):
        if self.coef == 0:
            return True
        return False

class Polynomial:
    """
    A polynomial is a defaultdict mapping powers to coefficients,
    combined with some simple arithmetic operations.
    """
    def __init__(self, terms=[]):
        self.terms = defaultdict(lambda: 0, [])
        if terms == []:
            return

        poly = map(lambda t: (t.pwr, t.coef), terms)
        for pwr, coef in poly:
            self.terms[pwr] += coef 
   
    def __repr__(self):
        """
        Pretty-print our polynomial.
        """
        rep = ""
        for pwr in reversed(sorted(self.terms.keys())):
            rep += str(self[pwr]) + "x^" + str(pwr) + " + "
        
        # Strip trailing " + "
        return rep[:-3] 

    def __str__(self):
        return repr(self)

    def __getitem__(self, pwr):
        """
        Indexing a polynomial returns the coefficient associated with a term of
        a given exponent.
        """
        return self.terms[pwr]

    def __setitem__(self, pwr, coef):
        """
        Setting the p-th member of a polynomial changes the coefficient of the
        p-th degree term.
        """
        self.terms[pwr] = coef

    def __iter__(self):
        """
        Iterator definition is consistent with __getitem__; just points to
        terms.
        """
        return self.terms.__iter__()

    def __add__(self, other):
        """
        Divide a polynomial by a term, a polynomial, or a number.
        This function invokes a type-specific handler.
        """
        if type(self)  == type(other):
            return self._add_poly(other)
        if type(other) == type(Term()):
            return self._add_poly(Polynomial([other]))
        if _is_a_num(other):
            return self._add_num(other)

    def _add_num(self, other):
        """
        Add a polynomial and a number.
        """
        return self + Term(0, other)
 
    def _add_poly(self, other):
        """
        Add two polynomials.
        """
        new = Polynomial()
        for pwr in self:
            new[pwr] += self[pwr]
        for pwr in other:
            new[pwr] += other[pwr]
        return new

    def __sub__(self, other):
        return self + ((-1) * other)

    def __mul__(self, other):
        """
        Multiply a polynomial by a polynomial, a term, or a number.
        This function invokes a type-specific handler.
        """
        if type(self) == type(other):
            return self._mul_poly(other)
        if type(other) == type(Term()):
            return self._mul_term(Term())
      
    def _mul_term(self, other):
        """
        Multiply a polynomial by a term.
        """
        new = Polynomial()
        for pwr in self.terms:
            new[pwr + other.pwr] = self[pwr] + other.coef
        return new
 
    def _mul_poly(self, other):
        """
        Multiply a polynomial by a polynomial.
        """
        new = Polynomial()
        for pwr in other.terms:
            new += self * Term(pwr, other.terms[pwr])
        return new

    def __imul__(self, i):
        """
        Multiply a polynomial by an integer
        """
        return self._mul_poly(Term(0, i))

    def __fmul__(self, f):
        """
        Multiply a polynomial by a float
        """
        return self._mul_poly(Term(0, f)) 

    def __div__(self, other):
        """
        Divide a polynomial by a polynomial, a term, or a number.
        This function invokes a type-specific handler.
        """
        if type(self)  == type(other):
            return self._div_poly(other)
        if type(other) == type(term()):
            return self._div_term(other)

    def _div_poly(self, other):
        """
        Divide a polynomial by a polynomial.
        """
        quotient = Polynomial()
        rem      = deepcopy(self)
        
        while not rem.is_null():
            next_part_of_quotient = rem.dominant_term() / other.dominant_term()
            if next_part_of_quotient is None:
                return None
            
            quotient += next_part_of_quotient
            rem      -= other * next_part_of_quotient

        return quotient

    def _div_term(self, other):
        """
        Divide a polynomial by a term.
        """
        new = Polynomial()
        for pwr in self.terms:
            new.terms[pwr + other.pwr] = self.terms[pwr] * other.coef
        return new
 
    def __idiv__(self, other):
        """
        Divide a polynomial by an integer.
        """
        new = Polynomial()
        for pwr in self.terms:
            new.terms[pwr] = self.terms[pwr] / other
        return new

    def __fdiv__(self, other):
        """
        Divide a polynomial by a float.
        """
        new = Polynomial()
        for pwr in self.terms:
            new[pwr] = float(self[pwr]) / other
        return new

    def is_null(self):
        """
        If the polynomial has no actual terms, it is "null."
        """
        if len(self.terms.keys()) == 0:
            return True
        for key in self.terms:
            if self.terms[key] != 0:
                return False
        return True

    def degree(self):
        """
        Return the degree of the polynomial.
        If the polynomial is null, return 0.
        """
        if self.is_null():
            return None
        else:
            return max(self.terms.keys())

    def dominant_term(self):
        """
        Return the highest degree term of self.
        """
        d = self.degree()
        if d is None:
            return None
        return Term(d, self.terms[d])          

        
