import pandas as pd
import numpy as np

def rmse(pred, y):
	return np.sqrt(np.mean((pred-y)**2))

def rmsle(pred, y):
	return rmse(np.log(pred), np.log(y))