from IPython import embed
from EIInterface import *


def mean_confidence_interval(data, confidence=0.95):
  a = 1.0*np.array(data)
  n = len(a)
  m, se = np.mean(a), sp.stats.sem(a)
  h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
  return m, m-h, m+h, h


if __name__ == "__main__":
	methods = ['imai','king','wake']
	params = {
		'imai': [],
		'king': [],
		'wake': []
	}
	datasets = ['all_gt_age.csv','all_gt_gender.csv']

