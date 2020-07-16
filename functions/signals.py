# Defining different synthetic signals

import numpy as np


# Special synthetic signal with good time-frequency resolution. A corresponds to time localisation, B to frequencies
def synthetic(A, B, expo=2, Fs=2000):
    n = np.linspace(0, 1, Fs)
    sig = np.sin(2 * np.pi * B * np.exp(-A * np.power(n - 0.5, expo)) * n)
    return sig


# Sum a lot of signals to distribute the time-frequency support over a larger area. Takes a lot of time.
def synthetic_sum(Fs=2000):
    res = np.zeros(Fs)
    for A in np.linspace(50, 10000, 150):
        for B in np.linspace(10, int(Fs / 2), int(Fs / 25)):
            res = res + synthetic(A, B, 2, Fs)

    return res


# Sum three special signals.
def synthetic_sum_small(Fs=2000):
    sig1 = synthetic(50, 2, 2, Fs)
    sig2 = synthetic(50000, 4, 2, Fs)
    sig3 = synthetic(40, 200, 2, Fs)
    sig = sig1 + sig2 + sig3
    sig /= max(abs(sig))

    return sig


# Simple gaussian function between 0 and 1, that gets close to zero at x=0 and x=1.
def gaussian(Fs=2000):
    n = np.linspace(0, 1, Fs)
    sig = 1/(np.sqrt(0.15*2*np.pi))*np.exp(-0.5*np.power((n-0.5)/0.15,2))
    return sig