from mlsmath.mls import make_mls
from audio.txrx  import sonar_probe

seq = make_mls(6)
rx = sonar_probe(seq)
