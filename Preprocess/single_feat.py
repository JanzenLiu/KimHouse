from header import *

# TODO: remove the redundant xlabel of timestamp plot
# TODO: eliminate the influence of start/end time in the middle of a year to timestamp distribution

# combine['timestamp'].nunique()
# 1435

# combine['timestamp'].value_counts().sort_values(ascending=False).head()
# 2014-12-16    160
# 2014-12-09    147
# 2014-06-30    133
# 2014-12-18    118
# 2014-11-25     93

# combine['timestamp'].sort_values().iloc[0]
# combine['timestamp'].sort_values().iloc[-1]
# 2011-08-20
# 2016-05-30

combine['trans_year'] = combine['timestamp'].apply(lambda x: int(x[:4]))
combine['trans_month'] = combine['timestamp'].apply(lambda x: int(x[5:7]))
combine['trans_day'] = combine['timestamp'].apply(lambda x: int(x[8:]))

def plt_timestamp_count()
	plt.figure(figsize=(12,8))
	sns.countplot(x='timestamp', data=combine) # TODO 1
	plt.show()

def plot_split_timestamp_count(): # TODO 2
	plt.figure(figsize=(12,15))
	plt.subplot(311)
	sns.countplot(x='trans_year', data=combine)
	plt.subplot(312)
	sns.countplot(x='trans_month', data=combine)
	plt.subplot(313)
	sns.countplot(x='trans_day', data=combine)
	plt.show()

plt_timestamp_count()
plot_split_timestamp_count()