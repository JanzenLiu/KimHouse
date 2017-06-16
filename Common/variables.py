import pandas as pd

# TODO(Janzen): Fix load data file problem while calling in other directory

train = pd.read_csv('../Data/train.csv')
test = pd.read_csv('../Data/test.csv')
price = train['price_doc']
macro = pd.read_csv('../Data/macro.csv')
combine = pd.concat([train.drop(['price_doc'], 1), test], ignore_index=True).drop(['id'], 1)
