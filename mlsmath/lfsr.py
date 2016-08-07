"""
LFSR -- linear feedback shift register.
Define an LFSR class and how to use it.
"""

from modtwo import ModTwo

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

    def evaluate(self, length, initial_seq=None):
        """
        From a sequence of initial numbers, create a sequence of 1's and 0's of
        length length. If a primitive polynomial is used as the input to the
        LFSR, then the generated sequence will be an m-sequence.
        """

        # Default initial sequence is just 000...1.
        if initial_seq is None:
            initial_seq = ([0] * (self.highest - 2)) + [1]

        # Make sure everything is a ModTwo.
        initial_seq = list(map(ModTwo, initial_seq))

        # Make sure we have enough values.
        if len(initial_seq) < (self.highest - 1):
            raise ValueError("Initial sequence is of insufficient length.")

        out_seq = initial_seq
        subseq_size = self.highest - 1

        for _ in range(length - len(initial_seq)):
            # Examine the most recent necessary members.
            next_val = ModTwo(0)
            subseq   = out_seq[-subseq_size:]
            for i in self.offsets:
                next_val += subseq[i]

            out_seq.append(next_val)

        return list(map(int, out_seq)) 
     
