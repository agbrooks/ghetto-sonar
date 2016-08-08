#!/usr/bin/python3

import numpy as np

"""
modulation.py:

Perform all of the gritty signal processing behind the sonar here. The basic
steps are as follows:

Transmission:

1. "Stretch" the m-sequence in time: each sample becomes n samples to form
    a new sequence which is n-times longer. Generally, as n increases, so does
    the SNR. However, the spatial resolution also decreases.
2. Use the stretched sequence to amplitude modulate  a sinusoid at Nyquist. We
    could choose our frequency almost arbitrarily, but Nyquist on conventional
    audio hardware should be inaudible and lack interference (usually).

Receiving:

The received sequence will consist of some background noise, which we hope to
be negligible, and the modulated sinusoid we sent, offset in time and amplitude
slightly with each reflection.

1. Demodulate the M-sequence. This can be done by taking a windowed FFT of len
    n and then picking out the proper frequency components of the sinusoid.
2. Correlate with the "ideal" M-sequence. In simulation, this tends to yield
    a signal that has several peaks superposed on some low-frequency distortion
    produced by the overlapping M-sequences.
3. The correlation must be high-passed to remove this low-frequency distortion.
4. Peaks are then selected.
"""

TIMESTRETCH = 8

def stretch(seq, n):
    """
    Form a new sequence by duplicating every sample in seq n times.
    """
    stretched = []
    for s in seq:
        for _ in range(n):
            stretched.append(s)

    return stretched

def modulate_pulse(pulse, space=TIMESTRETCH, dco=0):
    """
    Perform steps 1 and 2 of transmission. space is an integer corresponding
    to the number of samples to stretgth the pulse, and dco is the constant
    offset to use in amplitude modulation (ie, mls(t) * (dco + cos(t))).
    """
    pulse = stretch(pulse, space)
    
    modulated = []
    for idx, samp in enumerate(pulse):
        modulated.append(samp * (dco + np.cos(np.pi * idx)))
    
    return modulated

def demodulate_pulse(rx, space=TIMESTRETCH):
    """
    Demodulate the MLS from the received signal, per step 1 of RX.
    """
    rx = np.array(rx)
    demodulated = []
    #FIXME: Python loop overhead makes this excruciatingly slow!
    #       Cython might work in a pinch, but this needs to be
    #       very tight if we're going to use long sequences.
    for win_start in range(len(rx) - space):
        windowed = rx[win_start : win_start+space]
        dft      = np.fft.fft(windowed)
        score    = np.abs(dft[int(len(dft)/2)]) / 8

        demodulated.append(score)

    return demodulated

def find_reflections(demodulated, ideal, n=1, scaling=TIMESTRETCH,
                      ignore_highest=False):
    """
    Find how many samples in the reflections are present.
    To do so, correlate the demodulated m-sequence with the ideal one,
    high-pass to remove LF noise, and return n highest values.

    It may be desirable to ignore the highest peak, as it might just be
    the direct speaker -> microphone path.
    """
    corr = np.correlate(demodulated, ideal, mode='valid')
    #5th order butterworth filter with knee point just below
    #Nyquist
    p,q  = sig.butter(5, 0.975, 'highpass')
    filtered = sig.lfilter(p,q, corr)

    which_highest = np.argsort(filtered)[-n:]

    if ignore_highest:
        return which_highest[:-1]
    return which_highest
    
