from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB

import pandas as pd


class Model(object):
    """docstring for Model."""
    Classifiers = {'RF': 'RandomForestClassifier', 'SVM': 'SVC'}
    classfier_params = {
        'RandomForestClassifier':
            {
                'n_estimators':
                    {
                        'default': 100,
                        'param_values': {'int': []}
                    },
                'max_features':
                    {
                        'default': 'auto',
                        'param_values': {'int': [], 'float': [], 'string': [], None: []}
                    }
            },
        'SVC':
            {
                'kernel':
                    {
                        'default': 'rbf',
                        'param_values': {'string': ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']}
                    },
                'C':
                    {
                        'default': 1.0,
                        'param_values': {'float': ['+']}
                    },
                'gamma':
                    {
                        'default': 'scale',
                        'param_values': {'string': ['scale', 'auto'],
                                         'float': []}
                    }
            }

    }

    def __init__(self, app, dataset, name):
        self.app = app
        self.dataset = dataset
        self.classifier_name = name
        self.test_size = 0.2
        self.classifier = eval(name)()  # https://stackoverflow.com/a/7719518
        self.app.logger.info("Model Instance created ")
        self.parameters = self.classfier_params[self.classifier_name]

    def get_params(self):
        return self.parameters

    def process_params(self, params):
        for key in params.keys():
            types = self.parameters[key]['param_values'].keys()
            if 'string' in types and params[key].isalpha():
                if params[key] not in self.parameters[key]['param_values']['string']:
                    if 'float' in types or 'int' in types:
                        print("Invalid String input")
                    else:
                        print("Values of key '{}' saved.".format(key))
                else:
                    print("Values of key '{}' saved.".format(key))
            elif 'float' in types:
                params[key] = float(params[key])
                print("Values of key '{}' changed from string {} to float {}".format(key,str(params[key]),params[key]))
            elif 'int' in types:
                params[key] = int(params[key])
                print("Values of key '{}' changed from string {} to int {}".format(key,str(params[key]),params[key]))
        return params

    def set_params(self, params):
        self.classifier.set_params(**self.process_params(params))

    def set_split_ratio(self, test_size):
        self.test_size = test_size
        # if 0 then perform complete training
        # else store as X_train, X_validation , y_train , y_validation
        # use dataset instance

    def get_train_test_data(self, test_size):
        X = self.dataset.get_features()
        y = self.dataset.get_target()
        X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=test_size, random_state=6)
        return X_train, X_test, Y_train, Y_test

    def model_train(self):
        X_train, X_test, Y_train, Y_test = self.get_train_test_data(self.test_size)
        self.classifier.fit(X_train, Y_train)
        predictions = self.classifier.predict(X_test)
        acc_score = self.compute_accuracy(predictions, Y_test)
        return "Model Trained with accuracy {}.".format(acc_score)

    def compute_accuracy(self, predictions, Y_test):
        acc_score = accuracy_score(Y_test, predictions)
        print(acc_score)
        print(confusion_matrix(Y_test, predictions))
        print(classification_report(Y_test, predictions))
        return acc_score
