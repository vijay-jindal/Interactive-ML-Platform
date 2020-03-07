from dataclasses import dataclass

@dataclass
class Dataset:
    '''Class for keeping Sotring info about Dataset '''
    datasetName: str
    datasetPath : str
    numberOfColumns: int = 0
    numberOfRows: int = 0

    def __init__(self, datasetName: str,datasetPath :str, numberOfColumns: int, numberOfRows: int = 0):
        self.datasetName = datasetName
        self.datasetPath = datasetPath
        self.numberOfColumns = numberOfColumns
        self.numberOfRows = numberOfRows

@dataclass
class Algorithm:
    '''Class for keeping Sotring info about Algorithm Chosen by user '''
    algorithmName: str
    support_vector_machine=dict(
                              {'SVM': True,
                              'criterion': 'mse',
                              'max_depth': None,
                              'max_features': 'auto',
                              'max_leaf_nodes': None,
                              'min_impurity_decrease': 0.0,
                              'min_impurity_split': None,
                              'min_samples_leaf': 1,
                              'min_samples_split': 2,
                              'min_weight_fraction_leaf': 0.0,
                              'n_estimators': 10,
                              'n_jobs': 1,
                              'oob_score': False,
                              'random_state': 42,
                              'verbose': 0,
                              'warm_start': False})
    random_forest=dict(
                              {'RANDOM_FOREST': True,
                              'criterion': 'mse',
                              'max_depth': None,
                              'max_features': 'auto',
                              'max_leaf_nodes': None,
                              'min_impurity_decrease': 0.0,
                              'min_impurity_split': None,
                              'min_samples_leaf': 1,
                              'min_samples_split': 2,
                              'min_weight_fraction_leaf': 0.0,
                              'n_estimators': 10,
                              'n_jobs': 1,
                              'oob_score': False,
                              'random_state': 42,
                              'verbose': 0,
                              'warm_start': False})
    k_nearest_neighbours=dict(
                              {'KNN': True,
                              'criterion': 'mse',
                              'max_depth': None,
                              'max_features': 'auto',
                              'max_leaf_nodes': None,
                              'min_impurity_decrease': 0.0,
                              'min_impurity_split': None,
                              'min_samples_leaf': 1,
                              'min_samples_split': 2,
                              'min_weight_fraction_leaf': 0.0,
                              'n_estimators': 10,
                              'n_jobs': 1,
                              'oob_score': False,
                              'random_state': 42,
                              'verbose': 0,
                              'warm_start': False})



    def __init__(self,algorithmName,bootstrap: bool = True,criterion: str = 'mse',max_depth: int = None,max_features: str = 'auto',
                 max_leaf_nodes: int = None,min_impurity_decrease: float = 0.0,min_impurity_split: bool = None,
                 min_samples_leaf: int = 1,min_samples_split: int = 2,min_weight_fraction_leaf: float = 0.0,
                 n_estimators: int = 10,n_jobs: int = 1,oob_score: bool = False,random_state: int = 42,verbose: int = 0,
                 warm_start: bool = False):
        self.bootstrap = bootstrap
        self.criterion = criterion
        self.max_depth = max_depth
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes
        self.min_impurity_decrease = min_impurity_decrease
        self.min_impurity_split = min_impurity_split
        self.min_samples_leaf = min_samples_leaf
        self.min_samples_split = min_samples_split
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.n_estimators = n_estimators
        self.n_jobs = n_jobs
        self.oob_score = oob_score
        self.random_state = random_state
        self.verbose = verbose
        self.warm_start = warm_start