# Word to vec implementation https://jaketae.github.io/study/word2vec/
# id3 implementation https://towardsdatascience.com/id3-decision-tree-classifier-from-scratch-in-python-b38ef145fd90
import math
import random
import sys
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import numpy as np

np.random.seed(42)


nltk.download('stopwords')
# Create a set of stop words
stop_words = set(stopwords.words('english'))
# Define a function to remove stop words from a sentence


def clean_and_tokenize(text):
  # Split the sentence into individual words
    pattern = re.compile(r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*')
    words = pattern.findall(text.lower())
    filtered_words = [
        word for word in words if word not in stop_words and word != '']
    return filtered_words


def encoded_text(text, author):
    encoded_paragraphs = []
    for paragraph in text.split('\n\n'):
        encoded_dict = {}
        tokens = clean_and_tokenize(paragraph)
        # if a word is present mark it
        for token in tokens:
            encoded_dict[token] = 1
        if author == 'shelley':
            encoded_dict['author'] = 1
        else:
            encoded_dict['author'] = 0
        encoded_paragraphs.append(encoded_dict)
    return encoded_paragraphs


with open('shelley-frankenstein.txt') as file:
    frankenstein = file.read()

with open('austen-northanger-abbey.txt') as file:
    abbey = file.read()

with open('austen-pride-and-prejudice.txt') as file:
    pride = file.read()

with open('shelley-the-last-man.txt') as file:
    man = file.read()

from_start = True
if from_start:
    all_tokens = list(set(clean_and_tokenize(
        frankenstein + abbey + pride + man)))

    frankenstein_encodings = encoded_text(frankenstein, 'shelley')
    abbey_encodings = encoded_text(abbey, 'austen')
    pride_encodings = encoded_text(pride, 'austen')
    man_encodings = encoded_text(man, 'shelley')

    all_encodings = frankenstein_encodings + \
        abbey_encodings + pride_encodings + man_encodings

    data = pd.DataFrame.from_dict(all_encodings).fillna(0).astype(int)
    data.to_csv('encoded_text.csv', index=False)
else:
    data = pd.read_csv('encoded_text.csv')

# XXX Recursively building a tree; depth will depend on
# number of instance features.
sys.setrecursionlimit(17000)

# for row in data.iterrows():
# 	print(row)

# implementation dervied from https://github.com/pdx-cs-ai/psamid3/blob/main/id3.py

# Class of instances.


class Instance(object):
    def __init__(self, row, random=False):
        if random == False:
            self.label = int(row.get('author'))
            del row['author']
            self.features = [int(i) for i in row]
        else:
            self.label = int(row[0])
            self.features = [int(i) for i in row[1:]]


# sample_size = .2
# data.reset_index(drop=True)
# https://stackoverflow.com/questions/24147278/how-do-i-create-test-and-train-samples-from-one-dataframe-with-pandas
train = data.sample(frac=0.8, random_state=200)
test = data.drop(train.index)
train_instances = [Instance(row) for _, row in train.iterrows()]
test_instances = [Instance(row) for _, row in test.iterrows()]
min_chisquare = 3.841
nfeatures = len(train_instances[0].features)

if len(sys.argv) > 2:
    min_gain = float(sys.argv[2])
else:
    min_gain = 0.05


def count_labels(insts):
    n_insts = len(insts)
    np = 0
    for i in insts:
        np += i.label
    return np, n_insts-np


def chi_square(pos, neg):
    avg = (pos + neg) / 2
    dpos = pos - avg
    dneg = neg - avg
    return (dpos**2 + dneg**2) / avg


def entropy(insts):
    np, nn = count_labels(insts)
    ninsts = np + nn

    if np == 0 or nn == 0:
        return 0

    pr_p = np / ninsts
    pr_n = nn / ninsts

    return -pr_p * math.log2(pr_p) - pr_n * math.log2(pr_n)


def majority(insts):
    np, nn = count_labels(insts)
    return int(np > nn)


def split(insts, f):
    splits = [[] for _ in range(2)]
    for i in insts:
        splits[i.features[f]].append(i)
    return splits[1], splits[0]


class DTree(object):
    def __init__(self, insts, used=None, u=None):
        if used is None:
            used = set()
        else:
            used = set(used)
        self.label = None

        if len(used) == nfeatures:
            self.label = majority(insts)

            # get number of positive and negatives
        np, nn = count_labels(insts)
        ninsts = np + nn
        # chis = chi_square(np, nn)
        # if chis < min_chisquare:
        #     self.label = int(np > nn)
        #     return

        if u is None:
            u = entropy(insts)
        self.u = u

        best_f = None
        best_gain = None
        best_split = None

        for f in range(nfeatures):
            if f in used:
                continue

            pos, neg = split(insts, f)
            npos = len(pos)
            nneg = len(neg)

            if npos == 0 or nneg == 0:
                continue

            u_pos = entropy(pos)
            u_neg = entropy(neg)

            pr_pos = npos / ninsts
            pr_neg = nneg / ninsts

            gain = u - pr_pos*u_pos - pr_neg * u_neg
            if gain <= 0:
                continue
            if best_gain is None or gain > best_gain:
                best_gain = gain
                best_f = f
                best_split = ((pos, u_pos), (neg, u_neg))

        if best_f is None:
            self.label = majority(insts)
            return
        # best_split undefined here
        ps, ns = best_split
        pos, pu = ps
        neg, nu = ns
        used.add(best_f)
        self.f = best_f
        self.pos = DTree(pos, used=used, u=pu)
        self.neg = DTree(neg, used=used, u=nu)

    def classify(self, inst):
        if self.label is not None:
            return self.label
        if inst.features[self.f] > 0:
            return self.pos.classify(inst)
        else:
            return self.neg.classify(inst)

# Try training on the training instances and then
# classifying the test instances.  Return the classification
# accuracy.


def try_tc(training, test):
    # Build a decision tree for the training data.
    tree = DTree(training)

    # Score test instances.
    matrix = [[0] * 2 for _ in range(2)]
    for inst in test:
        guess = tree.classify(inst)
        matrix[inst.label][guess] += 1

    return matrix, tree


def test_random(tree):
    # Score test instances.
    matrix = [[0] * 2 for _ in range(2)]
    # Generate 1000 lists of length 16296 with random 1's and 0's
    random_vec = np.random.randint(2, size=(1000, nfeatures+1))

    # Convert the NumPy array to a list of lists
    random_vec = random_vec.tolist()
    random_insts = [Instance(inst, random=True) for inst in random_vec]
    for inst in random_insts:
        guess = tree.classify(inst)
        matrix[inst.label][guess] += 1
    return matrix


def accuracy_measure(matrix, instances):
    accuracy = (matrix[0][0] + matrix[1][1]) / ntest
    fpr = matrix[0][1] / ntest
    fnr = matrix[1][0] / ntest
    print(f"acc:{accuracy:.3f} fpr:{fpr:.3f}  fnr:{fnr:.3f}")


ntest = len(test_instances)
actual_results, tree = try_tc(train_instances, test_instances)
accuracy_measure(actual_results, ntest)
# random_results = test_random(tree)
# accuracy_measure(random_results, 1000)
