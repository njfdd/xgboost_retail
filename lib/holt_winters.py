import numpy as np

# triple exponential smoothing
def holt_winters_first_order_ewma(y, alpha):
    N = len(y)
    s = np.zeros((N,))
    b = np.zeros((N,))
    result = np.zeros((N,))
    s[0] = y[0]
    for i in range(1, N):
        s[i] = alpha * y[i - 1] + (1 - alpha) * (s[i - 1])
        result[i] = s[i]
    return result


def holt_winters_second_order_ewma(y, alpha, beta):
    N = len(y)
    s = np.zeros((N,))
    b = np.zeros((N,))
    result = np.zeros((N,))
    s[0] = y[0]
    for i in range(1, N):
        s[i] = alpha * y[i - 1] + (1 - alpha) * (s[i - 1] + b[i - 1])
        b[i] = beta * (s[i] - s[i - 1]) + (1 - beta) * b[i - 1]
        result[i] = s[i] + b[i]
    return result


def initial_trend(series, slen):
    sum = 0.0
    for i in range(slen):
        sum += float(series[i + slen] - series[i]) / slen
    return sum / slen


def initial_seasonal_components(series, slen):
    seasonals = {}
    season_averages = sum(series[0: slen]) / float(slen)
    for i in range(slen):
        seasonals[i] = series[i] - season_averages
    return seasonals

# gama mean 1 - cycle weight
def triple_exponential_smoothing(series, slen, alpha, beta, gamma):
    result = []
    seasonals = initial_seasonal_components(series, slen)
    for i in range(len(series)):
        if i == 0:  # initial values
            smooth = series[0]
            trend = initial_trend(series, slen)
            result.append(series[0])
            continue
        else:
            val = series[i - 1]
            last_smooth, smooth = smooth, alpha * (val - seasonals[i % slen]) + (1 - alpha) * (smooth + trend)
            trend = beta * (smooth - last_smooth) + (1 - beta) * trend
            seasonals[i % slen] = gamma * (val - smooth) + (1 - gamma) * seasonals[i % slen]
            result.append(smooth + trend + seasonals[i % slen])
    return result
