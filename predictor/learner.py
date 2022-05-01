# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yXyoyGaTAuk0j3-9lmCt-f8XiMGrrxtp
"""

import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression, LinearRegression
import numpy as np
from pathlib import Path
import operator
from math import sqrt
from statistics import mean
import pickle
import warnings
from sklearn.metrics import r2_score
from sklearn import linear_model

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
pd.options.mode.chained_assignment = None

class Learner:
    ml_model = None
    dataset = None
    X = None
    y = None
    enc = None 

    def set_encoder(self, file):
        tmp = pd.read_csv(file)
        tmp = tmp.drop(columns=['Price'])
        self.enc = pd.get_dummies(tmp).columns

    def train_and_predict(self, file, brand, model, kms, license, year, capacity, type_):
        if(self.preprocess(file, brand, model)==-1):
          return -1
        self.learn()
        return self.predict(kms, license, year, capacity, type_)

    def preprocess(self, file, brand, model):
        self.dataset = pd.read_csv(file)
        self.dataset = self.dataset.fillna(0)
        df = self.dataset[self.dataset['Brand'] == brand].copy()
        df['Same_model'] = np.where(df['Model'] == model, 1, 0)
        df = df.drop(columns=['Brand', 'Model'])
        if(len(df)==0):
          return -1
        self.y = df['Price'].copy()
        self.X = df.drop(columns=['Price']).copy()
        self.X = pd.get_dummies(self.X)
        for i in self.enc:
            if i not in self.X:
                self.X[i] = 0
        self.X = self.X.reindex(sorted(self.X.columns), axis=1)

    def learn(self):
        self.ml_model = LinearRegression()
        self.ml_model.fit(self.X, self.y)
        # save the model to disk
        #filename = 'finalized_model.sav'
        #pickle.dump(self.ml_model, open(filename, 'wb'))

        return self.ml_model

    def predict(self, kms, license, year, capacity, type_):
        dt = pd.DataFrame.from_dict({'Kms': [kms], 'License': [license], 'Year': [year], 'Capacity': [capacity],
                                       'Type': [type_], 'Same_model': [1]})
        
        dt = pd.get_dummies(dt)
        for i in self.enc:
            if i not in dt:
                dt[i] = 0 
        dt = dt.reindex(sorted(dt.columns), axis=1)
        val = self.ml_model.predict(dt)[0]
        #return self.ml_model.predict(dt)[0]
        return "{0:.3f}".format(val)