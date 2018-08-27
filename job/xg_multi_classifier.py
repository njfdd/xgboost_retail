# coding=utf-8
from xgboost import XGBClassifier

# 销量上限预测，提供准确度，预测一条数据
def predict(train_simple, train_label, test_simple, test_label, accuracy=0.99):
    if len(train_simple) > 0 and len(test_simple) > 0:
        y_pred_result = predict_detail(train_simple, train_label, test_simple, accuracy)
        return {'y_test': test_label.values[0], 'y_pred': y_pred_result}
    return {}

def predict_detail(x_train, y_train, x_test, accuracy):
    model = XGBClassifier()
    # 训练
    model.fit(x_train, y_train)
    # feature importance
    # plt.figure(0, figsize=(20, 7))
    # feat_imp = pd.Series(model.feature_importances_, index=x_train.columns).sort_values(ascending=False)
    # feat_imp.plot(kind='bar', title='Feature Importances', ax=plt.gca())
    # plt.savefig('../test/temp/importance.png')
    # plt.close('all')

    y_pred = model.predict_proba(x_test)
    # print(y_pred)
    sum_proba = 0
    y_train_unique = sorted(y_train.unique())
    index = 0
    while index < len(y_train_unique) - 1:
        sum_proba += y_pred[0, index]
        if sum_proba > accuracy:
            break
        index += 1
    return y_train_unique[index] * 1.5