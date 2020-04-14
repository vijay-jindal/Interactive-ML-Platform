from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


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
                        'param_values': {'int': [], 'float': [], 'string': ['auto', 'sqrt', 'log2'], None: []}
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
        self.classifier = eval(self.classifier_name)()  # https://stackoverflow.com/a/7719518
        self.parameters = self.classfier_params[self.classifier_name]
        self.app.logger.info("Model Instance created ")

    def get_params(self):
        return self.parameters

    def process_params(self, params):
        self.app.logger.info("Changed params : {}".format(params))
        bad_value = []
        try:
            for key in params.keys():
                types = self.parameters[key]['param_values'].keys()
                print(key)
                if None in types and params[key] == 'None':
                    params[key] = None

                elif 'string' in types and params[key].isalpha():
                    if params[key] not in self.parameters[key]['param_values']['string']:
                        self.app.logger.info("Invalid String input.".format(key))
                        bad_value.append(key)
                    else:
                        self.app.logger.info("Values of key '{}' saved.".format(key))

                elif 'float' in types and not params[key].isalpha():
                    params[key] = float(params[key])
                    self.app.logger.info(
                        "Values of key '{}' changed from string {} to float {}".format(key, str(params[key]),
                                                                                       params[key]))
                elif 'int' in types and not params[key].isalpha():
                    params[key] = int(params[key])
                    self.app.logger.info(
                        "Values of key '{}' changed from string {} to int {}".format(key, str(params[key]),
                                                                                     params[key]))
                else:
                    bad_value.append(key)

            if len(bad_value) == 0:
                return params, 1
            else:
                raise Exception
        except:
            self.app.logger.error("INVALID INPUT FOR THE HYPERPARAMETERS '{}'. INPUT : {}".format(bad_value,params))
            params['bad_value'] = bad_value
            return params, 0

    def set_params(self, params):
        try:
            processed_params, status = self.process_params(params)
            if status == 1:
                self.classifier.set_params(**processed_params)
                return 1
            else:
                raise Exception
        except:
            return "Invalid value for the hyperparameters {}".format(processed_params['bad_value'])
        # modify self.parameters too

    def set_split_ratio(self, test_size):
        self.test_size = test_size
        # if 0 then perform complete training
        # else store as X_train, X_validation , y_train , y_validation
        # use dataset instance

    def get_train_test_data(self, test_size):
        X = self.dataset.get_features()
        y = self.dataset.get_target()
        self.app.logger.info(
            "Data divided into {}% Training data and {}% Testing data".format((1 - test_size) * 100, test_size * 100))
        return train_test_split(X, y, test_size=test_size, random_state=6)

    def model_train(self):
        X_train, X_test, Y_train, Y_test = self.get_train_test_data(self.test_size)
        self.app.logger.info("Training the model. Classifier : {}.".format(self.classifier))
        self.classifier.fit(X_train, Y_train)
        self.app.logger.info("Model Training done.")
        predictions = self.classifier.predict(X_test)
        acc_score = self.compute_accuracy(predictions, Y_test)
        return "Model Trained with accuracy {}.".format(acc_score)

    def compute_accuracy(self, predictions, Y_test):
        acc_score = accuracy_score(Y_test, predictions)
        self.app.logger.info("MODEL ACCURACY CALCULATED BASED ON TEST DATA: ")
        self.app.logger.info(acc_score)
        self.app.logger.info(confusion_matrix(Y_test, predictions))
        self.app.logger.info(classification_report(Y_test, predictions))
        return acc_score
