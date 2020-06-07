from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.cluster import KMeans

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import re
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
                        'param_values': {'int': ['+']},
                        'tooltip_message':'The number of trees in the forest',
                        'link':'https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html'
                    },
                'max_features':
                    {
                        'default': 'auto',
                        'param_values': {'int': ['+'], 'float': ['+'], 'string': ['auto', 'sqrt', 'log2'], None: []},
                        'tooltip_message': 'The number of features to consider when looking for the best split',
                        'link':'https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html'
                    }
            },
        'SVC':
            {
                'kernel':
                    {
                        'default': 'rbf',
                        'param_values': {'string': ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']},
                        'tooltip_message': 'SVM algorithms use a set of mathematical functions that are defined as the kernel. The function of kernel is to take data as input and transform it into the required form.',
                        'link':'https://scikit-learn.org/stable/modules/classes.html#module-sklearn.svm'
                    },
                'C':
                    {
                        'default': 1.0,
                        'param_values': {'float': ['+']},
                        'tooltip_message': 'C is a regularization parameter that controls the trade off between the achieving a low training error and a low testing error that is the ability to generalize your classifier to unseen data.',
                        'link':'https://scikit-learn.org/stable/modules/classes.html#module-sklearn.svm'
                    },
                'gamma':
                    {
                        'default': 'scale',
                        'param_values': {'string': ['scale', 'auto'],
                                         'float': ['+']},
                        'tooltip_message': ' The gamma parameter defines how far the influence of a single training example reaches, with low values meaning far and high values meaning close.',
                        'link':'https://scikit-learn.org/stable/modules/classes.html#module-sklearn.svm'
                    }
            }
    }

    Clusterers = {'KM': 'KMeans'}
    clusterer_params = {
        'KMeans':
        {
            'n_clusters':
            {
                'default': 8,
                'param_values': {'int': ['+']},
                'tooltip_message': 'The number of clusters to form as well as the number of centroids to generate',
                'link': 'https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans'
            }
        }
    }

    def __init__(self, app, dataset, type, name):
        self.app = app
        self.dataset = dataset
        self.learning_type = type

        if self.learning_type == "Supervised":
            self.classifier_name = name
            self.test_size = 0.2
            self.classifier = eval(self.classifier_name)()  # https://stackoverflow.com/a/7719518
            self.parameters = self.classfier_params[self.classifier_name]
        elif self.learning_type == "Unsupervised":
            self.clusterer_name = name
            self.clusterer = eval(self.clusterer_name)()
            self.parameters = self.clusterer_params[self.clusterer_name]

        for param in self.parameters.values(): # Optimized further : https://stackoverflow.com/a/61380863/10155936
            param['current_value'] = param['default']
        self.app.logger.info("Model Instance created ")

    def get_params(self):
        return self.parameters

    def process_params(self, params):
        self.app.logger.info("Changed params : {}".format(params))
        bad_value = []
        special_character_regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        try:
            for key in params.keys():
                types = self.parameters[key]['param_values'].keys()
                print(key)
                if None in types and params[key] == 'None':
                    params[key] = None
                    self.parameters[key]['current_value'] = params[key]

                elif 'string' in types and (params[key].isalnum() and not params[key].isnumeric()) and special_character_regex.search(params[key]) is None:
                    if params[key] not in self.parameters[key]['param_values']['string']:
                        self.app.logger.info("Invalid String input.".format(key))
                        bad_value.append(key)
                    else:
                        self.app.logger.info("Values of key '{}' saved.".format(key))
                        self.parameters[key]['current_value'] = params[key]

                elif 'float' in types and params[key].replace('.','').isnumeric() and (params[key].count('.') == 1 or params[key].count('.') == 0) and special_character_regex.search(params[key]) is None:
                    if '+' in self.parameters[key]['param_values']['float'] and float(params[key]) >= 0:
                        params[key] = float(params[key])
                        self.parameters[key]['current_value'] = params[key]
                        self.app.logger.info(
                            "Values of key '{}' changed from string {} to float {}".format(key, str(params[key]),
                                                                                           params[key]))
                    elif '-' in self.parameters[key]['param_values']['float'] and float(params[key]) <= 0:
                        params[key] = float(params[key])
                        self.parameters[key]['current_value'] = params[key]
                        self.app.logger.info(
                            "Values of key '{}' changed from string {} to float {}".format(key, str(params[key]),
                                                                                           params[key]))
                    else:
                        bad_value.append(key)

                elif 'int' in types and (params[key].lstrip("-").isnumeric() or params[key].lstrip("+").isnumeric()) and special_character_regex.search(params[key]) is None:
                    print(int(params[key]))
                    if '+' in self.parameters[key]['param_values']['int'] and int(params[key]) >= 0:
                        params[key] = int(params[key])
                        self.parameters[key]['current_value'] = params[key]
                        self.app.logger.info(
                            "Values of key '{}' changed from string {} to int {}".format(key, str(params[key]),
                                                                                         params[key]))
                    elif '-' in self.parameters[key]['param_values']['int'] and int(params[key]) <= 0:
                        params[key] = int(params[key])
                        self.parameters[key]['current_value'] = params[key]
                        self.app.logger.info(
                            "Values of key '{}' changed from string {} to int {}".format(key, str(params[key]),
                                                                                         params[key]))
                    else:
                        bad_value.append(key)

                else:
                    bad_value.append(key)

            if len(bad_value) == 0:
                return params, 1
            else:
                raise Exception
        except Exception as e:
            print(bad_value)
            self.app.logger.error(e)
            self.app.logger.error("INVALID INPUT FOR THE HYPERPARAMETERS '{}'. INPUT : {}".format(bad_value,params))
            params['bad_value'] = bad_value
            return params, 0

    def set_params(self, params):
        try:
            processed_params, status = self.process_params(params)
            if status == 1:
                processed_params['verbose'] = 100
                if self.learning_type == "Supervised":
                    self.classifier.set_params(**processed_params)
                elif self.learning_type == "Unsupervised":
                    self.clusterer.set_params(**processed_params)
                else:
                    raise Exception
                print(self.parameters)
                return 1
            else:
                raise Exception
        except:
            return "Invalid value for the hyperparameters {}".format(processed_params['bad_value'])

    def set_split_ratio(self, test_size):
        self.test_size = test_size

    def get_train_test_data(self, test_size):
        # if test_size is 0 then perform complete training
        # else store as X_train, X_validation , y_train , y_validation
        # use dataset instance
        X = self.dataset.get_features()
        y = self.dataset.get_target()
        self.app.logger.info(
            "Data divided into {}% Training data and {}% Testing data".format((1 - test_size) * 100, test_size * 100))
        return train_test_split(X, y, test_size=test_size, random_state=6)

    def model_train(self):
        if self.learning_type == "Supervised":
            X_train, X_test, Y_train, Y_test = self.get_train_test_data(self.test_size)
            self.app.logger.info("Training the model. Classifier : {}.".format(self.classifier))
            self.classifier.fit(X_train, Y_train)
            self.app.logger.info("Model Training done.")
            predictions = self.classifier.predict(X_test)
            acc_score,confusion,classify_report = self.compute_accuracy(predictions, Y_test)
            return acc_score,confusion,classify_report
        elif self.learning_type == "Unsupervised":
            self.app.logger.info(f"Model Fitting. Clusterer : {self.clusterer}")
            kmeans = self.clusterer.fit(self.dataset.get_features())
            self.app.logger.info("Model Fitting Complete")
            return kmeans.labels_
            # Show labels assigned to the dataset by updating the datatable
        else :
            self.app.logger.info("Learning type is not valid")

    def compute_accuracy(self, predictions, Y_test):
        acc_score = accuracy_score(Y_test, predictions)
        self.app.logger.info("MODEL ACCURACY CALCULATED BASED ON TEST DATA: ")
        self.app.logger.info(acc_score)
        self.app.logger.info(confusion_matrix(Y_test, predictions))
        self.app.logger.info(classification_report(Y_test, predictions))
        return acc_score,confusion_matrix(Y_test, predictions),pd.DataFrame(classification_report(Y_test, predictions,output_dict=True)).transpose()
