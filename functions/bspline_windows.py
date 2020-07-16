import numpy as np
from scipy.interpolate import BSpline


# B-Spline as array of length width_samp.
def bspline(order_spline, width_samp):
    t = np.linspace(0, order_spline + 1, order_spline + 1)
    b = BSpline.basis_element(t, 0)  # Callable
    x = np.linspace(0, order_spline + 1, width_samp)

    return b(x)


# Centralize a window function (needed for ltfatpy).
def centralize(window):
    length = len(window)
    window = np.roll(window, int(length/2))

    return window


# Get the B-Spline window.
def bspline_window(order_spline, width_samp):
    spline = bspline(order_spline, width_samp)
    spline = centralize(spline)

    return spline