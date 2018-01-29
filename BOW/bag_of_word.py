from sklearn.feature_extraction.text import CountVectorizer
from xml.dom import minidom
import pickle



#training BOW model
corpus = []
sen_dict = {}


xmldoc_AIMED = minidom.parse('Bio_training.xml')
itemlist = xmldoc_AIMED.getElementsByTagName('sentence')
for sentence in itemlist:
    #print(sentence.attributes['id'].value)
    corpus.append(sentence.attributes['text'].value)
    sen_dict["training"+"."+sentence.attributes['id'].value.split(".")[2]]=sentence.attributes['text'].value
xmldoc_AIMED = minidom.parse('Bio_testing.xml')
itemlist = xmldoc_AIMED.getElementsByTagName('sentence')
for sentence in itemlist:
    #print(sentence.attributes['id'].value)
    corpus.append(sentence.attributes['text'].value)
    sen_dict["testing"+"."+sentence.attributes['id'].value.split(".")[2]]=sentence.attributes['text'].value


vectorizer = CountVectorizer(stop_words="english")
vectorizer.fit(corpus)







with open("bioCreative_newmutation_training.pickle",'rb') as f:
        training_feature = pickle.load(f)
with open("bioCreative_newmutation_testing.pickle",'rb') as f:
        testing_feature = pickle.load(f)





#normalization
normalized_training_feature=[]
max_vec=[0,0,0,0,0,0,0,0,0,0]


for i in testing_feature:
    for key,value in i.items():
        for i in range(len(max_vec)):
            if value[i]>max_vec[i]:
                max_vec[i]=value[i]

for i in testing_feature:
    for key,value in i.items():
        for i in range(len(max_vec)):
            if value[i]>max_vec[i]:
                max_vec[i]=value[i]



normalized_training_feature=[]
normalized_testing_feature=[]
for i in training_feature:
    temp={}
    for key,value in i.items():
        for v in range(len(value)):
            if max_vec[v]!=0:
                value[v]/=max_vec[v]
    temp[key]=value
    normalized_training_feature.append(temp)

for i in testing_feature:
    temp={}
    for key,value in i.items():
        for v in range(len(value)):
            if max_vec[v]!=0:
                value[v]/=max_vec[v]
    temp[key]=value
    normalized_testing_feature.append(temp)
# print(normalized_training_feature[0])
# print(normalized_testing_feature[0])







# adding bow vectors to original feature vectors
# bow is at the very beginning of the feature vector


normalized_training_feature_with_bow=[]
for i in normalized_training_feature:
    temp={}
    sen = sen_dict.get("training"+"."+list(i.keys())[0].split(";")[0].split(".")[2],"default value")
    bow=vectorizer.transform([sen])
    for key,value in i.items():
        temp[key]=list(bow.toarray()[0])+value
        print(key)
    normalized_training_feature_with_bow.append(temp)
print("############################## training is done#############################")
#print(normalized_training_feature_with_bow[9].keys())
#print(len(list(normalized_training_feature_with_bow[0].values())[0]))
#The length of whole vetor is 20274



normalized_testing_feature_with_bow=[]
for i in normalized_testing_feature:
    temp={}
    sen = sen_dict.get("testing"+"."+list(i.keys())[0].split(";")[0].split(".")[2],"default value")
    bow=vectorizer.transform([sen])
    for key,value in i.items():
        temp[key]=list(bow.toarray()[0])+value
        print(key)
    normalized_testing_feature_with_bow.append(temp)
print("#############testing is done")





# with open('normalized_training_feature_with_bow.pickle', 'wb') as handle:
#   pickle.dump(normalized_training_feature_with_bow,handle)

# with open('normalized_testing_feature_with_bow.pickle', 'wb') as handle:
#   pickle.dump(normalized_testing_feature_with_bow,handle)




print("starting ML Moudle")
##### starts with ML model training#########
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


print("is spliting training dataset")


training_list_group1234=[]



training_data=normalized_training_feature_with_bow

for data in training_data:
        for key,value in data.items():
            training_list_group1234.append(value)





print("is training model")


X=[]
Y=[]
for i in training_list_group1234:
        X.append(i[0:20273])
        Y.append(i[20273])
#cls is classifier
clf = SVC()
clf.fit(X,Y)


print("begin to predict")
test_data=normalized_testing_feature_with_bow

predict_result={}
cc=0
for data in test_data:
        for m,n in data.items():
            print("is predicting"+str(m))
                #if n[0]!=4: 
            if clf.predict([n[0:20273]])[0]==1:
                a=m.split(";")
                article_id = a[0].split(".")[1]
                pro_entity1=a[0].split(".")[0]+"."+a[0].split(".")[2]
                pro_entity2=a[1].split(".")[0]+"."+a[1].split(".")[2]
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

with open('Bio_testing_with_BOW_predict_result.pickle', 'wb') as handle:
        pickle.dump(predict_result,handle)















 
