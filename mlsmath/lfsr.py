"""
LFSR -- linear feedback shift register.
Define an LFSR class and how to use it.
"""

from mlsmath.modtwo import ModTwo

class LFSR:
    """
    Linear Feedback Shift Register
    """
    def __init__(self, poly):
        """
        Takes a Polynomial or an MTPolynomial which describes the LFSR.
        A trivial example:
        x^4 + x + 1 => x(i+4) = x(i+1) + x(i)
        """
        
        #Sanity check:
        for pwr in poly.terms:
            if (poly.terms[pwr] != 1) and (poly.terms[pwr] != 0):
                raise ValueError("Polynomial must have coefficients of 0/1.")

        # LFSR expression comes from polyomial as
        # x(i+highest) = 
        # x(i+offsets[n]) + x(i+offsets[n-1]) + ... + x(i+offsets[0])
        self.offsets = []
        for pwr in poly.terms:
            self.offsets.append(pwr)

        self.highest = max(self.offsets) 
        self.offsets.remove(self.highest)

    def evaluate(self, length, initial_st=None):
        """
        From a sequence of initial numbers, create a sequence of 1's and 0's of
        length length. If a primitive polynomial is used as the input to the
        LFSR, then the generated sequence will be an m-sequence.
        """

        # Default initial sequence is all 1's.
        if initial_st is None:
            initial_st = [1] * (self.highest)

        # Make sure we have enough values:
        if len(initial_st) < (self.highest):
            raise ValueError("Initial sequence is of insufficient length.")

        # Make sure everything is a ModTwo.
        reg_state = list(map(ModTwo, initial_st))

        output_seq = []
        for _ in range(length):
            next_state = ModTwo(0)
            for i in self.offsets:
               next_state += reg_state[i]
            output_seq.append(reg_state[0])
            reg_state = reg_state[1:] + [next_state]
        
        return list(map(int, output_seq))
