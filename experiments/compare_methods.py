from IPython import embed
from EIInterface import *
from scipy.stats import *
from itertools import combinations

if __name__ == "__main__":
	methods = ['imai','king','wake']
	params = {
		'imai': ['0','2','4','10','0','10'],
		'king': ['0.5','0.5','0.5'],
		'wake': ['0','2.3','0','2.3','0.8','0.01','0.8','0.01']
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
		print("\n")
		for method in methods:
			print("MAE W2 {}: {} ".format(method,results[method]['MAE_W2']))
		print("\n")

		for comb in combinations(methods,2):
			print("Wilcoxon test between {}".format(comb))		
			print(wilcoxon(results[comb[0]]['ABSOLUTE_ERRORS_W1'],results[comb[1]]['ABSOLUTE_ERRORS_W1']))	
		print('\n')
		for comb in combinations(methods,2):
			print("T-test test between {}".format(comb))		
			print(ttest_rel(results[comb[0]]['ABSOLUTE_ERRORS_W1'],results[comb[1]]['ABSOLUTE_ERRORS_W1']))	
		print('\n')
