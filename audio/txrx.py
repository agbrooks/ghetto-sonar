import pyaudio
import numpy as np
from time import sleep

"""
TXRX:

As part of our sonar system, we need to send and receive audio. We need
to play a MLS while recording and then correlate to find when the reflections
occurred. We will worry about processing elsewhere.

Specifically, this file defines sonar_probe(mls).
"""

CHANNELS = 1
RATE     = 44100
FORMAT   = pyaudio.paInt32
CHUNK    = 1024

class _Buffer:
    """
    A buffer with a notion of position. This allows us to treat lists and an
    index as one object rather than juggling around both and relating them
    explictly.
    """
    def __init__(self, contents, overrun_default=None):
        """
        Store contents and position and the default value if we try to read
        outside of the buffer.
        """
        self.contents = contents
        self.cursor = 0
        self.overrun_default = overrun_default
 
    def __len__(self):
        return len(self.contents)

    def consume(self, n):
        """
        Read n entries from contents and return them in a sublist. 
        Update cursor accordingly.
        If we read outside of the array, return the overrun_default, if it is
        not none.
        """
        if (self.cursor + n) < (len(self) - 1):
            out_buf = self.contents[self.cursor : self.cursor+n]
            self.cursor += n
        else:
            if self.overrun_default is not None:
                if self.cursor == (len(self) - 1):
                    return [self.overrun_default] * n
                else:
                    already_consumed = len(self) - 1 - self.cursor
                    self.cursor = len(self) - 1
                    return self.contents[self.cursor:] + \
                           [self.overrun_default] * (n - already_consumed)
            else:
                raise IndexError("Requesting too many samples in buffer without default!")

        return out_buf
    def is_done(self):
        return self.cursor >= len(self) - 1

def _prepare_for_sound(mls):
    """
    Re-scale the MLS so that it plays well over speakers -- make sure it's at
    100% volume.
    """
    new_mls = []
    for sample in mls:
        if sample == 0:
            # Min Int32
            new_mls.append(-2**31)
        else:
            # Max Int32
            new_mls.append(2**31 - 1)
    return new_mls
 
def sonar_probe(mls):
    """
    Sonar probe does the following:
    - Starts recording.
    - Plays the MLS.
    - Keeps recording for one MLS duration after the MLS completes.
    - Returns a list containing the recording.
    
    It accepts a list of 1's and 0's as its only argument.
    """
    # Simple audio callback.
    def audio_callback(in_data, frame_count, time_info, status):
        data = pulse.consume(frame_count)
        recording.extend(in_data)
        if pulse.is_done():
            return (data, pyaudio.paComplete)
        else:
            return (data, pyaudio.paContinue)

    recording = []
    length = len(mls)
    mls    = _prepare_for_sound(mls)
    pulse  = _Buffer(bytearray(mls + ([0] * length)), 0)
    
    audio_ctx = pyaudio.PyAudio()
    stream = audio_ctx.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            output=True,
                            frames_per_buffer=CHUNK,
                            stream_callback=audio_callback)

    print("[-] Sending one pulse, sample length is %s..." % str(length))
    while stream.is_active():
        sleep(0.1)

    stream.stop_stream()
    stream.close()
    audio_ctx.terminate()
       
    return recording

