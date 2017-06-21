import sys
sys.path.append('../')
sys.path.append('../Preprocess/')
from Common import *
import bld
import caf
import pop

hr = HouseReader()
X_train = train[hr.bld_feats + hr.caf_feats + hr.pop_feats].copy()
X_train = bld.preprocess(X_train)
X_train = caf.preprocess(X_train)
X_train = pop.preprocess(X_train)
X_train = X_train.drop(caf.caf_feats.index, 1)
X_train = X_train.drop(pop.pop_feats, 1)
X_test = test[hr.bld_feats + hr.caf_feats + hr.pop_feats].copy()
X_test = bld.preprocess(X_test)
X_test = caf.preprocess(X_test)
X_test = pop.preprocess(X_test)
X_test = X_test.drop(caf.caf_feats.index, 1)
X_test = X_test.drop(pop.pop_feats, 1)
y_train = np.log(train['price_doc'])