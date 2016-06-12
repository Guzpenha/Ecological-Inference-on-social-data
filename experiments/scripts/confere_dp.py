import numpy as np
from IPython import embed
from EIInterface import *
import itertools

def calculate_sd(method,dataset, replications = 10):
	results = []

	if method =='king':
		param = ['-0.3','0.3','0.5']
	if method == 'wake':
		param = ['0.0','2.3','0.1','2.7','0.7','0.08','0.9','0.03']
	if method == 'imai':
		param = ['0.1','0','6','15','0','19']

	for rep in range(0,replications):	
		eiInterface = EIInterface(method)
		eiInterface.run_inference(dataset, param, True)		
		result = (eiInterface.calculate_error_metrics(dataset))
		results.append(result['MAE_W1'])
		print("result: {}".format(result['MAE_W1']))

	return np.std(results), np.std(results)/np.mean(results)

if __name__ == "__main__":
	
	for method in ['king','imai','wake']:
		sd, cv = calculate_sd(method,"all_gt_gender.csv")
		print("Method {}, sd: {}, cd: {}".format(method,sd,cv))