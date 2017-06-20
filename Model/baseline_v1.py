import sys
sys.path.append('../')
from Common import *
from Preprocess import bld


train_size_ratio = 0.7
train_size = int(train.shape[0] * train_size_ratio)


hr = HouseReader()
df_train = bld.preprocess(train).copy()
df_test = bld.preprocess(test).copy()
X_train = df_train.drop(['price_doc'],1)
X_test = df_test
y_train = np.log(train['price_doc'])


X1_train = X_train[hr.bld_feats]
X1_test = X_test[hr.bld_feats]


lr_model = LinearRegression(normalize=True)
lr_model.fit(X1_train[:train_size], y_train[:train_size])
# lr_score = lr_model.score(X1_train[train_size:], y_train[train_size:])
lr_pred_val = lr_model.predict(X1_train[train_size:])
lr_score = rmse(lr_pred_val, y_train[train_size:])
print('Score of Linear Regression is: %f' % lr_score)
ridge_model = Ridge()
ridge_model.fit(X1_train[:train_size], y_train[:train_size])
# ridge_score = ridge_model.score(X1_train[train_size:], y_train[train_size:])
ridge_pred_val = ridge_model.predict(X1_train[train_size:])
ridge_score = rmse(ridge_pred_val, y_train[train_size:])
print('Score of Ridge is %f' % ridge_score)

pred_lr = np.exp(lr_model.predict(X1_test))
pred_ridge = np.exp(ridge_model.predict(X1_test))

res = pd.DataFrame({'id':test['id'], 'price_doc':pred_ridge})
res.to_csv('../baseline_v1.csv', index=False)