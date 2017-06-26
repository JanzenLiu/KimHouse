import sys
sys.path.append('../')
from Common import *

# special log_price values
# 14.508658    757
# 13.815511    747
# 14.914123    332

# special price values
# 2000000     757
# 1000000     747
# 3000000     332

df0 = train[(train['price_doc'] != 990000) *
	(train['price_doc'] != 1000000) * 
	(train['price_doc'] != 2000000) * 
	(train['price_doc'] != 3000000)]

df1 = train[(train['price_doc'] != 990000) +
	(train['price_doc'] == 1000000) + 
	(train['price_doc'] == 2000000) + 
	(train['price_doc'] == 3000000)]