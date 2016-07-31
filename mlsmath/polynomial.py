#!/usr/bin/python3
"""
Abstractions for polynomial term and polynomial.
Needed to generate M-sequence of arbitrary length.
"""

from collections import defaultdict

def _is_a_num(n):
    """
    Determine whether n is an int or a float.
    """
    if type(n) == type(0):
       return True
    if type(n) == type(1.0):
       return True
    return False

class Term:
    """
    A "term" is  a coefficient paired with an associated power.
    """
    def __init__(self, pwr=0, coef=0):
        self.pwr  = pwr
        self.coef = coef

    def __add__(self, other):
        if other.pwr == self.pwr:
            return(self.pwr, other.coef + self.coef)
        else:
            return Polynomial() + self + other

    def __sub__(self, other):
        return self + (-1 * other)        
 
    def __mul__(self, other):
        """
        Multiply a term by a number or another term.
        This function invokes _mul_num or _mul_term accordingly.
        """
        if _is_a_num(other):
            return self._mul_num(other)

        if type(other) == type(self):
            return self._mul_term(other)

    def _mul_num(self, n):
        """
        Multiply a term by a number.
        """
        return Term(self.pwr, self.coef * n)
    
    def _mul_term(self, other):
        """
        Multiply a term by another term.
        """
        return Term(self.pwr + other.pwr, self.coef * other.coef)

    def __div__(self, other):
        """
        Divide a term by a number or another term.
        This function invokes _div_num or _div_term accordingly.
        """
        if (_is_a_num(other)):
            return self._div_num(other)
       
        if type(self) == type(other):
            return self._div_term(other)

    def _div_num(self, other):
        """
        Divide a term by a number.
        """
        return Term(self.pwr, self.coef / other)

    def _div_term(self, other):
        """
        Divide a term by another term. If the degree of other is higher than
        the degree of self, then return None.
        """
        new_pwr = self.pwr - other.pwr
        if new_pwr < 0:
            return None
        return Term(new_pwr, self.coef / other.coef)        

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
        self.terms = defaultdict([], lambda _: 0)
        if terms == []:
            return

        poly = map(lambda t: (t.pwr, t.coef), terms)
        for pwr, coef in poly:
            self.terms[pwr] += coef 

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
        new = defaultdict([], lambda _: 0)
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
        if _is_a_num(other):
            return self._mul_num(other)
      
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

    def _mul_num(self, other):
        """
        Multiply a polynomial by a number.
        """
        return self._mul_poly(Term(0, other)) 

    def __div__(self, other):
        """
        Divide a polynomial by a polynomial, a term, or a number.
        This function invokes a type-specific handler.
        """
        if type(self)  == type(other):
            return self._div_poly(other)
        if type(other) == type(term()):
            return self._div_term(other)
        if _is_a_num(other):
            return self._div_num(other)

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

    def _div_term(self, other);
        """
        Divide a polynomial by a term.
        """
        new = Polynomial()
        for pwr in self.terms:
            new.terms[pwr + other.pwr] = self.terms[pwr] * other.coef
        return new
 
    def _div_num(self, other):
        """
        Divide a polynomial by a number.
        """
        new = Polynomial()
        for pwr in self.terms:
            new.terms[pwr] = self.terms[pwr] / other
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

        
