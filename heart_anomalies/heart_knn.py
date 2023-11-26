# Followed the algorithm explained here https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/

import copy
from random import randrange, seed
import pandas as pd
import numpy as np


def distance(row_a, row_b):
    distance = 0.0
    for i in range(len(row_a)):
        distance += (row_a[i] - row_b.iloc[i])**2
    return np.sqrt(distance)


def get_k_neighbors(training, new_row, k):
    '''
    Finds k nearest neighbors for new instance
    :param training: existing training data
    :param new_row: new row of data 
    :param k: number of neighbors to return
    '''
    distances = []
    neighbors = []

    # calculate distances for new instance
    for train_row in training:
        dist = distance(new_row[1:], train_row[1:])
        distances.append((train_row, dist))

        # sort and find nearest k neighbors
    distances.sort(key=lambda tup: tup[1])
    for i in range(k):
        # get the classification for the neighbor only
        neighbors.append(distances[i][0][0])
    return neighbors


def knn_prediction(train, test_row, k):
    neighbors = get_k_neighbors(train, test_row, k)
    return max(set(neighbors), key=neighbors.count)


def knn(train, test, k):
    predictions = []
    for row in test:
        output = knn_prediction(train, row, k)
        predictions.append(output)
    return predictions


def cross_validation_split(dataset, n_folds):
    dataset_copy = dataset.copy()
    shuffled = dataset_copy.sample(frac=1)
    return np.array_split(shuffled, n_folds)


def evaluate_knn(dataset, n_folds, k):
    folds = cross_validation_split(dataset, n_folds)
    scores = []
    for i, fold in enumerate(folds):
        fold_copy = folds.copy()
        fold_copy.pop(i)
        train_set = []
        for df in fold_copy:
            for row in df.iterrows():
                train_set.append(row[1])

        test_set = []
        for _, row in fold.iterrows():
            row_copy = list(row)
            test_set.append(row_copy)
            row_copy[0] = None
        predicted = knn(train_set, test_set, k)
        actual = [row[0] for _, row in fold.iterrows()]
        acc = accuracy(actual, predicted)
        scores.append(acc)
        print(acc)
    return scores


def accuracy(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0


seed(42)
file = 'heart-anomalies.csv'
folds = 5
neighbors = 5
dataset = pd.read_csv(file, header=None)

scores = evaluate_knn(dataset, folds, neighbors)
print('Scores: %s' % scores)
print('Mean Accuracy: %.3f%%' % (sum(scores)/float(len(scores))))
