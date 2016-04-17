from EIInterface import *
from sklearn.cross_validation import KFold
from IPython import embed
import numpy as np
import scipy as sp
import scipy.stats
import csv

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), sp.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h, h

def divide_in_folds(file_name,num_folds):
	rows = []
	with open("../data/"+dataset_name, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		first = True
		for row in spamreader:			
				if(first):
					first=False
					continue
				if(int(row[-1])<=100):
					break
				else:
					rows.append(row)
	kf = KFold(n=len(rows), n_folds=num_folds, shuffle=False,random_state=None)
	positions = np.array(rows)
	fold =0
	for train_index, test_index in kf:
		rows_train = [[]]
		rows_train[0] = ["MUNICIPIO","Y","X","W1","W2","N"]
		rows_train = rows_train +  positions[train_index].tolist()		 
		with open("../data/"+file_name+"fold_"+str(fold), 'wb') as f:
			writer = csv.writer(f)
			writer.writerows(rows_train)
		fold+=1

# method_name = 'wake'
method_name = 'imai'
# method_name = 'king'
dataset_name = "all_gt_age.csv"
n_folds = 10

divide_in_folds(dataset_name,n_folds)
results = []
for fold in range(0,n_folds):
	king_interface = EIInterface(method_name)
	king_interface.run_inference(dataset_name+"fold_"+str(fold))
	results.append((king_interface.calculate_error_metrics(dataset_name+"fold_"+str(fold))))
print(results)
print(mean_confidence_interval([result['RMSE_W1'] for result in results if "no_file_available" not in result.keys()]))