'''This module runs a 5-Fold CV for all the algorithms (default parameters) on
the movielens datasets, and reports average RMSE, MAE, and total computation
time.  It is used for making tables in the README.md file'''

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import time
import datetime
import random
import timeit

import numpy as np
import six
from tabulate import tabulate

import sys
import os
import importlib
module = ('baseline.py')

from surprise import Dataset, dataset, AlgoBase
from surprise.model_selection import cross_validate
from surprise.model_selection import KFold
from surprise import NormalPredictor
from surprise import BaselineOnly
from surprise import KNNBasic
from surprise import KNNWithMeans
from surprise import KNNBaseline
from surprise import SVD
from surprise import SVDpp
from surprise import NMF
from surprise import SlopeOne
from surprise import CoClustering


from baselines import GlobalMean, MeanofMeans
# from pyspark.ml.recommendation import ALS
# from baselines import all

baseline1 = {'method': 'sgd'}
BaselineSGD = BaselineOnly(bsl_options=baseline1)

baseline2 = {'method': 'als'}
ALS = BaselineOnly()

# The algorithms to cross-validate
classes = (GlobalMean, MeanofMeans, BaselineOnly, SVD, NMF, SlopeOne, KNNBasic, KNNWithMeans, KNNBaseline,
           CoClustering, NormalPredictor)

short_class = (MeanofMeans, BaselineOnly)
# took out SVDpp for time

# ugly dict to map algo names and datasets to their markdown links in the table
stable = 'http://surprise.readthedocs.io/en/stable/'
LINK = {'SVD': '[{}]({})'.format('SVD',
                                 stable +
                                 'matrix_factorization.html#surprise.prediction_algorithms.matrix_factorization.SVD'),
        # 'SVDpp': '[{}]({})'.format('SVD++',
        #                            stable +
        #                            'matrix_factorization.html#surprise.prediction_algorithms.matrix_factorization.SVDpp'),
        'NMF': '[{}]({})'.format('NMF',
                                 stable +
                                 'matrix_factorization.html#surprise.prediction_algorithms.matrix_factorization.NMF'),
        'SlopeOne': '[{}]({})'.format('Slope One',
                                      stable +
                                      'slope_one.html#surprise.prediction_algorithms.slope_one.SlopeOne'),
        'KNNBasic': '[{}]({})'.format('k-NN',
                                      stable +
                                      'knn_inspired.html#surprise.prediction_algorithms.knns.KNNBasic'),
        'KNNWithMeans': '[{}]({})'.format('Centered k-NN',
                                          stable +
                                          'knn_inspired.html#surprise.prediction_algorithms.knns.KNNWithMeans'),
        'KNNBaseline': '[{}]({})'.format('k-NN Baseline',
                                         stable +
                                         'knn_inspired.html#surprise.prediction_algorithms.knns.KNNBaseline'),
        'CoClustering': '[{}]({})'.format('Co-Clustering',
                                          stable +
                                          'co_clustering.html#surprise.prediction_algorithms.co_clustering.CoClustering'),
        'BaselineOnly': '[{}]({})'.format('Baseline',
                                          stable +
                                          'basic_algorithms.html#surprise.prediction_algorithms.baseline_only.BaselineOnly'),
        'NormalPredictor': '[{}]({})'.format('Random',
                                             stable +
                                             'basic_algorithms.html#surprise.prediction_algorithms.random_pred.NormalPredictor'),
        'ml-100k': '[{}]({})'.format('Movielens 100k',
                                     'http://grouplens.org/datasets/movielens/100k'),
        'ml-1m': '[{}]({})'.format('Movielens 1M',
                                   'http://grouplens.org/datasets/movielens/1m'),
        'ml-latest': '[{}]({})'.format('Movielens 1M',
                                   'https://grouplens.org/datasets/movielens/latest/')
        }


# set RNG
np.random.seed(0)
random.seed(0)

dataset = 'ml-latest'
data = Dataset.load_builtin(dataset)
kf = KFold(random_state=0)  # folds will be the same for all algorithms.
start_timer = timeit.default_timer()
table = []
for klass in short_class:
    print(f'{klass}')
    start = time.time()
    if klass == GlobalMean:
        data = Dataset.load_builtin('ml-100k')
        print("\nGlobal Mean...")
        algo = GlobalMean()
        cross_validate(algo, data, verbose=True)
    elif klass == MeanofMeans:
        print("\nMeanOfMeans...")
        algo = MeanofMeans()
        cross_validate(algo, data, verbose=True)
    else:
        out = cross_validate(klass(), data, ['rmse', 'mae'], kf)
        cv_time = str(datetime.timedelta(seconds=int(time.time() - start)))
        link = LINK[klass.__name__]
        mean_rmse = '{:.3f}'.format(np.mean(out['test_rmse']))
        mean_mae = '{:.3f}'.format(np.mean(out['test_mae']))

        new_line = [mean_rmse, mean_mae, cv_time]
        print(tabulate([new_line], tablefmt="pipe"))  # print current algo perf
        table.append(new_line)

        header = [LINK[dataset],
                'RMSE',
                'MAE',
                'Time'
          ]
print(tabulate(table, tablefmt="pipe"))
stop_timer = timeit.default_timer()
print(f"Time to complete ALS: {stop_timer-start_timer:.2f} seconds")