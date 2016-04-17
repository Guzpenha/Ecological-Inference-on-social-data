import os
from sklearn.metrics import *
from math import sqrt
import os.path

class EIInterface:
	method_name = ""

	def __init__(self, name="king"):
		self.method_name = name

	def run_inference(self,data_file):
		print("-------------------------------------------------------------")
		print("Running "+self.method_name+"'s inference on file "+data_file+".\n")		
		os.system("Rscript --vanilla inference_"+self.method_name+".R "+ data_file)
		print("Finished.")
		print("-------------------------------------------------------------\n")

	def calculate_error_metrics(self,ground_truth_file):
		if(not os.path.isfile("../results/predicted_W1_"+self.method_name + ground_truth_file)):
			return {"no_file_available":True}
		f = open("../results/predicted_W1_"+self.method_name + ground_truth_file)
		predicted_W1= []
		for line in f:
			for value in line.split(","):
				predicted_W1.append(float(value))				
		f.close()
		
		f = open("../results/predicted_W2_"+self.method_name + ground_truth_file)
		predicted_W2= []
		for line in f:
			for value in line.split(","):
				predicted_W2.append(float(value))
		f.close()

		f = open("../data/" + ground_truth_file)
		true_values_W1 = []
		true_values_W2 = []
		first = True
		for line in f:
			if(first):
				first=False
				continue
			if(int(line.split(",")[-1])<=100):
				break
			true_values_W1.append(float(line.split(",")[-3]))
			true_values_W2.append(float(line.split(",")[-2]))
		f.close()
		return {
			"RMSE_W1": sqrt(mean_squared_error(predicted_W1, true_values_W1)),
			"RMSE_W2": sqrt(mean_squared_error(predicted_W2, true_values_W2)),
			"MAE_W1": mean_absolute_error(predicted_W1, true_values_W1),
			"MAE_W2": mean_absolute_error(predicted_W2, true_values_W2)
		}		