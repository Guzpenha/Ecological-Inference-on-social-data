import numpy as np
from IPython import embed
from EIInterface import *
import itertools

def grid_search(method,params,dataset,replications =1 ):
	best_params = []
	best_result = 10

	combinations = list(itertools.product(*params))
	print("Running {} combinations with {} replications.".format(len(combinations),replications))
	for rep in range(0,replications):
		for param in combinations:
			eiInterface = EIInterface(method)
			eiInterface.run_inference(dataset, param, False)		
			results = (eiInterface.calculate_error_metrics(dataset))
			mae_W1 = results['MAE_W1']
			print("result: {} params: {}".format(mae_W1,param))
			if mae_W1 < best_result:
				best_result = mae_W1
				best_params = param

	return (best_result,best_params)

if __name__ == "__main__":
	# king
	# dataset = 'all_gt_gender.csv'	
	# method = 'king'	
	# params = [
	# 	[str(v) for v in [x * -0.1 for x in range(1, 5)]] + [str(v) for v in [x * 0.1 for x in range(0, 5)]],
	# 	[str(v) for v in [x * -0.1 for x in range(1, 5)]] + [str(v) for v in [x * 0.1 for x in range(0, 5)]],
	# 	['0.5']
	# ]	

	# imai
	# dataset = 'all_gt_gender.csv'
	# method = 'imai'
	# params = [
	# # ['0' ,'1'],
	# [str(v) for v in [x * 0.1 for x in range(0, 5)]]	,
	# ['0','1','2'],
	# ['6'],
	# ['15'],
	# ['0'],
	# ['15','16','17','18','19']
	# ]
	
	# wake
	dataset = 'all_gt_gender.csv'
	method = 'wake'
	params = [
	  [str(v) for v in [x * 0.1 for x in range(0, 3)]],
		['2.3','2.5','2.7'],
		[str(v) for v in [x * 0.1 for x in range(0, 3)]],
		['2.3','2.5','2.7'],
		['0.7','0.8','0.9'],
		['0.01','0.03','0.08'],
		['0.7','0.8','0.9'],
		['0.01','0.03','0.08']
	]

	best_result, best_params = (grid_search(method,params,dataset))

	print("Best result: {}.".format(best_result))
	print("Best params: {}.".format(best_params))

