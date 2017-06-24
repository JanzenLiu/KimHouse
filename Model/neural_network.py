import sys
sys.path.append('../')
from Common import *
from Preprocess import X_train, X_test, y_train

print(X_train.shape[1], "features used")
train_size_ratio = 0.7
train_size = int(train.shape[0] * train_size_ratio)

mlp_model = MLPRegressor((2), max_iter=1000)
mlp_model.fit(X_train[:train_size], y_train[:train_size])
# lr_score = lr_model.score(X_train[train_size:], y_train[train_size:])
mlp_pred_val = mlp_model.predict(X_train[train_size:])
mlp_score = rmse(mlp_pred_val, y_train[train_size:])
print('Score of Nueral Network with %d layers is: %f' % (mlp_model.n_layers_, mlp_score))