# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 11:42:34 2018

@author: Yuri
"""


from Classificadores import KNN_Classifier,DecisionTree_Classifier,SVM_Classifier,Referee,ModelEvaluate,NaiveBayes_Classifier, Perceptron_Classifier
import ProcessingData
from datetime import datetime 
import os 
import sys
#recebendo os argumentos para formação do comitê
strA = sys.argv[1].replace('[', ' ').replace(']', ' ').replace(',', ' ').split()
strB = sys.argv[2]
strC = sys.argv[3]

committe_models  = [int(i) for i in strA]
referee_model = int(strB)
n_splits = int(strC)
print (committe_models,referee_model,n_splits)


prep =ProcessingData.PreProcessingData()
prep.generateData(reduce_factor=20)
data,target = prep.getData()

me = ModelEvaluate()
r = Referee()   

# as listas abaixo devem ser alteradas para inserir um novo classificador implementado. Exemplo :"[...,NewCllf_Classifier()]"
# sempre inserir ao final para combinar com interface 
#criar dois desses é necessário pois python passa seus objetos por referência sempre
model_list = [DecisionTree_Classifier(),SVM_Classifier(),KNN_Classifier(),Perceptron_Classifier(),NaiveBayes_Classifier()]
referee_model_list = [DecisionTree_Classifier(),SVM_Classifier(),KNN_Classifier(),Perceptron_Classifier(),NaiveBayes_Classifier()]

clfs = [model_list[i] for i in range(len(model_list)) if committe_models[i]==1]
ref_clf = referee_model_list[referee_model]

kfolds = me.ManualCrossValSubseting(n_splits,data,target)
results = r.ExecuteReferee(kfolds,data,target,clfs,ref_clf)
path=os.path.abspath(os.path.dirname(__file__))+"\\Results\\{}.txt".format(datetime.strftime(datetime.now(),"%Y_%m_%d"))
with open(path,'w') as f: 
    for it in range(len(results)):
        f.write("\nResults:\n")
        print("\nResults:")
        f.write("----iteration {}----\n".format(it+1))
        print("----iteration {}----".format(it+1))
        for name in results[it].keys():
            f.write("{} => {:.2%} - {:.2%} - {:.2%}\n".format(name,results[it][name][0],results[it][name][1],results[it][name][2]))
            print("{} => {:.2%} - {:.2%} - {:.2%}\n".format(name,results[it][name][0],results[it][name][1],results[it][name][2]))
        f.write('\n')
        print('\n')
    # Averages
    f.write("\nAverages:\n")
    print("\nAverages:")
        
    for name in results[it].keys():
        values = [y[name] for y in results ]
        tot_avg=sum([x[2] for x in values ])/len(values)
        bot_avg=sum([x[0] for x in values ])/len(values)
        normal_avg=sum([x[1] for x in values ])/len(values)
        f.write("===={}==== \n".format(name))
        print("===={}==== \n".format(name))
        print("total: {:.2%}".format(tot_avg))
        print("bot: {:.2%}".format(bot_avg))
        print("normal: {:.2%}".format(normal_avg))
        f.write("total: {:.2%}\n".format(tot_avg))
        f.write("bot: {:.2%}\n".format(bot_avg))
        f.write("normal: {:.2%}\n".format(normal_avg))            

exit()