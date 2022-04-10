from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.svm import LinearSVC
from ProcessingData import PreProcessingData
import numpy as np


class SVMGridSearch:
    def __init__(self, verbose=5):
        self.param_grid = {'C':[0.1, 1, 10, 100, 1000], 'gamma':['auto', 1, 0.1, 0.01, 0.001, 0.0001], 'kernel':['rbf', 'linear']}
        self.verbose = verbose
        self.model = LinearSVC(random_state=0)

    def fit(self, trainData, trainTarget):
        self.model = GridSearchCV(SVC(), self.param_grid, refit=True, verbose=self.verbose, n_jobs=4)
        self.model.fit(trainData, trainTarget)
        print(self.model.best_params_)

    def predict(self, testData):
        return self.model.predict(testData)

    def get_params(self):
        return self.model.best_estimator_.get_params()


prep = PreProcessingData()
prep.generateData(reduce_factor=20)
data,target = prep.getData()
svm=SVMGridSearch()
svm.fit(np.matrix(data),target)
print(svm.get_params())
