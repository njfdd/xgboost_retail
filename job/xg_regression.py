# coding=utf-8
from xgboost import XGBRegressor
import xgboost as xgb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 销量预测，预测一条数据
def predict(paras, train_simple, train_label, test_simple, test_label):
    if len(train_simple) > 0 and len(test_simple) > 0:
        y_pred_result = predict_detail(paras, train_simple, train_label, test_simple)
        return {'y_test': test_label.values[0], 'y_pred': y_pred_result}
    return {}

def evalmape(preds,dtrain):
    labels = dtrain.get_label()
    error = sum(abs(preds-labels)*1.0/(labels))*1.0/len(labels)
    return 'error',error

def logregobj(preds, dtrain):
    labels = dtrain.get_label()
    preds = 1.0 / (1.0 + np.exp(-preds))
    grad = preds - labels
    hess = preds * (1.0 - preds)
    return grad, hess

def huber_approx_obj(preds, dtrain):
    d = dtrain.get_label() - preds #remove .get_labels() for sklearn
    h = 1  #h is delta
    scale = 1 + (d / h) ** 2
    scale_sqrt = np.sqrt(scale)
    grad = d / scale_sqrt
    hess = 1 / scale / scale_sqrt
    return grad, hess

def predict_detail(paras, x_train, y_train, x_test):
    # xgtrain = xgb.DMatrix(x_train.values, y_train.values)
    # xgtest = xgb.DMatrix(x_test.values)
    # model = xgb.train(paras, dtrain=xgtrain, verbose_eval=0)
    # y_pred = model.predict(xgtest)

    paras['reg_alpha'] = 0.1
    model = XGBRegressor(**paras)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    # feature importance
    # plt.figure(0, figsize=(20, 10))
    # feat_imp = pd.Series(model.feature_importances_, index=x_train.columns).sort_values(ascending=False)
    # feat_imp.plot(kind='bar', title='Feature Importances', ax=plt.gca())
    # plt.savefig('../sources/importance.png')
    # plt.close('all')
    # exit(1)
    return y_pred[0]