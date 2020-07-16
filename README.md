# Compression Simulations
 Code to simulate the effect of different window functions on the compression rate when using Gabor frames.
 
## Installation
Python packeges required are defined in `requirements.txt`. To get the code running when using a new Ubuntu system, simply run
```
chmod o+x install.sh
./install.sh
```

## Usage
Update `config.py` to set your desired parameters, then run
```
python3 compression_simulation.py
```
If you set the flag `--plot_results`, you get a visualisation of the compression rates.