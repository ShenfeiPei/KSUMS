import os
import time
import random
import numpy as np
import pandas as pd
import scipy
import scipy.io as sio
from scipy import stats
from scipy import sparse
from sklearn.metrics.pairwise import euclidean_distances as EuDist2
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from joblib import Parallel, delayed
from multiprocessing import Pool
from functools import partial

import matplotlib.pyplot as plt
import matplotlib.transforms as mt


def load_Agg():
    this_directory = os.path.dirname(__file__)
    data_path = os.path.join(this_directory, "dataset/")
    name_full = os.path.join(data_path + "Agg.mat")
    X, y_true, N, dim, c_true = load_mat(name_full)
    return X, y_true, N, dim, c_true


def load_USPS():
    this_directory = os.path.dirname(__file__)
    data_path = os.path.join(this_directory, "dataset/")
    name_full = os.path.join(data_path + "USPS.mat")
    X, y_true, N, dim, c_true = load_mat(name_full)
    return X, y_true, N, dim, c_true


def load_mat(path, to_dense=True):
    data = sio.loadmat(path)
    X = data["X"]
    if "y_true" in data.keys():
        y_true = data["y_true"].astype(np.int32).reshape(-1)
    elif "Y" in data.keys():
        y_true = data["Y"].astype(np.int32).reshape(-1)
    else:
        assert 1==0

    if sparse.isspmatrix(X) and to_dense:
        X = X.toarray()

    N, dim, c_true = X.shape[0], X.shape[1], len(np.unique(y_true))
    return X, y_true, N, dim, c_true


def save_mat(name_full, xy):
    sio.savemat(name_full, xy)


def matrix_index_take(X, ind_M):
    """
    :param X: ndarray
    :param ind_M: ndarray
    :return: X[ind_M] copied
    """
    assert np.all(ind_M >= 0)

    n, k = ind_M.shape
    row = np.repeat(np.array(range(n), dtype=np.int32), k)
    col = ind_M.reshape(-1)
    ret = X[row, col].reshape((n, k))
    return ret


def matrix_index_assign(X, ind_M, Val):
    n, k = ind_M.shape
    row = np.repeat(np.array(range(n), dtype=np.int32), k)
    col = ind_M.reshape(-1)
    if isinstance(Val, (float, int)):
        X[row, col] = Val
    else:
        X[row, col] = Val.reshape(-1)


def EProjSimplex_new(v, k=1):
    v = v.reshape(-1)
    # min  || x- v ||^2
    # s.t. x>=0, sum(x)=k
    ft = 1
    n = len(v)
    v0 = v-np.mean(v) + k/n
    vmin = np.min(v0)

    if vmin < 0:
        f = 1
        lambda_m = 0
        while np.abs(f) > 1e-10:
            v1 = v0 - lambda_m
            posidx = v1 > 0
            npos = np.sum(posidx)
            g = -npos
            f = np.sum(v1[posidx]) - k
            lambda_m -= f/g
            ft += 1
            if ft > 100:
                break
        x = np.maximum(v1, 0)
    else:
        x = v0

    return x, ft


def EProjSimplexdiag(d, u):
    #  d = d.astype(np.float64)
    #  u = u.astype(np.float64)
    # min  1/2*x'*U*x - x'*d
    # s.t. x>=0, sum(x) = 1
    lam = np.min(u-d)
    #  print(lam)
    f = 1
    count = 1
    while np.abs(f) > 1e-8:
        v1 = (lam + d)/u
        posidx = v1 > 0
        #  print(v1)
        g = np.sum(1/u[posidx])
        f = np.sum(v1[posidx]) - 1
        #  print(f)
        lam -= f/g

        if count > 1000:
            break
        count += 1
    v1 = (lam+d)/u
    x = np.maximum(v1, 0)
    return x, f


def eig1(A, c, isMax=True, isSym=True):
    if isinstance(A, sparse.spmatrix):
        A = A.toarray()

    if isSym:
        A = np.maximum(A, A.T)

    if isSym:
        d, v = np.linalg.eigh(A)
    else:
        d, v = np.linalg.eig(A)

    if isMax:
        idx = np.argsort(-d)
    else:
        idx = np.argsort(d)

    idx1 = idx[:c]
    eigval = d[idx1]
    eigvec = v[:, idx1]

    eigval_full = d[idx]

    return eigvec, eigval, eigval_full


def kmeans(X, c, rep, init="random", mini_batch=False):
    '''
    :param X: 2D-array with size of N x dim
    :param c: the number of clusters to construct
    :param rep: the number of runs
    :param init: the way of initialization: random (default), k-means++
    :param mini_batch: mini_batch kmeans: True, False (default)
    :param par: parallel: True (default), False
    :param n_cpu: the number of cores used if par==True, n_cpu = 6, by default.
    :return: Y, 2D-array with size of rep x N, each row is a assignment
    '''

    Y = np.zeros((rep, X.shape[0]), dtype=np.int32)
    if mini_batch:
        for i in range(rep):
            Y[i, :] = MiniBatchKMeans(n_clusters=c, n_init=1, init=init).fit(X).predict(X)
    else:
        for i in range(rep):
            Y[i, :] = KMeans(n_clusters=c, n_init=1, init=init, algorithm="full").fit(X).labels_
    return Y


def relabel(y, offset=0):
    y_df = pd.DataFrame(data=y, columns=["label"])
    ind_dict = y_df.groupby("label").indices

    for yi, ind in ind_dict.items():
        y[ind] = offset
        offset += 1


def normalize_fea(fea, row):
    '''
    if row == 1, normalize each row of fea to have unit norm;
    if row == 0, normalize each column of fea to have unit norm;
    '''

    if 'row' not in locals():
        row = 1

    if row == 1:
        feaNorm = np.maximum(1e-14, np.sum(fea ** 2, 1).reshape(-1, 1))
        fea = fea / np.sqrt(feaNorm)
    else:
        feaNorm = np.maximum(1e-14, np.sum(fea ** 2, 0))
        fea = fea / np.sqrt(feaNorm)

    return fea


def plot_bar(Y, labels, fname, barWidth=0.3, ra=0.5, addy=10):
    plt.figure(figsize=(6.4, 4.8))

    d_external = (1-2*barWidth)/(1+ra)
    d_internal = ra*d_external

    # Set position of bar on X axis
    X = np.zeros_like(Y)
    x_base = np.arange(Y.shape[0])
    X[:, 0] = x_base - 0.5*d_internal - 0.5*barWidth
    X[:, 1] = x_base + 0.5*d_internal + 0.5*barWidth

    # Make the plot
    plt.bar(X[:, 0], Y[:, 0], color=[0.99, 0.5, 0.05], width=barWidth,
            edgecolor='white', label='Random')
    plt.bar(X[:, 1], Y[:, 1], color=[0.137, 0.533, 0.8], width=barWidth,
            edgecolor='white', label=r'$k$-means')

    for g in range(Y.shape[1]):
        for i in range(Y.shape[0]):
            plt.text(X[i, g], Y[i, g], str(Y[i, g]), rotation=0, horizontalalignment='center')

    plt.xticks(x_base, labels=labels)

    plt.ylim(np.minimum(np.min(Y), 0), np.max(Y) + addy)
    plt.legend(loc='upper left')
    plt.yticks([])
    plt.subplots_adjust(top=0.98, bottom=0.06, right=0.98, left=0.02, hspace=0, wspace=0)
    plt.margins(0.05, 0.05)

    plt.savefig(fname=fname, format="pdf")
    # plt.gca().xaxis.set_major_locator(plt.NullLocator())
    # plt.gca().yaxis.set_major_locator(plt.NullLocator())
    # plt.savefig("/home/pei/Hm.C.pdf", dpi=300, bbox_inches=mt.Bbox([[-0.1, -0.1], [6.5, 4.9]]))
    plt.show()


def etaFunction(t, etaBase, rho, r):
    if t <= r:
        eta = etaBase * (t/r)**rho
    else:
        eta = etaBase

    return eta


def initialY(init, N, c_true, rep, X=None):
    if isinstance(init, np.ndarray):
        Y = init
    elif isinstance(init, str):
        if init == "random":
            eye_c = np.eye(c_true)
            Y = np.zeros((rep, N), dtype=np.int32)
            for i in range(rep):
                y1 = np.arange(c_true)
                np.random.shuffle(y1)
                y2 = np.random.randint(0, c_true, N-c_true)
                Y[i, :] = np.concatenate((y1, y2), axis=0)
                
        elif init == "kmeans":
            Y = kmeans(X=X, c=c_true, rep=rep, init="random")
        elif init == "k-means++":
            Y = kmeans(X=X, c=c_true, rep=rep, init="k-means++")
        else:
            raise SystemExit('no such options in "initialY"')
    else:
        raise SystemExit('no such options in "initialY"')

    assert Y.shape[1] == N
    assert Y.shape[0] == rep
    return Y


def data_description(data_path, data_name, version, url):
    X, y_true, N, dim, c_true = load_mat(
            "{}{}_{}.mat".format(data_path, data_name, version))

    # title and content
    T1 = "data_name"
    T2 = "# Samples"
    T3 = "# Features"
    T4 = "# Subjects"

    C1 = data_name
    C2 = str(X.shape[0])
    C3 = str(X.shape[1])
    C4 = str(c_true)

    n1 = max(len(T1), len(C1))
    n2 = max(len(T2), len(C2))
    n3 = max(len(T3), len(C3))
    n4 = max(len(T4), len(C4))

    y_df = pd.DataFrame(data=y_true, columns=["label"])
    ind_L = y_df.groupby("label").size()

    show_n = 5

    with open("{}{}_{}.txt".format(data_path, data_name, version), "a") as f:

        # version
        f.write("version = {}\n\n".format(version))

        # table
        f.write("{}  {}  {}  {}\n".format(
            T1.rjust(n1), T2.rjust(n2), T3.rjust(n3), T4.rjust(n4)))
        f.write("{}  {}  {}  {}\n\n".format(
            C1.rjust(n1), C2.rjust(n2), C3.rjust(n3), C4.rjust(n4)))

        # url
        f.write("url = {}\n\n".format(url))
        f.write("=================================\n")

        # content
        f.write("X[:, :2], {}, {}, {}\n".format(
            str(type(X))[8:-2], X.shape, str(type(X[0, 0]))[8:-2]))
        if isinstance(X, sparse.spmatrix):
            f.write("{}\n".format(X[:show_n, :2].toarray()))
        else:
            f.write("{}\n".format(X[:show_n, :2]))
        f.write("...\n\n")

        f.write("y_true, {}, {}, {}\n".format(
            str(type(y_true))[8:-2], y_true.shape, str(type(y_true[0]))[8:-2]))
        f.write("{}".format(y_true[:show_n]))
        f.write("...\n\n")

        f.write("distribution\n")
        f.write(ind_L[:50].to_string())
        f.write("\n\n")


def WHH(W, c, beta=0.5, ITER=100):
    val, vec = np.linalg.eigh(W)
    H = vec[:, -c:]
    #  H = sparse.linalg.eigsh(W, which='LA', k=c)[1]
    #  print(np.mean(H))
    H = np.maximum(W @ H, 0.00001)

    obj = np.zeros(ITER)
    obj[0] = np.linalg.norm(W - H@H.T, ord="fro")

    for i in range(1, ITER):
        H_old = H.copy()

        WH = W@H
        HHH = H@(H.T@H)
        H = H*(1 - beta + beta*WH/HHH)

        obj[i] = np.linalg.norm(W - H@H.T, ord="fro")

        if np.abs(obj[i] - obj[i-1])/obj[i] < 1e-6:
            break

    return H, obj


#  def WHH2(W, lam, P, c, beta=0.5, ITER=100):
#      W = sparse.csr_matrix(W)
#      H = sparse.linalg.eigsh(W, which='LA', k=c)[1]
#      H = np.maximum(W @ H, 0.00001)
#
#      obj = np.zeros(ITER)
#      obj[0] = np.linalg.norm(W + lam*P@P.T - H@H.T, ord="fro")
#
#      for i in range(1, ITER):
#
#          WH = W@H + lam*P@(P.T@H)
#          HHH = H@(H.T@H)
#          H = H*(1 - beta + beta*WH/HHH)
#
#          obj[i] = np.linalg.norm(W + lam*P@P.T - H@H.T, ord="fro")
#
#          if np.abs(obj[i] - obj[i-1])/obj[i] < 1e-6:
#              break
#
#      return H, obj

def norm_W(A):
    d = np.sum(A, 1)
    d[d == 0] = 1e-6
    d_inv = 1 / np.sqrt(d)
    tmp = A * np.outer(d_inv, d_inv)
    A2 = np.maximum(tmp, tmp.T)
    return A2


def rand_ring(r, N, tur, cx=0, cy=0, s=0, e=2 * np.pi, dis="gaussian"):
    """
    dis=["uniform", "gaussian"]
    """
    theta = np.linspace(s, e, N)
    x = np.vstack((r * np.cos(theta), r * np.sin(theta))).T
    x = x + turdata(N, tur, d=2, dis=dis)

    x[:, 0] += cx
    x[:, 1] += cy

    return x


def turdata(N, tur, d=2, dis="gaussian"):
    """
    dis=["uniform", "gaussian"]
    """

    if dis == "gaussian":
        mu = np.repeat(0, d)
        sig = np.eye(d) * tur
        x = np.random.multivariate_normal(mu, sig, N)
    elif dis == "uniform":
        x = np.random.uniform(-tur/2, tur/2, (N, 2))
    return x

