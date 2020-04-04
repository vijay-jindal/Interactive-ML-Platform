from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

class Model(object):
    """docstring for Model."""
    Classifiers = {'RF': 'RandomForestClassifier', 'SVM':'SVC'}

    def __init__(self, app, dataset, name):
        self.app = app
        self.dataset = dataset
        self.classifier_name = name
        self.classifier = eval(name)() # https://stackoverflow.com/a/7719518
        self.app.logger.info("Model Instance created ")

    def get_params(self):
        return self.classifier.get_params()

    def set_params(self, **kwargs):
        self.classifier.set_params(**kwargs)

    def set_split_ratio(self, test_size):
        self.test_size = test_size
        # if 0 then perform complete training
        # else store as X_train, X_validation , y_train , y_validation
        # use dataset instance
