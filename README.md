# ghetto-sonar
A high-precision sonar experiment for commodity computer hardware.

## Basic Idea
* Generate an M-sequence
* Start an audio recording
* Play it over computer speakers
* Correlate against the known M-sequence to find when reflections were received.

## How well does it work?
Fairly well (in simulation)! As for the real world, well, this project aims to find out!

## Current Progress
Polynomial abstraction, M-sequence generation, modulation/demodulation some aspects of audio all work.

### Remaining work:
* Clean up / verify audio TX/RX
* Command line interface
* More exhaustive testing

