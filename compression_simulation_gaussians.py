# Script to run compression simulations. Configurations have to be made in the config file before running the script.

import os
import time as time
import numpy as np
import argparse
import matplotlib.pyplot as plt
import scipy.io.wavfile as wave

from functions.signals import gaussian
from functions.compression import compression_results, get_modspace_p_from_compression

import config as cfg


# Parser only needed for 'plot_results' flag. Everything else is defined in config file.
def parse_args():
    parser = argparse.ArgumentParser(description='Run some compression simulations.',
                                     epilog='All configurations should be done in the config file.')
    parser.add_argument('--plot_results', help='Plot the results', action='store_true')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    # Document settings
    cfg.make_summary()

    # Directory for results
    if not os.path.exists('results/numpy_data'):
        os.makedirs('results/numpy_data')

    # Get all arguments from command line
    args = parse_args()

    # Get signal
    if cfg.signal == 'synthetic':
        sampling_rate = 2000
        signal = gaussian(sampling_rate)
    else:
        sampling_rate, signal = wave.read('recordings/blackbird.wav')
        signal = np.float64(signal)
        signal /= np.max(np.abs(signal))
    length_signal = len(signal)

    # Get all numbers of coefficients we want to test against.
    max_coef_number = length_signal * sampling_rate / (2 * cfg.alpha * cfg.beta)
    list_of_coefnumbers = np.linspace(int(max_coef_number * cfg.min_portion),
                                      int(max_coef_number * cfg.max_portion),
                                      500, dtype='int')

    # Get results for Gaussian window function
    start_time_gaussian = time.time()
    for tfr in np.linspace(0.5, 2, 7):
        results = compression_results(signal, cfg.alpha, cfg.beta, ['gauss', float(tfr)], list_of_coefnumbers)
        p = get_modspace_p_from_compression([res[0] for res in results], [res[1] for res in results])
        print('Gaussian window, tfr: ', tfr, ' p: ', p, sep='')

        # Save results
        np.save('results/numpy_data/gauss_' + cfg.version + '.npy', results, allow_pickle=True)
        # Plot
        if args.plot_results:
            plt.plot([np.log(res[0]) for res in results], [np.log(res[1]) for res in results],
                     label='Time-Frequency ratio: ' + str(tfr), linestyle=(0, (4*tfr, 1, 1, 1)))

    end_time_gaussian = time.time()

    # Get results for all splines
    # start_time_splines = time.time()
    # for spline_order in range(1, cfg.max_spline + 1):
    #     results = compression_results(signal, cfg.alpha, cfg.beta, ['spline', spline_order, cfg.window_length],
    #                                   list_of_coefnumbers)
    #     p = get_modspace_p_from_compression([res[0] for res in results], [res[1] for res in results])
    #     print('Spline of order ', spline_order, ', p: ', p, sep='')
    #
    #     # Save results
    #     np.save('results/numpy_data/spline_' + str(spline_order) + '_' + cfg.version + '.npy', results,
    #             allow_pickle=True)
    #     # Plot
    #     if args.plot_results:
    #         plt.plot([np.log(res[0]) for res in results], [np.log(res[1]) for res in results],
    #                  label='Spline order ' + str(spline_order))
    # end_time_splines = time.time()

    # Compare times.
    print("%s seconds for Gaussian window" % (end_time_gaussian - start_time_gaussian))
    # print("%s seconds for all spline windows" % (end_time_splines - start_time_splines))

    if args.plot_results:
        plt.title('Errors for ' + cfg.signal + ' signal')
        plt.xlabel('Number of coefficients (log scaled)')
        plt.ylabel('Error (log scaled)')
        plt.legend(loc='lower left')
        plt.show()