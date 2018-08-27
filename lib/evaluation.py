import numpy as np
import sys
import pandas as pd
import math

def mape(y_test, predict_list):
    i = 0
    sum_value = 0
    for real in y_test:
        if real > 0:
            predict = predict_list[i]
            v1 = float(abs(predict - real)) / float(real)
            sum_value += v1
        i = i + 1
    v2 = sum_value / len(predict_list)
    return v2

# Evaluation algorithm
def rmsp_avg_1(y_test, predict_list):
    i = 0
    sum_value = 0
    for real in y_test:
        predict = predict_list[i]
        v1 = float(abs(predict - real)) / float(real + 1)
        sum_value += v1
        i = i + 1
    v2 = sum_value / len(predict_list)
    return v2


def rmsp_avg_2(y_test, predict_list):
    i = 0
    sum_value = 0
    for real in y_test:
        predict = predict_list[i]
        if real == 0.0:
            real = 1.0
        v1 = float(abs(predict - real)) / float(real)
        sum_value += v1
        i = i + 1
    v2 = sum_value / len(predict_list)
    return v2


def rmsp_avg_3(y_test, predict_list):
    i = 0
    sum_value = 0
    for real in y_test:
        predict = predict_list[i]
        v1 = float(abs(predict - real)) / float(predict + 1)
        sum_value += v1
        i = i + 1
    v2 = sum_value / len(predict_list)
    return v2


def rmsp_avg_4(y_test, predict_list):
    i = 0
    sum_value = 0
    for real in y_test:
        predict = predict_list[i]
        if predict == 0.0:
            predict = 1.0
        v1 = float(abs(predict - real)) / float(predict + 1)
        sum_value += v1
        i = i + 1
    v2 = sum_value / len(predict_list)
    return v2


def rmsp_avg_5(y_test, predict_list):
    i = 0
    sum_test = 0
    sum_pred = 0
    for real in y_test:
        predict = predict_list[i]
        sum_test += float(abs(predict - real))
        sum_pred += float(predict + 1)
        i = i + 1
    v2 = sum_test / sum_pred
    return v2

def rmsp_avg_5_2(y_test, predict_list):
    i = 0
    sum_test = 0
    sum_real = 0
    for real in y_test:
        predict = predict_list[i]
        sum_test += float(abs(predict - real))
        sum_real += float(real + 1)
        i = i + 1
    v2 = sum_test / sum_real
    return v2


def rmsp_avg_6(y_test, predict_list):
    i = 0
    sum_value = 0
    for real in y_test:
        predict = predict_list[i]
        v1 = float(abs(predict - real)) / float(max(predict, real) + 1)
        sum_value += v1
        i = i + 1
    v2 = sum_value / len(predict_list)
    return v2


def rmsp_avg_7(y_test, predict_list):
    i = 0
    sum_value = 0
    for real in y_test:
        predict = predict_list[i]
        v1 = float(abs(predict - real)) / float(real + 1)
        if v1 > 1.0:
            v1 = 1.0
        sum_value += v1
        i = i + 1
    v2 = sum_value / len(predict_list)
    return v2


def rmsp_avg_8(y_test, predict_list):
    i = 0
    sum_value = 0
    for real in y_test:
        predict = predict_list[i]
        v1 = float(abs(predict - real)) / float(predict + 1)
        if v1 > 1.0:
            v1 = 1.0
        sum_value += v1
        i = i + 1
    v2 = sum_value / len(predict_list)
    return v2


def rmsp_avg_9(y_test, predict_list):
    i = 0
    sum_value = 0
    for real in y_test:
        predict = predict_list[i]
        v1 = float(abs(predict - real)) / float(real + 1)
        if v1 > 1.0:
            sum_value += 1
        i = i + 1
    return sum_value


def rmsp_avg_10(y_test, predict_list):
    i = 0
    sum_value = 0
    for real in y_test:
        predict = predict_list[i]
        v1 = float(abs(predict - real)) / float(predict + 1)
        if v1 > 1.0:
            sum_value += 1
        i = i + 1
    return sum_value


def rmsp_avg_11(y_test, predict_list):
    i = 0
    sum_value = 0
    for real in y_test:
        if real > 0.0:
            sum_value += 1
        i = i + 1
    return sum_value

def rmsp_avg_12(y_test, predict_list):
    i = 0
    sum_value = 0
    for real in y_test:
        predict = predict_list[i]
        v1 = float(abs(predict - real)) / float(max(predict + real, 1))
        sum_value += v1
        i = i + 1
    v2 = sum_value / len(predict_list)
    return v2

def rmsp_avg_13(y_test, predict_list):
    i = 0
    sum_real = 0
    sum_pred = 0
    for real in y_test:
        predict = predict_list[i]
        sum_real += real + 1
        sum_pred += predict + 1
        i = i + 1
    v2 = sum_pred / sum_real
    return v2


def accuracy_cov(y_test, predict_list):
    i = 0
    result = []
    for real in y_test:
        predict = predict_list[i]
        v1 = float(abs(real - predict)) / float(real)
        result.append(v1)
        i = i + 1
    return np.var(result)

def get_volatility(y_test):
    pred = y_test[0]
    sum_real = 0
    sum_gap = 0
    for real in y_test:
        sum_gap += abs(real - pred)
        sum_real += real
        pred = real
    return sum_gap / sum_real

def corr(x,y):
    if len(x) != len(y):
        sys.stderr.write('err: input length not equal\n')
        sys.exit(1)
    df = pd.DataFrame(columns=['x','y'])
    df['x'] = x
    df['y'] = y
    n = len(x)
    mean = df.mean()
    x_mean = mean['x']
    y_mean = mean['y']
    covariance = 0
    x_std = 0
    y_std = 0
    for i in range(0,n):
        covariance += (x[i]-x_mean) * (y[i]-y_mean)
        x_std += math.pow((x[i] - x_mean),2)
        y_std += math.pow((y[i] - y_mean),2)
    return covariance / math.sqrt(x_std*y_std)