import sys
sys.path.append('../')
from Common import *

hr = HouseReader()

# train.plot.scatter('material','price_doc',logy=True,alpha=0.3,s=30)
# train.plot.scatter('material','price_doc',logy=True,alpha=0.2,s=50)
for col in hr.num_feats:
    if train[col].nunique() <= 5:
        train.plot.scatter(col,'log_price',alpha=0.2)       
for col in hr.num_feats:
    if train[col].nunique() < 1000:
        plt.figure(figsize=(12,8))
        train.dropna(subset=[col]).plot.scatter(col,'price_doc',logy=True,alpha=0.2)
        filename = format("%s_log.png"%col)
        plt.savefig(os.path.join('../Figure/Raw/Scatter/',filename))
        plt.close()
