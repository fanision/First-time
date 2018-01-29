#from sklearn.feature_extraction.text import CountVectorizer
from xml.dom import minidom
import pickle


corpus = []
sen_dict = {}



xmldoc_AIMED = minidom.parse('Bio_training.xml')
itemlist = xmldoc_AIMED.getElementsByTagName('sentence')
for sentence in itemlist:
	corpus.append(sentence.attributes['text'].value)
	sen_dict["training"+"."+sentence.attributes['id'].value.split(".")[2]]=sentence.attributes['text'].value
xmldoc_AIMED = minidom.parse('Bio_testing.xml')
itemlist = xmldoc_AIMED.getElementsByTagName('sentence')
for sentence in itemlist:
	corpus.append(sentence.attributes['text'].value)
	sen_dict["testing"+"."+sentence.attributes['id'].value.split(".")[2]]=sentence.attributes['text'].value



vectorizer = CountVectorizer(stop_words="english")
vectorizer.fit(corpus)

with open('vectorizer.pickle', 'wb') as handle:
	pickle.dump(vectorizer,handle)

with open('sen_dict.pickle', 'wb') as handle:
	pickle.dump(sen_dict,handle)





with open("bioCreative_newmutation_training.pickle",'rb') as f:
    training_feature = pickle.load(f)
with open("bioCreative_newmutation_testing.pickle",'rb') as f:
    testing_feature = pickle.load(f)
for i in training_feature:
	sen = sen_dict.get("training"+"."+i.keys()[0].split(";")[0].split(".")[2])
	bow=vectorizer.transform(sen).todense()
	i[i.keys()[0]]=bow+i[i.keys()[0]]
	break




print(training_feature[0])










 
# vectorizer = CountVectorizer(stop_words="english")


# vectorizer.fit(corpus)
# print(vectorizer.transform(corpus).todense())
# print(vectorizer.vocabulary_)