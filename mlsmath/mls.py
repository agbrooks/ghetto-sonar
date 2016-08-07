from mlsmath.lfsr import LFSR
from mlsmath.polynomial import Term
from mlsmath.modtwo     import MTPolynomial 

"""
mls defines make_mls, which creates a maximum length sequence from a given
degree.

The top of the file contains some parsing functions to read the generator
polynomial definitions.
"""

GENERATOR_FILE = "mlsmath/generators.text"

def _strip_after_pound(string):
    """
    Treat "#" as a comment character and remove everything after.
    """
    msg = ""
    for char in string:
        if char != "#":
            msg = msg + char
        else:
            return msg
    return msg

def _to_integers(lst):
    """
    Coerce all members of a list to integers.
    """
    return list(map(int, lst))
 
def _powers_to_terms(pwrs):
    """
    Converts lists containing which terms have a coefficient of 1 to the actual terms
    themselves.
    """
    terms = []
    for pwr in pwrs:
        terms.append(Term(pwr, 1))
    return terms

def _parse_polynomials(filepath):
    """
    Populate a list of polynomials from a filepath.
    """
    try:
        f = open(filepath)
    except FileNotFoundError:
        raise Warning("Unable to find generator definition " + filepath)
    poly_strs = f.readlines()
    polynomials = map(_parse_polynomial, poly_strs)
    # Reject any failures.
    good_polynomials = [p for p in polynomials if p is not None]
    return list(good_polynomials) 

def _parse_polynomial(string):
    """
    Convert a string describing a polynomial (see generators.text) to a MTPoly.
    On fail returns None.
    """
    p = _strip_after_pound(string).split()
 
    if len(p) is 0:
        return None

    try:
        p = _to_integers(p)
    except ValueError:
        return None    

    return MTPolynomial(_powers_to_terms(p))
    


# Note the null polynomial at the beginning. This makes _generators[degree] valid.
_generators = [MTPolynomial([])] + _parse_polynomials(GENERATOR_FILE)

def make_mls(degree):
    """
    Create a maximum length sequence of a given degree.
    """
    if degree > len(_generators):
        raise ValueError("Degree can be, at most, 30.")
    if degree < 1:
        raise ValueError("Degrees less than one are meaningless for MLSes.")

    generator = _generators[degree]
    lfsr      = LFSR(generator)

    return lfsr.evaluate(2**degree - 1)
