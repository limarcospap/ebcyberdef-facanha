from Classificadores import KNN_Classifier,DecisionTree_Classifier,SVM_Classifier,Referee,NaiveBayes_Classifier, Perceptron_Classifier
import ProcessingData
import numpy as np
from datetime import datetime 
import os 
import sys
#recebendo os argumentos para formação do comitê

models = ['DT', 'SVM', 'KNN', 'MLP','NB']
mod = [1,0,0,0,0] # to selecionando só o DT

class RefereeFunctions():
    def __init__(self):
        self.strA = mod
        self.strB = 0
        self.prep = ProcessingData.PreProcessingData()
        self.prep.generateData(reduce_factor=20)
        self.data, self.target = self.prep.getData()
        self.r = Referee()
        self.committe_models  = self.strA #é uma lista com 1 pra cada modelo
        self.referee_model = int(self.strB) #pega o indice
        # as listas abaixo devem ser alteradas para inserir um novo classificador implementado. Exemplo :"[...,NewCllf_Classifier()]"
        # sempre inserir ao final para combinar com interface 
        #criar dois desses é necessário pois python passa seus objetos por referência sempre
        self.model_list = [DecisionTree_Classifier(),SVM_Classifier(),KNN_Classifier(),Perceptron_Classifier(),NaiveBayes_Classifier()]
        referee_model_list = [DecisionTree_Classifier(),SVM_Classifier(),KNN_Classifier(),Perceptron_Classifier(),NaiveBayes_Classifier()]

        self.clfs = [self.model_list[i] for i in range(len(self.model_list)) if self.committe_models[i]==1]
        self.ref_clf = referee_model_list[self.referee_model]
        self.referee = self.TrainModelReferee(self.data, self.target, self.r)
        

    
    def TrainModelReferee(self, data, target, r):
        ref_clf = r.ExecuteReferee(data,target,self.clfs,self.ref_clf)
        return ref_clf

    def RefereePredict(self, newNetworkFlow):
        classifiers = self.clfs
        #gerar os dados para o referee
        test_predict=[]
        for clf in classifiers:
            # extraindo previsão dos classificadores para teste do ábitro classificador
            #tbm será utilizado com entrada para votos do vot_clf 
            predicted=clf.predict(newNetworkFlow)
            test_predict.append(predicted)
        
        
        test_predict = np.array(np.matrix(test_predict).transpose())
        flowToPredict = np.concatenate ((newNetworkFlow,test_predict),axis=1)

        print(flowToPredict)
        return self.referee.predict(flowToPredict)
                 