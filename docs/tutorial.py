#!/usr/bin/python3
import op_tools
from random import seed
from random import normalvariate
from random import random

seed(9999)

coord_grid = [[x + normalvariate(0, 0.3),
               y + normalvariate(0, 0.3),
               0] for x in range(10) for y in range(10)]
coord_random = [[10*random(),
                 10*random(),
                 0] for x in range(10) for y in range(10)]

op_settings = {
    'neighbor': [6],
    'ave_times': 1,
    'oi_oj': [0], 'o_factor': [0],
    'b_in_Q': 1, 'l_in_Q': [2, 4, 8], 'p_in_Q': [0],
    'analysis_type': ['Q']}
direct = []
thread_num = 3
sim_box = [10, 10, 10]
order_parameter_grid = op_tools.op_analyze(
    coord_grid, direct, sim_box, op_settings, thread_num)
order_parameter_random = op_tools.op_analyze(
    coord_random, direct, sim_box, op_settings, thread_num)

order_parameter_grid['label'] = ['grid' for i in range(100)]
order_parameter_random['label'] = ['rand' for i in range(100)]
import pandas as pd
df_grid = pd.DataFrame(order_parameter_grid)
df_random = pd.DataFrame(order_parameter_random)
df = pd.concat([df_grid, df_random])

# split data
train_x = df.drop('label', axis=1)
train_y = df['label']

from sklearn.model_selection import train_test_split
(train_x2, test_x2, train_y2, test_y2) = train_test_split(
    train_x, train_y, test_size=0.2, random_state=666)

from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100)

# train and predict
clf_fit = clf.fit(train_x2, train_y2)
pred = clf_fit.predict(test_x2)

# show accuracy
from sklearn.metrics import accuracy_score
acc = accuracy_score(pred, test_y2)
print(acc, pred, test_y2)


params = {
    'n_estimators': [100],
    'max_depth': [1, 3, 5, None],
    'criterion': ['gini', 'entropy'],
    'max_features': [1, 3, 5, 'auto', None],
}
from sklearn.model_selection import GridSearchCV
clf_search = GridSearchCV(RandomForestClassifier(
    n_jobs=2), params, scoring='accuracy', cv=5)
clf_search.fit(train_x2, train_y2)

print('Best parameters: {}'.format(clf_search.best_params_))
print('Best score: {:.3f}'.format(clf_search.best_score_))
# Best parameters: {'criterion': 'entropy', 'max_depth': 3, 'max_features': 3, 'n_estimators': 100}
# Best score: 0.986
