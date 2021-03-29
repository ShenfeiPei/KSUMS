import numpy as np


def twospirals(N=2000, degrees=570, start=90, noise=0.2):
    X = np.zeros((N, 2), dtype=np.float64)
    deg2rad = np.pi/180
    start = start * deg2rad

    N1 = int(np.floor(N/2))
    N2 = N - N1

    n = start + np.sqrt(np.random.rand(N1)) * degrees * deg2rad
    X[:N1, 0] = -np.cos(n) * n + np.random.rand(N1) * noise
    X[:N1, 1] =  np.sin(n) * n + np.random.rand(N1) * noise

    n = start + np.sqrt(np.random.rand(N2)) * degrees * deg2rad
    X[N1:, 0] =  np.cos(n) * n + np.random.rand(N2) * noise
    X[N1:, 1] = -np.sin(n) * n + np.random.rand(N2) * noise

    y = np.ones(N, dtype=np.int32)
    y[:N1] = 0
    return X, y