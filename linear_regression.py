import numpy as np
from numpy.linalg import inv
from preprocessing import normalize


def gradient(x, y, w, t=0.0):
    grad = np.zeros(x[0].T.shape)
    for xi, yi in zip(x, y):
        grad += (np.dot(w, xi) - yi) * xi.T / x.shape[0]
    return grad + w * 2.0 * t


def gradient_descent(x, y, t):
    rate = 0.5
    n, l = x.shape
    w = np.ones((1, l))
    while True:
        w_was = np.copy(w)
        w -= rate * gradient(x, y, w, t)
        if np.linalg.norm(w_was - w, 2) < 1e-9:
            break
    return w


def exact_solution(x, y):
    w = inv(np.dot(x.T, x))
    w = w.dot(x.T)
    w = w.dot(y)
    return w.T


class LinearRegression:
    def __init__(self, normalize=False, reg_score=0.0, method='gd'):
        self.normalize = normalize
        self.reg_score = reg_score
        self.method = method
        self.X = None
        self.Y = None
        self.weights = None

    def fit(self, x, y):
        shape = (x.shape[0], 1)
        self.X = x
        self.X = np.c_[np.ones(shape), x]
        self.Y = np.copy(y)
        self.weights = self.__solve__()
        return self.weights

    def __solve__(self):
        if self.normalize:
            normalize(self.X)
        if self.method == 'gd':
            return gradient_descent(self.X, self.Y, self.reg_score)
        if self.method == 'exact':
            return exact_solution(self.X, self.Y)
