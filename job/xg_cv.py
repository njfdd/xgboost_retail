# coding=utf-8
from sklearn.model_selection import GridSearchCV
import xgboost as xgb


def get_best_paras(train_simple, train_label):
    if len(train_simple) > 3:
        cv_params = {
            'n_estimators': [100, 200, 500],
            'learning_rate': [0.1, 0.3, 0.5],
            'max_depth': [2, 3, 4],
            'min_child_weight': [1, 2, 3],
            'gamma': [0, 0.1, 0.3]
        }
        model = xgb.XGBRegressor()
        optimized_GBM = GridSearchCV(estimator=model, param_grid=cv_params, scoring='neg_mean_squared_error',
                                     cv=3, verbose=False, n_jobs=-1)
        optimized_GBM.fit(train_simple, train_label)
        evalute_result = optimized_GBM.best_params_
        # print('参数的最佳取值：{0}'.format(optimized_GBM.best_params_))
        # print('最佳模型得分:{0}'.format(optimized_GBM.best_score_))
        return evalute_result
    return {}