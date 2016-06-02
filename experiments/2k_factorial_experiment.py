from itertools import combinations
from EIInterface import *
from sklearn.cross_validation import KFold
from IPython import embed
import numpy as np
import scipy as sp
import scipy.stats
import csv
from pyDOE import *

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


def get_factors_by_config(config, method_name):
	config = [0 if c == -1 else 1 for c in config]		
	if method_name=='imai':
		mu0 = ['0','1']
		tau0 = ['2','4']
		nu0 = ['4','6']
		# return [mu0[config[0]],tau0[config[1]],nu0[config[2]]]
		s0 = ['10','15']
		mustart = ['0','2']
		sigmastart = ['10','15']
		return [mu0[config[0]],tau0[config[1]],nu0[config[2]],s0[config[3]],mustart[config[4]],sigmastart[config[5]]]
	if method_name == 'king':
		ehro = ['0.5','1']
		esigma = ['0.5','1']
		ebeta = ['0.5','1']
		return [ehro[config[0]],esigma[config[1]],ebeta[config[2]]]
	if method_name == "wake":
		m0 = ['0','0.5']
		M0 = ['2.3','3']
		m1 = ['0','0.5']
		M1 = ['2.3','3']
		a0 = ['0.8','1']
		b0 = ['0.01','0.03']
		a1 = ['0.8','1']
		b1 = ['0.01','0.03']
 		return [m0[config[0]],M0[config[1]],m1[config[2]],M1[config[3]],a0[config[4]],b0[config[5]],a1[config[6]],b1[config[7]]]

method_name = 'wake'
# method_name = 'imai'
# method_name = 'king'

dataset_name = "all_gt_age.csv"
n_folds = 1

num_param  = 6 if method_name == 'imai' else 3 if method_name == 'king' else 8 
# num_param  = 3 if method_name == 'imai' else 3 if method_name == 'king' else 8 
print(num_param)
factorial_project_2k = ff2n(num_param)
number_of_replications = 1

y_W1 = []
y_W2 = []
for rep in range(0,number_of_replications):
	print("Replication {} of method {} 2^{} factorial project.".format(rep+1,method_name,num_param))
	for params in factorial_project_2k:
		params = get_factors_by_config(list(params),method_name)
		print(params)
		divide_in_folds(dataset_name,n_folds)
		results = []
		for fold in range(0,n_folds):
			method_interface = EIInterface(method_name)
			method_interface.run_inference(dataset_name+"fold_"+str(fold), params)
			results.append((method_interface.calculate_error_metrics(dataset_name+"fold_"+str(fold))))
		
		mu_W1 = [result['RMSE_W1'] for result in results if "no_file_available" not in result.keys()]
		mu_W2 = [result['RMSE_W2'] for result in results if "no_file_available" not in result.keys()]
		mu_W1 = sum(mu_W1)/len(mu_W1)
		mu_W2 = sum(mu_W2)/len(mu_W2)

		y_W1.append(mu_W1)
		y_W2.append(mu_W2)	
		# print(results)
		print(mean_confidence_interval([result['RMSE_W1'] for result in results if "no_file_available" not in result.keys()]))
		print(mean_confidence_interval([result['RMSE_W2'] for result in results if "no_file_available" not in result.keys()]))

print(y_W1)
print(y_W2)

# With replication
# means_W1 = []
# means_W2 = []
# for result in y_W1:
# 	means_W1.append(sum(result)/len(result))
# for result in y_W2:
# 	means_W2.append(sum(result)/len(result))
# q_W1 = []
# q_W2 = []
# q_W1.append(sum(means_W1)/len(means_W1))
# q_W2.append(sum(means_W2)/len(means_W2))
# for factor in range(0,num_param):
# 	q_factor = 0
# 	i=0
# 	for config in factorial_project_2k:
# 		print(config[factor])
# 		print(means_W1[i])
# 		q_factor+=config[factor] * means_W1[i]
# 		i+=1
# 	q_factor = q_factor/i
# 	q_W1.append(q_factor)
# 	q_factor = 0
# 	i=0
# 	for config in factorial_project_2k:
# 		print(config[factor])
# 		print(means_W2[i])
# 		q_factor+=config[factor] * means_W2[i]
# 		i+=1
# 	q_factor = q_factor/i
# 	q_W2.append(q_factor)

# SSE_W1 = 0
# SSE_W2 = 0
# for i,prediction_list in enumerate(y_W1):
# 	for pred in prediction_list:
# 		SSE_W1 += (pred-means_W1[i]) * (pred-means_W1[i])
# for i,prediction_list in enumerate(y_W2):
# 	for pred in prediction_list:
# 		SSE_W2 += (pred-means_W2[i]) * (pred-means_W2[i])

# SS_W1 = []
# SS_W2 = []
# for q in q_W1:
# 	SS_W1.append(pow(2,num_param) * number_of_replications * pow(q,2))
# for q in q_W2:
# 	SS_W2.append(pow(2,num_param) * number_of_replications * pow(q,2))

# SSY_W1 = 0
# SSY_W2 = 0
# for prediction_list in y_W1:
# 	for y in prediction_list:
# 		SSY_W1+= pow(y,2)
# for prediction_list in y_W2:
# 	for y in prediction_list:
# 		SSY_W2+= pow(y,2)		

# SST_W1 = SSY_W1 - SS_W1[0]
# SST_W2 = SSY_W2 - SS_W2[0]

# Without replications
q_W1 = []
q_W2 = []

# Adding iterations factors
iteraction_factors = []
for i in range(2,num_param+1):
	for perm in combinations(range(0,num_param),i):
		iteraction_factors.append(list(perm))

# embed()

factorial_project_2k = factorial_project_2k.tolist()
for iterations in iteraction_factors:
	for i in range(0,len(factorial_project_2k)):
		to_append = 1
		for iteration in iterations:
			to_append*=factorial_project_2k[i][iteration]
		factorial_project_2k[i].append(to_append)

for factor in range(0,len(factorial_project_2k[0])):
	q_factor = 0
	i=0
	for config in factorial_project_2k:
		print factor
		print i
		print config		
		print(config[factor])
		print(y_W1[i])
		q_factor+=config[factor] * y_W1[i]
		i+=1
	q_factor = q_factor/i
	q_W1.append(q_factor)
	q_factor = 0
	i=0
	for config in factorial_project_2k:
		print(config[factor])
		print(y_W2[i])
		q_factor+=config[factor] * y_W2[i]
		i+=1
	q_factor = q_factor/i
	q_W2.append(q_factor)

SS_W1 = []
SS_W2 = []
for q in q_W1:
	SS_W1.append(pow(2,num_param) * pow(q,2))
for q in q_W2:
	SS_W2.append(pow(2,num_param)  * pow(q,2))

SST_W1 = sum(SS_W1)
SST_W2 = sum(SS_W2) 

print("W1")
for factor in range(0,len(factorial_project_2k[0])):
	print("Fator {}, Porcentagem: {}%".format(factor,SS_W1[factor]/SST_W1))

print("W2")
for factor in range(0,len(factorial_project_2k[0])):
	print("Fator {}, Porcentagem: {}%".format(factor,SS_W2[factor]/SST_W2))

# embed()