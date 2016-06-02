from itertools import combinations
from IPython import embed

results_file = open('results')
values = []
for line in results_file:
	values.append(float(line))

iteraction_factors = []
factors_values = []
j =0
for i in range(2,9):
	for perm in combinations(['A','B','C','D','E','F','G','H'],i):
		iteraction_factors.append(list(perm))		
		factors_values.append( (''.join(list(perm)), values[j]) )
		j+=1

sorted_values = sorted(factors_values, key=lambda tup: -tup[1])

print(sorted_values[0:10])

embed()
