import sys
sys.path.append('../')
from Common import *
from Preprocess.baseline_v1  import preprocess

hr = HouseReader()
train = preprocess(train)
test = preprocess(test)
X_train = train.drop(['price_doc'],1)
X_test = test
y_train = train['price_doc']


X1_train = X_train[hr.bld_feats]
X1_test = X_test[hr.bld_feats]


train_size_ratio = 0.7
train_size = int(train.shape[0] * train_size_ratio)


lr_model = LinearRegression(normalize=True)
lr_model.fit(X1_train[:train_size], np.log(y_train[:train_size]))
# lr_score = lr_model.score(X1_train[train_size:], y_train[train_size:])
lr_pred_val = lr_model.predict(X1_train[train_size:])
lr_pred_val = np.exp(lr_pred_val)
lr_score = rmsle(lr_pred_val, y_train[train_size:])
print('Score of Linear Regression is: %f' % lr_score)
ridge_model = Ridge()
ridge_model.fit(X1_train[:train_size], np.log(y_train[:train_size]))
# ridge_score = ridge_model.score(X1_train[train_size:], y_train[train_size:])
ridge_pred_val = ridge_model.predict(X1_train[train_size:])
ridge_pred_val = np.exp(ridge_pred_val)
ridge_score = rmsle(ridge_pred_val, y_train[train_size:])
print('Score of Ridge is %f' % ridge_score)

pred_lr = lr_model.predict(X1_test)
pred_ridge = ridge_model.predict(X1_test)

res = pd.DataFrame({'id':test['id'], 'price_doc':pred_ridge})
# res.to_csv('../baseline_v1.csv', index=False)