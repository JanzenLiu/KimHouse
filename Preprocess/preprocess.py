import sys
sys.path.append('../')
sys.path.append('../Preprocess/')
from Common import *
import bld, caf, pop, ofc, rel, bus, cul, edu, ind, spt, env, non, nbr, trp

X_train = train[hr.bld_feats + hr.caf_feats + hr.pop_feats + hr.ofc_feats + hr.rel_feats + \
	hr.bus_feats + hr.cul_feats + hr.edu_feats + hr.ind_feats + hr.spt_feats + hr.env_feats + \
	hr.non_feats + hr.nbr_feats + hr.trp_feats].copy()
X_train = bld.preprocess(X_train)
X_train = caf.preprocess(X_train)
X_train = pop.preprocess(X_train)
X_train = ofc.add_feats(X_train)
X_train = rel.add_feats(X_train)
X_train = bus.add_feats(X_train)
X_train = cul.preprocess(X_train)
X_train = edu.preprocess(X_train)
X_train = ind.preprocess(X_train)
X_train = spt.preprocess(X_train)
X_train = env.preprocess(X_train)
X_train = non.preprocess(X_train)
X_train = nbr.preprocess(X_train)
X_train = trp.preprocess(X_train)
X_train = bus.trim_feats(X_train)
X_train = rel.trim_feats(X_train)
X_train = ofc.trim_feats(X_train)
X_train = X_train.drop(caf.caf_feats.index, 1)
X_train = X_train.drop(pop.pop_feats, 1)
X_test = test[hr.bld_feats + hr.caf_feats + hr.pop_feats + hr.ofc_feats + hr.rel_feats + \
	hr.bus_feats + hr.cul_feats + hr.edu_feats + hr.ind_feats + hr.spt_feats + hr.env_feats + \
	hr.non_feats + hr.nbr_feats + hr.trp_feats].copy()
X_test = bld.preprocess(X_test)
X_test = caf.preprocess(X_test)
X_test = pop.preprocess(X_test)
X_test = ofc.add_feats(X_test)
X_test = rel.add_feats(X_test)
X_test = bus.add_feats(X_test)
X_test = cul.preprocess(X_test)
X_test = edu.preprocess(X_test)
X_test = ind.preprocess(X_test)
X_test = spt.preprocess(X_test)
X_test = env.preprocess(X_test)
X_test = non.preprocess(X_test)
X_test = nbr.preprocess(X_test)
X_test = trp.preprocess(X_test)
X_test = bus.trim_feats(X_test)
X_test = rel.trim_feats(X_test)
X_test = ofc.trim_feats(X_test)
X_test = X_test.drop(caf.caf_feats.index, 1)
X_test = X_test.drop(pop.pop_feats, 1)
y_train = np.log(train['price_doc'])
y_train_raw = train['price_doc']

for df in [train, test]:
	df['build_year'] = df['build_year'].map(lambda x: 2018 - x if x < 1000 else x if x < 3000 else 2005)