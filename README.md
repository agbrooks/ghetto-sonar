# ghetto-sonar
A high-precision sonar experiment for commodity computer hardware.

## Basic Idea
* Generate an M-sequence
* Start an audio recording
* Play it over computer speakers
* Convolve against the known M-sequence to find when reflections were received.

## How well does it work?
I have no idea! That's why I'm building it. Speaker phase distortions could
make it completely ineffective.

Worst case scenario means doing some interesting math and having python code re-usable for other projects.

## Current Progress
M-sequence generation is the "hard part." Most of the abstractions required to do the actual generation are in place.

### Remaining work:
* Kronecker-Schubert Factorizer
* Audio TX/RX
* Testing

