import random
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances as EuDist2
from scipy import signal

from . import funs as Ifuns


def get_anchor(X, m, way="random"):
    if way == "kmeans":
        A = KMeans(m, init='random').fit(X).cluster_centers_
    elif way == "kmeans2":
        A = KMeans(m, init='random').fit(X).cluster_centers_
        D = EuDist2(A, X)
        ind = np.argmin(D, axis=1)
        A = X[ind, :]
    elif way == "k-means++":
        A = KMeans(m, init='k-means++').fit(X).cluster_centers_
    elif way == "k-means++2":
        A = KMeans(m, init='k-means++').fit(X).cluster_centers_
        D = EuDist2(A, X)
        A = np.argmin(D, axis=1)
    elif way == "random":
        ids = random.sample(range(X.shape[0]), m)
        A = X[ids, :]
    else:
        raise SystemExit('no such options in "get_anchor"')
    return A


def knn_f(X, knn, squared=True):
    D_full = EuDist2(X, X, squared=squared)
    np.fill_diagonal(D_full, -1)
    NN_full = np.argsort(D_full, axis=1)
    np.fill_diagonal(D_full, 0)

    NN = NN_full[:, :knn]
    NND = Ifuns.matrix_index_take(D_full, NN)
    return NN, NND


def kng(X, knn, way="gaussian", t="mean", self=0, isSym=True):
    """
    :param X: data matrix of n by d
    :param knn: the number of nearest neighbors
    :param way: one of ["gaussian", "t_free"]
        "t_free" denote the method proposed in :
            "The constrained laplacian rank algorithm for graph-based clustering"
        "gaussian" denote the heat kernel
    :param t: only needed by gaussian, the bandwidth parameter
    :param self: including self: weather xi is among the knn of xi
    :param isSym: True or False, isSym = True by default
    :return: A, a matrix (graph) of n by n
    """
    N, dim = X.shape

    # n x n graph
    D = EuDist2(X, X, squared=True)

    np.fill_diagonal(D, -1)
    NN_full = np.argsort(D, axis=1)
    np.fill_diagonal(D, 0)

    if self == 1:
        NN = NN_full[:, :knn]  # xi isn't among neighbors of xi
        NN_k = NN_full[:, knn]
    else:
        NN = NN_full[:, 1:(knn + 1)]  # xi isn't among neighbors of xi
        NN_k = NN_full[:, knn + 1]

    # A = np.zeros((N, N))
    # for i in range(N):
    #     id = NN_full[i, 1 : knn + 2]
    #     di = D[i, id]
    #     A[i, id] = (di[knn] - di) / (knn * di[knn] - np.sum(di[:knn]));

    #
    Val = get_similarity_by_dist(D=D, NN=NN, NN_k=NN_k, knn=knn, way=way, t=t)

    A = np.zeros((N, N))
    Ifuns.matrix_index_assign(A, NN, Val)

    if isSym:
        A = (A + A.T) / 2

    return A


def kng_anchor(X, Anchor: np.ndarray, knn=20, way="gaussian", t="mean", HSI=False, shape=None, alpha=0):
    """ see agci for more detail
    :param X: data matrix of n (a x b in HSI) by d
    :param Anchor: Anchor set, m by d
    :param knn: the number of nearest neighbors
    :param alpha:
    :param way: one of ["gaussian", "t_free"]
        "t_free" denote the method proposed in :
            "The constrained laplacian rank algorithm for graph-based clustering"
        "gaussian" denote the heat kernel
    :param t: only needed by gaussian, the bandwidth parameter
    :param HSI: compute similarity for HSI image
    :param shape: list, [a, b, c] image: a x b, c: channel
    :param alpha: parameter for HSI
    :return: A, a matrix (graph) of n by m
    """
    if shape is None:
        shape = list([1, 1, 1])
    N = X.shape[0]
    anchor_num = Anchor.shape[0]

    D = EuDist2(X, Anchor, squared=True)  # n x m
    if HSI:
        # MeanData
        conv = np.ones((3, 3))/9
        NData = X.reshape(shape)
        MeanData = np.zeros_like(NData)
        for i in range(shape[-1]):
            MeanData[:, :, i] = signal.convolve2d(NData[:, :, i], np.rot90(conv), mode='same')
        MeanData = MeanData.reshape(shape[0] * shape[1], shape[2])

        D += EuDist2(MeanData, Anchor, squared=True)*alpha  # n x m
    NN_full = np.argsort(D, axis=1)
    NN = NN_full[:, :knn]  # xi isn't among neighbors of xi
    NN_k = NN_full[:, knn]

    Val = get_similarity_by_dist(D=D, NN=NN, NN_k=NN_k, knn=knn, way=way, t=t)

    A = np.zeros((N, anchor_num))
    Ifuns.matrix_index_assign(A, NN, Val)
    return A


def get_similarity_by_dist(D, NN, NN_k, knn, way, t):
    """
    :param D: Distance matrix
    :param NN_k: k-th neighbor of each sample
    :param NN: k-nearest-neighbor of each sample
    :param knn: neighbors
    :param way: "gaussian" or "t_free"
    :param t: "mean" or "median" if way=="gaussian"
    :return: NN, val, val[i, j] denotes the similarity between xi and xj
    """
    eps = 2.2204e-16
    NND = Ifuns.matrix_index_take(D, NN)
    if way == "gaussian":
        if t == "mean":
            t = np.mean(D)   # Before March 2021, t = np.mean(NND), exp(-NND/t)
        elif t == "median":
            t = np.median(D)  # Before March 2021, t = np.median(NND), exp(-NND/t)
        Val = np.exp(-NND / (2 * t ** 2))
    elif way == "t_free":
        NND_k = Ifuns.matrix_index_take(D, NN_k.reshape(-1, 1))
        Val = NND_k - NND
        ind0 = np.where(Val[:, 0] == 0)[0]
        if len(ind0) > 0:
            Val[ind0, :] = 1/knn
        Val = Val / (np.sum(Val, axis=1).reshape(-1, 1))
    else:
        raise SystemExit('no such options in "kng_anchor"')

    return Val
