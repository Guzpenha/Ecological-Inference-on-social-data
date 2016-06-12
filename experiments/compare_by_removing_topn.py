from IPython import embed
from EIInterface import *
from scipy.stats import *
from itertools import combinations
import numpy as np
import scipy as sp
import scipy.stats
import csv
from sklearn.cross_validation import KFold

def  make_data_removing_top_n(file_name,k=100):
	rows = []
	with open("../data/"+file_name, 'rb') as csvfile:
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
	
	for i in range(0,k):
		positions = np.array(rows)
		rows_train = [[]]
		rows_train[0] = ["MUNICIPIO","Y","X","W1","W2","N"]														
		rows_train = rows_train + positions[i:len(rows)].tolist()
		# print(len(rows_train))
		with open("../data/"+file_name+"removing_"+str(i), 'wb') as f:
				writer = csv.writer(f)
				writer.writerows(rows_train)

if __name__ == "__main__":

	methods = ['imai','king','wake']
	params = {
		'imai': ['0.1','0','6','15','0','19'],
		'king': ['-0.3','0.3','0.5'],
		'wake': ['0.0','2.3','0.1','2.7','0.7','0.08','0.9','0.03']
	}		
	datasets = ['all_gt_age.csv','all_gt_gender.csv']	
	results = {
		'imai':None,
		'king':None,
		'wake':None
	}
	up_to = 150

	for dataset in datasets:
		make_data_removing_top_n(dataset,up_to)
		for i in range(0,up_to):		
			# print("removing {} top N".format(i))
			for method in methods:
				eiInterface = EIInterface(method)
				eiInterface.run_inference(dataset+"removing_"+ str(i), params[method],True)	
				results[method] = ((eiInterface.calculate_error_metrics(dataset+"removing_"+ str(i))))
			
			# print("\nDataset {}".format(dataset))
			for method in methods:
				print("{},{},{},{}".format(dataset,method,i,results[method]['MAE_W1']))			
			# print("\n")
			# for method in methods:
				# print("MAE W2 {}: {}".format(method,results[method]['MAE_W2']))			
			# print("\n")