#!/usr/bin/env python
# -*- coding: utf-8 -*-
from IPython import embed
from EIInterface import *
from scipy.stats import *
from itertools import combinations
import numpy as np
import scipy as sp
import scipy.stats
import csv
from sklearn.cross_validation import KFold

def divide_in_folds(file_name,num_folds):
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

	if(num_folds >1):
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
	else:
		rows_to_write = [[]]
		rows_to_write[0] = ["MUNICIPIO","Y","X","W1","W2","N"]
		rows_to_write =  rows_to_write + rows
		with open("../data/"+file_name+"fold_0", 'wb') as f:
			writer = csv.writer(f)
			writer.writerows(rows_to_write)

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
	# datasets = ['all_gt_age.csv','all_gt_gender.csv']
	# datasets = ['age_group1.csv','age_group2.csv','gender_group1.csv','gender_group2.csv']
	datasets = ['range1_gt_age.csv','range2_gt_age.csv','all_gt_age.csv',
						'range2_gt_genero.csv','range1_gt_genero.csv', 'all_gt_gender.csv']

	results = {
		'imai':None,
		'king':None,
		'wake':None
	}

	# RMSE calculations
	# n_folds = 10
	# for dataset in datasets:
	# 	for method in methods:
	# 		results_RMSE = []
	# 		eiInterface = EIInterface(method)
	# 		divide_in_folds(dataset,n_folds)
	# 		for fold in range(0,n_folds):
	# 			eiInterface.run_inference(dataset+"fold_"+str(fold), params[method],True)	
	# 			results_RMSE.append((eiInterface.calculate_error_metrics(dataset+"fold_"+str(fold))))				
	# 		print("\nDataset {}, method {}".format(dataset,method))
	# 		print("RMSE W1: {}".format(mean_confidence_interval([result['RMSE_W1'] for result in results_RMSE if "no_file_available" not in result.keys()])))
	# 		print("RMSE W2: {}".format(mean_confidence_interval([result['RMSE_W2'] for result in results_RMSE if "no_file_available" not in result.keys()])))

	for dataset in datasets:
		for method in methods:
			eiInterface = EIInterface(method)
			eiInterface.run_inference(dataset, params[method],True)	
			results[method] = ((eiInterface.calculate_error_metrics(dataset)))

		# Print for boxplots
		# print("\nDataset {}".format(dataset))
		for method in methods:
			if 'all' in dataset:
				grupo = "Grupo 3"
			elif 'range2' in dataset:
				grupo = "Grupo 2"
			else:
				grupo = "Grupo 1"

			if 'age' in dataset:
				dataset_name = "Idade "
			else:
				dataset_name = "Gênero "
			mean, bt, up, ci = mean_confidence_interval(results[method]['ABSOLUTE_ERRORS_W1'])
			print("{},{},{},{},{},{},{}".format(method,grupo,mean, bt,up, ci, dataset_name+"W1"))
			mean, bt, up, ci = mean_confidence_interval(results[method]['ABSOLUTE_ERRORS_W2'])
			print("{},{},{},{},{},{},{}".format(method,grupo,mean, bt,up, ci, dataset_name+"W2"))		
		
		# print("\nDataset {}".format(dataset))
		# for method in methods:
		# 	print("MAE W1 {}: {} +- {}".format(method,results[method]['MAE_W1'],mean_confidence_interval(results[method]['ABSOLUTE_ERRORS_W1'])))			
		# print("\n")
		# for method in methods:
		# 	print("MAE W2 {}: {} +- {}".format(method,results[method]['MAE_W2'],mean_confidence_interval(results[method]['ABSOLUTE_ERRORS_W2'])))			
		# print("\n")

		# statistical tests 
		# for comb in combinations(methods,2):
		# 	print("Wilcoxon test between {}".format(comb))		
		# 	print(wilcoxon(results[comb[0]]['ABSOLUTE_ERRORS_W1'],results[comb[1]]['ABSOLUTE_ERRORS_W1']))	
		# 	print(wilcoxon(results[comb[0]]['ABSOLUTE_ERRORS_W2'],results[comb[1]]['ABSOLUTE_ERRORS_W2']))	
		# print('\n')
		# for comb in combinations(methods,2):
		# 	print("T-test test between {}".format(comb))		
		# 	print(ttest_rel(results[comb[0]]['ABSOLUTE_ERRORS_W1'],results[comb[1]]['ABSOLUTE_ERRORS_W1']))	
		# 	print(ttest_rel(results[comb[0]]['ABSOLUTE_ERRORS_W2'],results[comb[1]]['ABSOLUTE_ERRORS_W2']))	
		# print('\n')

