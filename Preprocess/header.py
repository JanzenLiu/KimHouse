# for seaborn issue
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import stats

mpl.rcParams['figure.figsize'] = (12, 8)

train = pd.read_csv('../Data/train.csv')
test = pd.read_csv('../Data/test.csv')
macro = pd.read_csv('../Data/macro.csv')
combine = pd.concat([train.drop(['price_doc'], 1), test])

log_file = "log.txt"

def log(msg, title=None, filename=None):
	if(not filename):
		filename = log_file
	if(type(msg) != str):
		msg = format(msg)
	with open(filename, "a") as f:
		if(title):
			f.write("# " + title + "\n")
		f.write(msg + "\n\n")