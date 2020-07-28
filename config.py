import oyaml as yaml
import os

version = 'v1.3_real'

signal = 'real'
alpha = 130
beta = 130
max_spline = 4
window_length = 800
min_portion = 0.05
max_portion = 0.25


def make_summary():
    filename = 'documentation/config_' + version + '.yaml'

    # Now, put it all together
    dict_for_yaml = {'Signal': signal,
                     'Step size time': alpha,
                     'Step size Frequency': beta,
                     'Highest Spline order': max_spline,
                     'Spline window length': window_length,
                     'Minimum portion of Coefficients': min_portion,
                     'Maximum portion of Coefficients': max_portion}

    # Write into yaml file. Overwrites existing files.
    if not os.path.exists('documentation'):
        os.makedirs('documentation')

    with open(filename, "w") as f:
        yaml.safe_dump(dict_for_yaml, f)
