from  sklearn.neural_network import MLPClassifier
from Classificadores import KNN_Classifier, ModelEvaluate, DecisionTree_Classifier,NaiveBayes_Classifier, SVM_Classifier

import ProcessingData

prep =  ProcessingData.PreProcessingData()
prep.generateData(reduce_factor=50)

data,target = prep.getData()

me = ModelEvaluate()
kfolds = me.ManualCrossValSubseting(5,data,target)
#knn= KNN_Classifier()
#dt=DecisionTree_Classifier()
#svm = SVM_Classifier()
nb=NaiveBayes_Classifier()
me.ManualEvaluateModel(nb,kfolds,data,target)





