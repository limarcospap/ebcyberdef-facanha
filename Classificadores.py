from sklearn.tree import DecisionTreeClassifier 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import StratifiedKFold
from  sklearn.neural_network import MLPClassifier
import numpy as np 

class Classifier(object):
    def __init__(self,data=None,target=None):
        self.name = None
        self.model = None
        self.data = data
        self.target = target
        self.individualEvaluate_model= None
    def fit(self,trainData,trainTarget):
        self.model.fit(trainData,trainTarget)
    
    def predict(self,testData):
        return self.model.predict(testData)
    
    def predict_proba(self,testData):
        return self.model.predict_proba(testData)
    
    def score(self,testData,targetData):
        return self.model.score(testData,targetData)

    #usar para retornar modelos pros juízes
    def getModel(self):
        return self.individualEvaluate_model
    

        
class DecisionTree_Classifier(Classifier):
    def __init__(self,data=None,target=None,max_d=22):
        super().__init__()
        Classifier.__init__(self,data,target)
        self.name = "DecisionTree"
        self.model = DecisionTreeClassifier(max_depth=22,random_state=0)
        self.individualEvaluate_model= DecisionTreeClassifier(max_depth=max_d,random_state=0)    
    
class KNN_Classifier(Classifier):
    def __init__(self,data=None,target=None):
        super().__init__()
        Classifier.__init__(self,data,target)
        self.name = "KNN"
        self.model = KNeighborsClassifier(n_neighbors=3)
        self.individualEvaluate_model= KNeighborsClassifier(n_neighbors=3)

class SVM_Classifier(Classifier):
    def __init__(self,data=None,target=None):
        super().__init__()
        Classifier.__init__(self,data,target)
        self.name = "SVM"
        self.model = SVC(C = 100, kernel = 'rbf', gamma = 0.0001)
        self.individualEvaluate_model = SVC(C = 100, kernel = 'rbf', gamma = 0.0001)

    def set_params(self, kernel = 'rbf', gamma = 1, C = 0.1):
        self.model.C = C
        self.model.gamma = gamma
        self.model.kernel = kernel


class NaiveBayes_Classifier(Classifier):
    def __init__(self,data=None,target=None):
        super().__init__()
        Classifier.__init__(self,data,target)
        self.name = "NaiveBayes"
        #self.model =  MultinomialNB(alpha=1,fit_prior=False)
        #self.model =  BernoulliNB(alpha=1,fit_prior=False)
        self.model =  GaussianNB()
        #self.individualEvaluate_model=  BernoulliNB(alpha=1,fit_prior=False)
        self.individualEvaluate_model=  GaussianNB()

class Perceptron_Classifier(Classifier):
    def __init__(self, data=None, target=None):
        super().__init__()
        Classifier.__init__(self, data, target)
        self.name = "Perceptron"
        self.model = MLPClassifier(solver='adam', hidden_layer_sizes=(8), alpha = 100, random_state=1)
        self.individualEvaluate_model = MLPClassifier(solver='adam', hidden_layer_sizes=(8), alpha = 100, random_state=1)
        self.model.set_params()

    def set_params(self, solver = 'adam', alpha=100, hidden_layer_sizes=(8)):
        self.model.solver = solver
        self.model.alpha = alpha
        self.model.hidden_layer_sizes = hidden_layer_sizes


class Referee :
    def __init__(self):
        pass
            
    def ExecuteReferee(self,data,target,classifiers,referee_model):
        data_train=data
        target_train= target
        
        #extraindo previsões de cada modelo
        train_predict=[]
        for clf in classifiers:
            #treino de cada classificador
            clf.fit(data_train,target_train)
            train_predict.append(clf.predict(data_train))
        
        #treino do árbitro classificador
            #join data_train with classifiers predict
        train_predict = np.array(np.matrix(train_predict).transpose())
        data_referee = np.concatenate ((data_train,train_predict),axis=1)
        
        target_referee = target_train
        referee_model.fit(data_referee,target_referee)
        
        return referee_model
        
