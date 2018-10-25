#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 10:53:37 2018

@author: pavel
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score, make_scorer
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier

def classification_report_with_accuracy_score(y_true, y_pred):
    print(classification_report(y_true, y_pred))
    return accuracy_score(y_true, y_pred)

#%%

AGGREGATE = False
#AGGREGATE = True
DATAFILE = 'en_docs_clean.csv.gz'
LANG = 'english'
#DATAFILE = 'pt_docs_clean.csv.gz'
#LANG = None

data = pd.read_csv(DATAFILE, header=0, encoding='utf-8')

if (AGGREGATE):
    full_manifestos = data.groupby(['manifesto_id', 'party', 'date', 'title']).agg({'text' : sum})
    data = full_manifestos.reset_index()

party_counts = data.party.value_counts()
party_counts = party_counts[party_counts >= 5]
data = data[data.party.isin(party_counts.index)]

print(data.party.value_counts())

#%%

vectorizer = TfidfVectorizer(stop_words=LANG)
tfidfdata = vectorizer.fit_transform(data.text)
classes = data.party

#%%

models = {
          'nb' : MultinomialNB(), 
          'svm' : svm.SVC(kernel='linear'), 
          'rf' : RandomForestClassifier(), 
          'ab' : AdaBoostClassifier(), 
          'gb' : GradientBoostingClassifier(), 
          'mlp' : MLPClassifier(hidden_layer_sizes=(5, 5)), 
          }

accuracies = {}
for name in models:
    clf = models[name]
    scores = cross_val_score(clf, tfidfdata, classes, cv=5,
                             scoring=make_scorer(classification_report_with_accuracy_score), n_jobs=3)
    accuracies[name] = (scores.mean(), scores.std() * 2)
    print("Accuracy %s: %0.2f (+/- %0.2f)" % (name, accuracies[name][0], accuracies[name][1]))
    print("*" * 80)

for name in accuracies:
    print("Accuracy %s: %0.2f (+/- %0.2f)" % (name, accuracies[name][0], accuracies[name][1]))
