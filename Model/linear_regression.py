import sys
sys.path.append('../')
from Common import *
from Preprocess import X_train, X_test, y_train

print(X_train.shape[1], "features used")
train_size_ratio = 0.7
train_size = int(train.shape[0] * train_size_ratio)


lr_model = LinearRegression(normalize=True)
lr_model.fit(X_train[:train_size], y_train[:train_size])
# lr_score = lr_model.score(X_train[train_size:], y_train[train_size:])
lr_pred_val = lr_model.predict(X_train[train_size:])
lr_score = rmse(lr_pred_val, y_train[train_size:])
print('Score of Linear Regression is: %f' % lr_score)
ridge_model = Ridge()
ridge_model.fit(X_train[:train_size], y_train[:train_size])
# ridge_score = ridge_model.score(X_train[train_size:], y_train[train_size:])
ridge_pred_val = ridge_model.predict(X_train[train_size:])
ridge_score = rmse(ridge_pred_val, y_train[train_size:])
print('Score of Ridge is %f' % ridge_score)

pred_lr = np.exp(lr_model.predict(X_test))
pred_ridge = np.exp(ridge_model.predict(X_test))

res = pd.DataFrame({'id':test['id'], 'price_doc':pred_ridge})
# res.to_csv('../Predictions/baseline_v12.csv', index=False)