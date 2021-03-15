import sys
sys.path += ['../']
from evolib import *
from explib import *
from divlib import *
from optlib import *
from problib import *

from scipy.stats import pearsonr

def em_distance(list1, list2):
    total_distance = 0
    for i1,item1 in enumerate(list1):
        single_distance = 0
        for i2,item2 in enumerate(list2):
            if item1 == item2:
                single_distance = abs(i1 - i2)
                break
        total_distance += single_distance
    return total_distance

AgeTest = Test("age").with_function(lambda pop: avg([individual.age for individual in pop.individuals])).with_live(True)


tests = []

tests += [Test("best fitness")]
tests += [Test("secondary fitness").with_function(lambda pop: pop.best().compute_secondary_fitness(pop)).with_live(True)]
tests += [Test("augmented fitness").with_function(lambda pop: pop.best().evaluate(pop)).with_live(True)]
# tests += [Test("dynamic pf").with_function(lambda pop: pop.best_pf()).with_live(False)]
# tests += [Test("opf").with_function(lambda pop: pop.best_opf()).with_live(False)]


# tests += [ContextTest("f increase").with_function(lambda pop, context: pop.best().compute_problem_fitness() - context['all_populations'][context['current_gen']-1].best().compute_problem_fitness())]
# tests += [ContextTest("pf increase").with_function(lambda pop, context: pop.best_pf() - context['all_populations'][context['current_gen']-1].best_pf())]

# f_full  = lambda pop, context: pop.best_f()  / context['all_populations'][-1].best_f()
# pf_full = lambda pop, context: pop.best_pf() / context['all_populations'][-1].best_pf()
# tests += [ContextTest(" f %").with_function(f_full).with_live(False)]
# tests += [ContextTest("pf %").with_function(pf_full).with_live(False)]

# final_descendants = lambda pop, con: avg([len(con["all_populations"][-1].filter_descendants(individual)) for individual in pop.individuals])
# tests += [ContextTest("descendants survive").with_function(final_descendants).with_live(False)]

def get_pop(con, offset=0):
    return con["all_populations"][max(0, min(con["current_gen"]+offset, len(con["all_populations"])-1))]

# pf_for = lambda individual, con, x: con["all_populations"][min(con["current_gen"]+x, len(con["all_populations"])-1)].compute_pf_here(individual) or 0.0
#
# onepf = lambda pop, con: avg([pf_for(individual, con, 1) for individual in pop.individuals])
# tenpf = lambda pop, con: avg([pf_for(individual, con, 10) for individual in pop.individuals])
# tests += [ContextTest(" 1-pf").with_function(onepf).with_live(False)]
# tests += [ContextTest("10-pf").with_function(tenpf).with_live(False)]


fpf_for = lambda individual, con: con["all_populations"][-1].compute_pf_here(individual) or 0.0
#
fpf = lambda pop, con: avgex([fpf_for(individual, con) for individual in pop.individuals])
# fpf_norm = lambda pop, con: fpf(pop, con) / con["all_populations"][-1].best_f()
# fpf_incr = lambda pop, con: fpf(pop, con) - fpf(con["all_populations"][max(con['current_gen']-1, 0)], con)
tests += [ContextTest("fpf").with_function(fpf).with_live(False)]
# tests += [ContextTest("fpf norm").with_function(fpf_norm).with_live(False)]
# tests += [ContextTest("fpf incr").with_function(fpf_incr).with_live(False)]

ffpf  = lambda pop, con: avg([abs(individual.compute_problem_fitness() - fpf_for(individual, con)) for individual in pop.individuals])
affpf = lambda pop, con: avg([abs(individual.get_fitness()             - fpf_for(individual, con)) for individual in pop.individuals])

tests += [ContextTest(" |f - fpf|").with_function(ffpf).with_live(False)]
tests += [ContextTest("|af - fpf|").with_function(affpf).with_live(False)]
# tests += [ContextTest("potential gain").with_function(lambda pop, con: abs(affpf(pop, con) - ffpf(pop, con))).with_live(False)]
tests += [ContextTest("delta |af - fpf|").with_function(lambda pop, con: affpf(get_pop(con, -1), con) - affpf(pop, con)).with_live(False)]


exp = Experiment(NormalizedRoomWalk(step_count=5, step_size=0.33),
    population_class=HistoricalPopulation,
    mig=0.1,
    pop_size=50,
    num_gens=500,
    num_runs=25,
    diversity_sample=10,
    save_file=True,
    separate_subplots=True)
for test in tests:
    exp.add_test(test).with_style(ls="-")


for weight in [0.1 * i for i in range(11)]:
    exp.perform(individual_class=NormalizedManhattanDiversityIndividual,
        diversity_weight=weight,
        style=dict(color=(0, 0, weight), ls='-'),
        label='manhattan diverse, weight ' + str(weight))
# exp.perform(individual_class=Individual,
#     style=dict(color=(0, 0, 0)),
#     label='non-diverse')
exp.save_dill()
exp.save_all_results()
#exp.print_verdict()
#exp.print_examples()

#exp.plot(correlate_with=AvgOptProductiveFitnessTest)
exp.plot(show_legend=False)
