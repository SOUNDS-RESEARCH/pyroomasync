from simulator import simulate
from analysis import compare_doa_estimators

results = simulate()
results = compare_doa_estimators(results)
print(results)
