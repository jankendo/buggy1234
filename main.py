import NePo
import newsn
from statistics import mean
from matplotlib import pyplot as plt


l = (newsn.get_comment())
pn_list = []
for a in l:
    print(a)
    text = NePo.get_pnmean(NePo.add_pnvalue(NePo.get_diclist(a)))
    print(text)
    pn_list.append(text)

pnmean = mean(pn_list)
plt.plot(pn_list)
plt.show()
print("Ave :")
print(pnmean)