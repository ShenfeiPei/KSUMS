import os
import scipy.io as sio
import numpy as np
from alias_copyi_KSUMS.KSUMS import KSUMS
from alias_copyi_KSUMS.FeiPub import Funs, Gfuns, Mfuns

knn = 20

# load date
file_path = os.path.dirname(__file__)
data = sio.loadmat(os.path.join(file_path, "data/Mpeg7_20200916.mat"))
X = data["X"]
y_true = data["Y"].astype(np.int32).reshape(-1)
c_true = len(np.unique(y_true))

NN, NND, t_graph = Gfuns.knn_f(X, knn, self_include=True)
max_d = np.max(NND)
NN_l, NND_l = Gfuns.symmetry_py(NN, NND, expand=False)

obj = KSUMS(NN_l, NND_l, max_d, c_true)
obj.opt()
y_pred = obj.y_pre


acc = Mfuns.accuracy(y_true=y_true, y_pred=y_pred)
print(acc)

#  paper: Mpeg7, acc = 0.554
#  run:   Mpeg7, acc = 0.555
