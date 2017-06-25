import sys
sys.path.append('../')
from Common import *
from Preprocess import X_train, X_test, y_train

print(X_train.shape[1], "features used")
train_size_ratio = 0.7
train_size = int(train.shape[0] * train_size_ratio)

d_train = xgb.DMatrix(X_train[:train_size].values, y_train[:train_size].values)
d_val = xgb.DMatrix(X_train[train_size:].values)
d_test = xgb.DMatrix(X_test.values)
D_train = xgb.DMatrix(X_train.values, y_train.values)

params = {'max_depth':5, 'eta':0.03, 'silent':1, 'task':'reg:linear', 'eval_metric':'rmse'}
num_round = 500

bst = xgb.train(params, d_train, num_round)
xgb_pred_val = bst.predict(d_val)
xgb_score = rmse(xgb_pred_val, y_train[train_size:].values)
print('Score of XGBoost (Linear Regression) is: %f' % xgb_score)

# bst = xgb.train(params, D_train, num_round)
# pred_xgb = np.exp(bst.predict(d_test))

# res = pd.DataFrame({'id':test['id'], 'price_doc':pred_xgb})
# res.to_csv('../Predictions/baseline_v17.xgb.2.csv', index=False)