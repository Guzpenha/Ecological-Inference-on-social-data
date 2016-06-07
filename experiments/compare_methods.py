from IPython import embed
from EIInterface import *
from scipy.stats import *
from itertools import combinations
import numpy as np
import scipy as sp
import scipy.stats
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), sp.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h, h

if __name__ == "__main__":
	methods = ['imai','king','wake']
	params = {
		'imai': ['0.1','0','6','15','0','19'],
		'king': ['-0.3','0.3','0.5'],
		'wake': ['0.0','2.3','0.1','2.7','0.7','0.08','0.9','0.03']
	}	
	# datasets = ['all_gt_gender.csv']
	datasets = ['all_gt_age.csv','all_gt_gender.csv']
	results = {
		'imai':None,
		'king':None,
		'wake':None
	}

	for dataset in datasets:
		for method in methods:
			eiInterface = EIInterface(method)
			eiInterface.run_inference(dataset, params[method])	
			results[method] = ((eiInterface.calculate_error_metrics(dataset)))
		
		print("\nDataset {}".format(dataset))
		for method in methods:
			print("MAE W1 {}: {} ".format(method,results[method]['MAE_W1']))
			print("RMSE W1 {}: {} ".format(method,results[method]['RMSE_W1']))
		print("\n")
		for method in methods:
			print("MAE W2 {}: {} ".format(method,results[method]['MAE_W2']))
			print("RMSE W2 {}: {} ".format(method,results[method]['RMSE_W2']))
		print("\n")

		for comb in combinations(methods,2):
			print("Wilcoxon test between {}".format(comb))		
			print(wilcoxon(results[comb[0]]['ABSOLUTE_ERRORS_W1'],results[comb[1]]['ABSOLUTE_ERRORS_W1']))	
			print(wilcoxon(results[comb[0]]['ABSOLUTE_ERRORS_W2'],results[comb[1]]['ABSOLUTE_ERRORS_W2']))	
		print('\n')
		for comb in combinations(methods,2):
			print("T-test test between {}".format(comb))		
			print(ttest_rel(results[comb[0]]['ABSOLUTE_ERRORS_W1'],results[comb[1]]['ABSOLUTE_ERRORS_W1']))	
			print(ttest_rel(results[comb[0]]['ABSOLUTE_ERRORS_W2'],results[comb[1]]['ABSOLUTE_ERRORS_W2']))	
		print('\n')
