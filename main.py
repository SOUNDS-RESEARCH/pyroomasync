from simulator import simulate
from analysis import compare_doa_estimators

results = simulate()
compare_doa_estimators(results)
