# All the functions needed for compressing a signal and analysing the result

import numpy as np
from scipy.stats import linregress
from ltfatpy import gabimagepars, dgtreal, gabwin, idgtreal, gabdual

from functions.bspline_windows import bspline_window


# Get modulation norm from matrix of Gabor coefficients.
def mod_norm(matrix, weight, p=1, C2=1):
    V = np.power(np.abs(matrix), float(p))
    # meshgrid
    i = np.arange(0, matrix.shape[0], 1)
    j = np.arange(0, matrix.shape[1], 1)
    grid_i, grid_j = np.meshgrid(i, j, indexing='ij', sparse=True)
    grid = weight(grid_i, grid_j)
    grid = np.power(grid, float(p))

    return np.power(np.multiply(V, grid).sum(), 1 / float(p)) * C2


# Given number of coefficients N, get N-th highest value mu.
def mu_out_coefnumber(matrix, number_of_coefficients):
    mu = np.sort(abs(matrix).flatten())[-number_of_coefficients]

    return mu


# Reconstruct signal with only the coefficients higher than mu, return reconstruction error.
def reconstruct_signal(matrix, mu, signal, window, alpha, number_of_frequencies):
    length_signal = len(signal)
    new_coefficients = np.where(abs(matrix) < mu, 0, matrix)
    new_signal = (idgtreal(new_coefficients, window, alpha, number_of_frequencies, length_signal)[0]).real
    err = (np.linalg.norm(new_signal - signal) ** 2) / length_signal

    return err  # , mu, new_signal  # Can return more stats to analyse different aspects.


# Results for compressing the given digits using different numbers of coefficients.
# Returns a list with each entry of form (number_of_coefficients, compression_error).
def compression_results(signal, alpha, beta, window_params, list_of_coefnumbers):
    # window_params: Either ['gauss', variance] or ['spline', order, window_length]

    length_signal = len(signal)

    # Gabor Frame and window function
    # number_of_frequencies = int(length_signal/beta)
    # length_for_gabor = gabimagepars(length_signal, int(length_signal/alpha), number_of_frequencies)[2]
    alpha, number_of_frequencies, length_for_gabor, bla1, bla2 = \
        gabimagepars(length_signal, int(length_signal / alpha), int(length_signal / beta))

    # Window and dual window
    if window_params[0] == 'gauss':
        window = gabwin({'name': 'gauss', 'tfr': window_params[1]}, alpha, number_of_frequencies, length_for_gabor)[0]
    elif window_params[0] == 'spline':
        window = bspline_window(window_params[1], window_params[2])
    else:
        raise ValueError("Please use 'gauss' or 'spline' window")
    dual_window = gabdual(window, alpha, number_of_frequencies)

    # Get Gabor coefficients
    coefficients = dgtreal(signal, dual_window, alpha, number_of_frequencies)[0]

    # Different reconstructions
    result = []
    for coefnumber in list_of_coefnumbers:
        mu = mu_out_coefnumber(coefficients, coefnumber)
        err = reconstruct_signal(coefficients, mu, signal, window, alpha, number_of_frequencies)
        result = result + [(coefnumber, err)]

    return result


# Given the results of different reconstructions in compression_results, calculate the compression rate and return the
# corresponding value for p (smoothness in modulation space).
def get_modspace_p_from_compression(list_of_coefnumbers, errors):
    slope = linregress(np.log(list_of_coefnumbers), np.log(errors))[0]

    return 2 / (1 - slope)
