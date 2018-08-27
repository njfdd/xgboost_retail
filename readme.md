## 各文件作用

```
data_init
│   purchase_init.py                预处理purchase表，得到某家店某天某件单品的平均单价、平均总额、平均折扣
│   statistics_feature_init.py      预处理purchaseitem表，得到某家店某件单品的一段时间内，销量的统计量，例如6天内销量均值
│   user_count_init.py    	        预处理purchase表，得到某家店某件单品，一天内的成单量，估计为客流数量
│   weather_hour_init.py    	    预处理weather_hour表，将按小时的天气拍平，转化为按天的某些时间段内的天气情况
data_union
│   origin_clean.py                 清洗原始特征数据，删除异常值
│   origin_union.py                 聚合原始特征数据
exporter
│   day_sale_exporter.py            销量预测结果的文字和图形输出
feature_engine
│   f_binning.py                    分箱，将长尾特征映射到少量离散值
│   f_date.py			            日历信息特征映射
│   f_weather.py                    天气信息特征映射
│   f_smoothing.py                  添加平滑曲线预测结果
global_sources
│   file_operation.py               通用文件读写处理
job
│   sk_gdbt.py                      sklearn的gdbt
│   xg_cv.py                        xgboost使用交叉验证求最佳参数
│   xg_multi_classifier.py          xgboost多分类
│   xg_regression.py                xgboost回归
lib
│   date_map.py                     映射
│   evaluation.py                   计算评价指标结果
│   goods_map.py                    映射
│   holt_winters.py                 三次平滑曲线库
│   woe_binning.py                  最优分箱库
regression
│   day_sale.py                     xgboost按天销量预测
│   day_sale_stock.py               xgboost按天销量+库存预测
│   day_sale_ugly.py                移动平均按天销量预测
│   day_stock.py                    xgboost按天销库存预测
test
│   input                           存放原始与中间文件
```

## 代码流程
1. 对原始数据进行预处理，生成以商铺编号、商品编号、日期为主键的数据表
2. 融合已有的库存数据、天气数据、日历数据、商品数据等
3. 进行数据映射，添加平滑曲线，不断更新特征表
4. 按天进行销量或库存预测

## 执行流程
1. 乱序执行data_init下各文件
2. 执行origin_union.py，生成原始特征表origin_full.csv
3. 执行origin_clean.py，生成特征表feature_full.csv
4. 乱序执行feature_engine下各文件，注意f_binning.py不需要执行
5. 执行regression下某个具体任务


## 特征名称
| 名称 | 描述 | 时间 |
| --- | ---: | ---: |
| result | 销量 | 明天 |
| rundate | 日期 | 明天 |
| storeid | 店铺编号 | |
| goodscode | 商品编号 | |
| saleqty | 销量 | 昨天 |
| inqty | 进货数量 | 昨天 |
| stockqty | 库存数量 | 昨天 |
| price | 单品平均价格 | 昨天 |
| total_amount | 订单平均总价 | 昨天 |
| total_discount | 订单平均折扣 | 昨天 |
| user_count | 店铺成单量 | 昨天 |
| week | 周几 | 明天 |
| holiday | 是否节假日 | 明天 |
| free_holiday | 是否放假 | 明天 |
| hightemp | 最高温度 | 明天 |
| lowtemp | 最低温度 | 明天 |
| descrip | 天气描述 | 明天 |
| windspeed | 风速 | 明天 |
| preci | 降雨量 | 明天 |
| preci_prob | 降雨概率 | 明天 |
| humi | 湿度 | 明天 |
| pressure | 压强 | 明天 |
| cloud | 云覆盖比例 | 明天 |
| morn_temp | 平均温度--早 | 明天 |
| morn_windspeed | 平均风速--早 | 明天 |
| morn_preci | 平均降雨强度--早 | 明天 |
| morn_humi | 平均湿度--早 | 明天 |
| noon_temp | 平均温度--中午 | 明天 |
| noon_windspeed | 平均风速--中午 | 明天 |
| noon_preci | 平均降水强度--中午 | 明天 |
| noon_humi | 平均湿度-中午 | 明天 |
| even_temp | 平均温度--晚 | 明天 |
| even_windspeed | 平均风速--晚 | 明天 |
| even_preci | 平均降水强度--晚 | 明天 |
| even_humi | 平均湿度--晚 | 明天 |
| max_3 | 过去3天最大销量值 | 昨天 |
| min_3 | 过去3天最小销量值 | 昨天 |
| var_3 | 过去3天销量方差 | 昨天 |
| std_3 | 过去3天销量标准差 | 昨天 |
| sum_3 | 过去3天销量总和 | 昨天 |
| max_7 | 过去7天最大销量值 | 昨天 |
| min_7 | 过去7天最小销量值 | 昨天 |
| var_7 | 过去7天销量方差 | 昨天 |
| std_7 | 过去7天销量标准差 | 昨天 |
| sum_7 | 过去7天销量总和 | 昨天 |
| max_15 | 过去15天最大销量值 | 昨天 |
| min_15 | 过去15天最小销量值 | 昨天 |
| var_15 | 过去15天销量方差 | 昨天 |
| std_15 | 过去15天销量标准差 | 昨天 |
| sum_15 | 过去15天销量总和 | 昨天 |
| max_60 | 过去60天最大销量值 | 昨天 |
| min_60 | 过去60天最小销量值 | 昨天 |
| var_60 | 过去60天销量方差 | 昨天 |
| std_60 | 过去60天销量标准差 | 昨天 |
| sum_60 | 过去60天销量总和 | 昨天 |
| smoothing1 | 一次平滑曲线预测值 | 昨天 |
| smoothing2 | 二次平滑曲线预测值 | 昨天 |
| smoothing3 | 三次平滑曲线预测值 | 昨天 |

##预测形式
一般店员在下午3点准备明天的进货，所以预测模型使用今天预测明天销量时，所使用的数据是历史至昨天的数据。
