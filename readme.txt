Library files are in the main directory. Experiments are in 'instances/'.

The available optimization problems with their respective genome encodings for the EA are found in 'problib.py'.

For the experiments in 'instances/':

- 'pf-*' files countain comparative runs between various types of EAs.
- 'pfx-*' files contain comparative runs for various hyperparameters for the same type of EA.

Experiments are run by calling the python interpreter on the 'instances/pf*' file. They write out result files in the 'results/' folder. These include some parameter descriptions and preliminary plots. Most importantly, the '*.pickle' file contains all data about the experiment. 'pf-' experiments can be plottted in detail by calling 'plotter.py' on the '*.pickle' file. 'pfx-' experiments can be plottted in detail by calling 'plotterx.py' on the '*.pickle' file.