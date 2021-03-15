import sys
import os
import time
import dill
import __main__
import explib
from evobasics import *
import matplotlib.pyplot as plt

def lower(avgs, stds):
    return [avgs[x]-stds[x] for x in range(min(len(avgs), len(stds)))]
def upper(avgs, stds):
    return [avgs[x]+stds[x] for x in range(min(len(avgs), len(stds)))]


experiment_dill = sys.argv[1]
exp = dill.load(open(sys.argv[1], 'rb'))

print(exp.global_args)
print(exp.evolutions)

for t,test in enumerate(exp.tests):
    
    if test.name == 'best fitness':
        plotter = plt
        plt.figure(t)
        xs = [0.05 * i for i in range(21)]
        ys = []
        stds =  []
        for e,x in enumerate(xs):
            y =      max([avg(exp.unfolded_results[e][t][gen]) for gen in range(len(exp.unfolded_results[e][t]))])
            std = np.std([avg(exp.unfolded_results[e][t][gen]) for gen in range(len(exp.unfolded_results[e][t]))])
            ys += [y]
            stds += [std]
        params = {'color': 'k'}        
        #plot = plotter.semilogy(xs, ys, **params)[0]
        plot = plotter.plot(xs, ys, **params)[0]
        plotter.plot(xs, upper(ys, stds), xs, lower(ys, stds), alpha=0.1, **params)
        plt.xlabel('diversity weight')
        plt.ylabel('best fitness reached')
        #plt.show()
        plt.savefig('plotx' + str(time.time()) + '.png')
        
        
    if test.name == '|af - fpf|':
        plotter = plt
        plt.figure(t)
        xs = [0.1 * i for i in range(21)]
        ys = []
        stds =  []
        for e,x in enumerate(xs):
            y =      max([avg(exp.unfolded_results[e][t][gen]) for gen in range(len(exp.unfolded_results[e][t]))]) - min([avg(exp.unfolded_results[e][t][gen]) for gen in range(len(exp.unfolded_results[e][t]))])
            std = np.std([avg(exp.unfolded_results[e][t][gen]) for gen in range(len(exp.unfolded_results[e][t]))])
            ys += [y]
            stds += [std]
        params = {'color': 'k'}
        #plot = plotter.semilogy(xs, ys, **params)[0]
        plot = plotter.plot(xs, ys, **params)[0]
        plotter.plot(xs, upper(ys, stds), xs, lower(ys, stds), alpha=0.1, **params)
        plt.xlabel('diversity weight')
        plt.ylabel('max |af - fpf| - min |af - fpf|')
        plt.savefig('plotxd' + str(time.time()) + '.png')