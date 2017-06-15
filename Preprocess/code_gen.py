from header import *

with open('single_feat2.py','a') as f:
	for col in combine.columns:
		str = ""
		str += "plt.figure(figsize=(12,8))\n"
		str += format("sns.countplot(x='%s', data=combine)\n" % col)
		str += "plt.show()\n\n"
		# print(str)
		f.write(str)