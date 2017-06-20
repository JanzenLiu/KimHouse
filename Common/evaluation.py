import pandas as pd
import numpy as np

def rmsle(pred, y):
	return np.sqrt(np.mean((np.log(pred)-np.log(y))**2))

def rmse(pred, y):
	return np.sqrt(np.mean((pred-y)**2))