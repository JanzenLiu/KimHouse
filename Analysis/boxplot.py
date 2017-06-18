import sys
sys.path.append('../')
from Common import *

hr = HouseReader()

sns.boxplot(x="ecology",y="price_doc",data=train)
plt.show()
train['log_price']=np.log(train['price_doc'])
sns.boxplot(x="ecology",y="log_price",data=train)
plt.show()
mpl.rcParams['figure.figsize']=(12.0,8.0)
sns.boxplot(x="ecology",y="log_price",data=train);plt.show()


for col in hr.cat_feats:
    if col != 'timestamp' and col != 'sub_area':
        plt.figure()
        sns.boxplot(x=col,y="price_doc",data=train)
        plt.show()
        plt.figure()
        sns.boxplot(x=col,y="log_price",data=train)
        plt.show()

sns.boxplot(x="sub_area", y="price_doc",data=train)
sns.boxplot(x="sub_area", y="log_price",data=train)
subarea_sorted=train.groupby('sub_area')['price_doc'].mean().sort_values(ascending=False)
sns.boxplot(x="sub_area", y="price_doc",data=train, order=subarea_sorted.index)
sns.boxplot(x="sub_area", y="log_price",data=train, order=subarea_sorted.index)
subarea_log_sorted=train.groupby('sub_area')['log_price'].mean().sort_values(ascending=False)
sns.boxplot(x="sub_area", y="log_price",data=train, order=subarea_log_sorted.index)
