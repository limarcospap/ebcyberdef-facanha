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
            
    def ExecuteReferee(self,kfolds,data,target,classifiers,referee_model):
        me = ModelEvaluate()
        #-----list contendo o resultado final de cada iteração 
        
        iterations_results=[]
        #------#
        it=1
        
        for train_index, test_index in kfolds:
            print("iteration {} running...".format(it),end='\r')
            
            #-----dict contendo o resultado final da presente iteração validação cruzada para cada classifcador e ábirtro
            final_results={}
            #-----------------------------------------------#
            
            # buscando o k-ésimo conjunto de treino dos k_folds
            data_train=data[train_index]
            target_train= target[train_index]
            data_test = data[test_index]
            target_test =  target[test_index] 
            
            
            #extraindo previsões de cada modelo
            train_predict=[]
            for clf in classifiers:
                #treino de cada classificador
                clf.fit(data_train,target_train)
                train_predict.append(clf.predict(data_train))
                
                
            #numero de predições de cada classificador
            lentgh_test=len(data_test)
            
            #treino do árbitro classificador
                #join data_train with classifiers predict
            train_predict = np.array(np.matrix(train_predict).transpose())
            data_referee = np.concatenate ((data_train,train_predict),axis=1)
            
            target_referee = target_train
            referee_model.fit(data_referee,target_referee)
            
            #dados para teste dos árbitros
            test_predict=[]
            for clf in classifiers:
                # extraindo previsão dos classificadores para teste do ábitro classificador
                #tbm será utilizado com entrada para votos do vot_clf 
                predicted=clf.predict(data_test)
                test_predict.append(predicted)
                
                # registrando as avaliações de cada classificador para cada iteração 
                final_results[clf.name]=me.EvaluateResults(predicted,target_test)
            
            #salvando predições no teste do árbitro classificador    
                #join data_test with classifiers test predict
            test_predict = np.array(np.matrix(test_predict).transpose())
            test_referee = np.concatenate ((data_test,test_predict),axis=1)
            
            
            referee_results = referee_model.predict(test_referee)
           
        #ÁRBITRO VOTOS
            # votos do árbitro
            referee_votes=[]
            for sample in test_predict:
                referee_votes.append(np.bincount(sample).argmax())    
            
            #avaliação do árvitro de votos
            final_results['Vot_referee']=me.EvaluateResults(referee_votes,target_test)
            

        #ÁRBITRO CLASSIFICADOR
            #avaliação do árbitro classificador
            final_results['Clf_referee']=me.EvaluateResults(referee_results,target_test)
            
            
        #saving interation final results
            iterations_results.append(final_results)
            print(end='\r')
            print("iteration {} Completed!    ".format(it))
            it+=1
        return iterations_results
        
class ModelEvaluate:
    def __init__(self):
        pass
    def EvaluateResults(self, predicted,target_test):
        tot_bot=0#análise de falsos negativos (eficiência em prever bots)
        tot_normal=0#análise de falsos positivos (eficiência em prever normal)
        parcial_values=[]        
        for i in range (len(predicted)):
            if predicted[i] == 0 and target_test[i] == 0:
                tot_bot+=1
            elif predicted[i] ==1 and target_test[i]== 1:
                tot_normal+=1
        #salvando resultados
        parcial_values.append(tot_bot/len([y for y in target_test if y == 0]))#bot
        parcial_values.append(tot_normal/len([y for y in target_test if y == 1]))#normal
        parcial_values.append(np.sum(np.array(predicted) == np.array(target_test))/len(predicted))#total
        return parcial_values
        
    
    def ManualCrossValSubseting(self,cv_num,data,target):
        skf=StratifiedKFold(n_splits=cv_num)
        return skf.split(data,target)
    
    def ManualEvaluateModel(self,model, k_folds,data,target):
        print(model.name+": ")
        it = 1
        values = []
        for train_index, test_index in k_folds:
            parcial_values=[]
            target_train, target_test = target[train_index], target[test_index] 
            data_train, data_test = data[train_index], data[test_index]
            model.fit(data_train,target_train)
            x=model.predict(data_test)
            parcial_values.append(model.score(data_test,target_test))
            it+=1
            #encontrando eficiencia para bots  
            tot_bot = 0
            tot_normal = 0
            for i in range (len(x)):
                if x[i] ==0 and target_test[i]==0:
                    tot_bot+=1
                elif x[i] ==1 and target_test[i]==1:
                    tot_normal+=1
            parcial_values.append(tot_bot/len([y for y in target_test if y == 0]))
            parcial_values.append(tot_normal/len([y for y in target_test if y == 1]))
            #encontrando eficiencia para normal
            values.append(parcial_values)

        tot_avg=sum([x[0] for x in values ])/len(values)
        bot_avg=sum([x[1] for x in values ])/len(values)
        normal_avg=sum([x[2] for x in values ])/len(values)
        print("total: {:.2%}".format(tot_avg))
        print("bot: {:.2%}".format(bot_avg))
        print("normal: {:.2%}".format(normal_avg))

        return (tot_avg*100, bot_avg*100, normal_avg*100)
            
    

if __name__ == "__main__":
    pass
 
