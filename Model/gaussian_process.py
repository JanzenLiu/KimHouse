import sys
sys.path.append('../')
from Common import *
from Preprocess import X_train, X_test, y_train

print(X_train.shape[1], "features used")
train_size_ratio = 0.7
train_size = int(train.shape[0] * train_size_ratio)

gpr_model = GaussianProcessRegressor()
gpr_model.fit(X_train[:train_size], y_train[:train_size])
gpr_pred_val = gpr_model.predict(X_train[train_size:])
gpr_score = rmse(gpr_pred_val, y_train[train_size:])
print('Score of Gaussian Process Regression is: %f' % gpr_score)