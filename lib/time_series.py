import numpy as np


def time_series_max(y, gap):
    N = len(y)
    result = np.zeros((N,))
    result[0:gap] = y[0:gap]
    for i in range(gap, N):
        result[i] = max(y[i - gap:i])
    return result

def time_series_min(y, gap):
    N = len(y)
    result = np.zeros((N,))
    result[0:gap] = y[0:gap]
    for i in range(gap, N):
        result[i] = min(y[i - gap:i])
    return result

def time_series_var(y, gap):
    N = len(y)
    result = np.zeros((N,))
    result[0:gap] = y[0:gap]
    for i in range(gap, N):
        result[i] = np.var(y[i - gap:i])
    return result

def time_series_std(y, gap):
    N = len(y)
    result = np.zeros((N,))
    result[0:gap] = y[0:gap]
    for i in range(gap, N):
        result[i] = np.std(y[i - gap:i])
    return result

def time_series_sum(y, gap):
    N = len(y)
    result = np.zeros((N,))
    result[0:gap] = y[0:gap]
    for i in range(gap, N):
        result[i] = sum(y[i - gap:i])
    return result