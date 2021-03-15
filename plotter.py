import sys
import os
import time
import dill
import __main__
import explib


experiment_dill = sys.argv[1]
exp = dill.load(open(sys.argv[1], 'rb'))
print(exp.global_args)
print(exp.evolutions)
#print('diversity weight: ' + str(exp.))
explib.Experiment.plot(exp, separate_figures=True, separate_subplots=False, no_show=True, save_file=True, plot_std=True, plot_log=True, show_legend=False)