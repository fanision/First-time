import json
from collections import Counter
import operator
import pickle
from time import time






#####M-L libraries###########
import pandas
from pandas.tools.plotting import scatter_matrix
#import matplotlib.pyplot as plt
from sklearn import cross_validation
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC





training_list_group1=[]
training_list_group2=[]
training_list_group3=[]
training_list_group4=[]



with open("/Users/fanision/Desktop/Thesis_Research/Text-Mining--BioCreativeVI/bioCreative_newmutation_training.pickle",'rb') as f:
        training_data = pickle.load(f)

# with open("training_data_firstbatch.pickle",'rb') as f:
#     training_data = pickle.load(f)

# rel_dict={}
# for data in training_data:
#     a=set()
#     for key,value in data.items():
#         k = key.split(";")[0].split(".")[0]+key.split(";")[0].split(".")[1]+key.split(";")[0].split(".")[2]
             
#         try:
#             a.add(key.split(";")[2])
#         except IndexError:
#             continue
#     rel_dict[k]=a

# count =0
# for k,v in rel_dict.items():
#     if len(v)>1:
#         print(k)
#         print(v)
#         count+=1
# print(count)















for data in training_data:
        for key,value in data.items():
                if value[0]==1:
                        training_list_group1.append(value)
                if value[0]==2:
                        training_list_group2.append(value)
                if value[0]==3:
                        training_list_group3.append(value)
                if value[0]==4:
                        training_list_group4.append(value)
training_list_group1234=[]
training_list_group123=[]
training_list_group123.extend(training_list_group1)
training_list_group123.extend(training_list_group2)
training_list_group123.extend(training_list_group3)
training_list_group1234.extend(training_list_group123)
training_list_group1234.extend(training_list_group4)




# headers=["feature1","feature2","feature3","feature4","feature5","feature6","feature7","feature8","feature9","class"]
# myData = pandas.DataFrame(training_list_group123,columns = headers)










#######################################
#######################################
#training model and predict new values:

X=[]
Y=[]
for i in training_list_group1234:
        X.append(i[0:9])
        Y.append(i[9])
#cls is classifier
clf = SVC(probability=True)
clf.fit(X,Y)



#below is to test whether the classifier is good on itself
#pre=list(clf.predict(X))
# TP = 0
# FP = 0
# for i in range(len(Y)):
#     if pre[i]==1 and Y[i]==1:
#         TP+=1
#     if pre[i]==1 and Y[i]==0:
#         FP +=1
# print("TP = "+str(TP))
# print("FP = "+str(FP))

# print(X[:10])
# print(len(X))
# print(Y.count(1))
# print(pre.count(1))



#Here is to predict new values from testing dataset
with open("bioCreative_newmutation_testing.pickle",'rb') as f:
        test_data = pickle.load(f)






predict_result={}
cc=0
for data in test_data:
        for m,n in data.items():
                #if n[0]!=4: 
                if clf.predict([n[0:9]])[0]==0:
                        p = clf.predict_proba([n[0:9]])
                        print(p)
                        a=m.split(";")
                        article_id = a[0].split(".")[1]
                        #pro_entity1=a[0].split(".")[0]+"."+a[0].split(".")[2]
                        pro_entity1=a[0].split(".")[0]+"."+a[0].split(".")[2]+'.'+a[0].split(".")[3]+'.'+str(p[0])
                        pro_entity2=a[1].split(".")[0]+"."+a[1].split(".")[2]+'.'+a[1].split(".")[3]
                        pair={pro_entity1,pro_entity2}
                        if article_id in predict_result:
                                if pair not in predict_result[article_id]:
                                        predict_result[article_id].append(pair)
                        else:
                                #if this is the first positive pair for an article
                                predict_result[article_id]=[pair]

                        cc+=1
# print("positive number "+str(cc))
# print(predict_result["d17906639"])

with open('Bio_testing_predict_result_proba_0.pickle', 'wb') as handle:
        pickle.dump(predict_result,handle)





# #####################################################
# #Evaluate algorithms
# #####################################################

# # Separate training and final validation data set. First remove class
# # label from data (X). Setup target class (Y)
# # Then make the validation set 20% of the entire
# # set of labeled data (X_validate, Y_validate)
# valueArray = myData.values
# X = valueArray[:,1:7]
# Y = valueArray[:,8]
# test_size = 0.20
# seed = 7
# X_train, X_validate, Y_train, Y_validate = cross_validation.train_test_split(X, Y, test_size=test_size, random_state=seed)

# # Setup 10-fold cross validation to estimate the accuracy of different models
# # Split data into 10 parts
# # Test options and evaluation metric
# num_folds = 10
# num_instances = len(X_train)
# seed = 7
# scoring = 'accuracy'

# ######################################################
# # Use different algorithms to build models
# ######################################################

# # Add each algorithm and its name to the model array
# models = []
# models.append(('KNN', KNeighborsClassifier()))
# models.append(('CART', DecisionTreeClassifier()))
# models.append(('NB', GaussianNB()))
# models.append(('SVM', SVC()))

# # Evaluate each model, add results to a results array,
# # Print the accuracy results (remember these are averages and std
# results = []
# names = []
# for name, model in models:
#     kfold = cross_validation.KFold(n=num_instances, n_folds=num_folds, random_state=seed)
#     cv_results = cross_validation.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
#     results.append(cv_results)
#     names.append(name)
#     msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
#     print(msg)



















