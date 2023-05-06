import os
import scipy.io as sio
import numpy as np
from alias_copyi_KSUMS import KSUMS, data_path
from alias_copyi_KSUMS.FeiPub import Funs, Gfuns, Mfuns

knn = 20

# load date
data = sio.loadmat(os.path.join(data_path, "Face95.mat"))
X = data["X"]
y_true = data["y_true"].astype(np.int32).reshape(-1)
c_true = len(np.unique(y_true))

NN, NND, t_graph = Gfuns.knn_f(X, knn, self_include=True)
max_d = np.max(NND)
NN_l, NND_l = Gfuns.symmetry_py(NN, NND, expand=False)

obj = KSUMS(NN_l, NND_l, max_d, c_true)
obj.opt()
y_pred = obj.y_pre


acc = Mfuns.accuracy(y_true=y_true, y_pred=y_pred)
print(acc)

#  paper: Face95, acc = 0.471
#  run:   Face95, acc = 0.476
