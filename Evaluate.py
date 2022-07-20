from Classificadores import KNN_Classifier,DecisionTree_Classifier,SVM_Classifier,Referee,NaiveBayes_Classifier, Perceptron_Classifier
import ProcessingData
import numpy as np
from datetime import datetime 
import os 
import sys
#recebendo os argumentos para formação do comitê

models = ['DT', 'SVM', 'KNN', 'MLP','NB']
mod = [1,1,1,1,1] # to selecionando só o DT
threshold = 0.2

class RefereeFunctions():
    def __init__(self):
        self.strA = mod
        self.strB = 3
        self.prep = ProcessingData.PreProcessingData()
        self.prep.generateData(reduce_factor=10)
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
            predicted=[np.int32(clf.predict(newNetworkFlow)[0]).item()]
            test_predict.append(predicted)
        
        test_predict = np.array(np.matrix(test_predict).transpose())
        flowToPredict = np.concatenate ((newNetworkFlow,test_predict),axis=1)

        classif = self.referee.predict(flowToPredict)
        proba = self.referee.predict_proba(flowToPredict)
        ref_classif = ([],[])

        for i in range(0,len(proba)):
            proba_bot = proba[i][0]
            proba_normal = proba[i][1]
            # 0->bot
            # 1->normal
            # 2->sus
            ref_classif[0].append(2 if abs(proba_bot-proba_normal) < threshold else np.int32(classif[i]).item())
            ref_classif[1].append((proba_bot, proba_normal))

        return ref_classif

                 