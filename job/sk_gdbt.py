# coding=utf-8
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error

# 销量预测，预测一条数据
def predict(train_simple, train_label, test_simple, test_label):
    if len(train_simple) > 0 and len(test_simple) > 0:
        y_pred_result = predict_detail(train_simple, train_label, test_simple)
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

def MAPE(true, pred):
    diff = np.abs(np.array(true) - np.array(pred))
    return np.mean(diff / true)

def predict_detail(x_train, y_train, x_test):
    model = RandomForestRegressor(random_state=10, criterion='mae')
    model.fit(x_train, y_train)
    print(MAPE(y_train, model.predict(x_train)))
    y_pred = model.predict(x_test)
    # feature importance
    # plt.figure(0, figsize=(20, 7))
    # feat_imp = pd.Series(model.feature_importances_, index=x_train.columns).sort_values(ascending=False)
    # feat_imp.plot(kind='bar', title='Feature Importances', ax=plt.gca())
    # plt.savefig('../test/temp/importance.png')
    # plt.close('all')
    return y_pred[0]