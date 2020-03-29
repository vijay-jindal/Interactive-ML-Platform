from sklearn.ensemble import RandomForestClassifier

class Model(object):
    """docstring for Model."""
    def __init__(self, app, dataset, name):
        self.app = app
        self.dataset = dataset
        self.classifier_name = name
        self.classifier = eval(name)()
        self.app.logger.info("Model Instance created ")

    def get_params(self):
        return self.classifier.get_params()
