import sys
sys.path.append('../')
from Common import *
from Preprocess import y_train_raw

# special price values
# 2000000     757
# 1000000     747
# 3000000     332

# r_train = y_train_raw.map(lambda x : 0 if (x < 1500000) else 1 if (x >= 1500000 and x < 2500000) else 2 if (x >= 2500000 and x < 3300000) else 3)
r_train = y_train_raw.map(lambda x : 0 if x == 1000000 else 1 if x == 2000000 else 2 if x == 3000000 else 3)

df0 = train[r_train < 3]
df1 = train[r_train == 3]

df0 = train[r_train == 0]
df1 = train[r_train == 1]
df2 = train[r_train == 2]
df3 = train[r_train == 3]

# params = {'max_depth':5, 'eta':0.03, 'silent':0, 'subsample':0.7, 'colsample_bytree':0.7, 
# 	'task':'multi:softmax', 'num_class':4}
# num_round = 500
# bst = xgb.train(params, d_train, num_round)
# pred = bst.predict(d_train)

# print((pred != r_train).sum() / X_train.shape[0])

sns.distplot(df0['build_year'], kde=False)
sns.distplot(df3['build_year'], kde=False)
plt.show()

sns.kdeplot(df0['build_year'], label='$990,000 or 1,000,000')
sns.kdeplot(df1['build_year'], label='$2,000,000')
sns.kdeplot(df2['build_year'], label='$3,000,000')
sns.kdeplot(df3['build_year'], label='others')
plt.show()

sns.distplot(df0['build_year'], kde=False, color='b')
sns.distplot(df1['build_year'], kde=False, color='y')
sns.distplot(df2['build_year'], kde=False, color='r')
# sns.distplot(df3['build_year'], kde=False, color='g')	
plt.show()

def plot_kde_log(feat):
	sns.kdeplot(np.log1p(df0[feat]), label='$990,000 or 1,000,000')
	sns.kdeplot(np.log1p(df1[feat]), label='$2,000,000')
	sns.kdeplot(np.log1p(df2[feat]), label='$3,000,000')
	sns.kdeplot(np.log1p(df3[feat]), label='others')
	plt.show()

def print_values(feat):
	res = pd.Series()
	for df in [df0, df1, df2, df3]:
		res = pd.concat([res, pd.DataFrame({'val': df[feat].value_counts().values})], axis=1)
	return res.iloc[:,1:]

def print_ratios(feat):
	res = pd.Series()
	for df in [df0, df1, df2, df3]:
		res = pd.concat([res, pd.DataFrame({'ration': df[feat].value_counts().values / df.shape[0]})], axis=1)
	return res.iloc[:,1:]

def print_ratio(feat, value):
	for df in [df0, df1, df2, df3]:
		print((df[feat]==value).sum() / df.shape[0])

df0 = train[r_train < 3]
df3 = train[r_train == 3]