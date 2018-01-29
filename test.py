import json
from pprint import pprint
import urllib.request
import pickle
from xml.dom import minidom




########################This block is for error analysis########3
#load ground truth
data = json.load(open('/Users/fanision/Desktop/Thesis_Research/Text-Mining--BioCreativeVI/PMtask_Relations_TestSet.json'))


ground_truth={}
for i in data["documents"]:
	ground_truth[i["id"]]=[]
	for w in i["relations"]:
		ground_truth[i["id"]].append({w["infons"]["Gene1"],w["infons"]["Gene2"]})


with open("Bio_testing_predict_result.pickle",'rb') as f:
    predict_result = pickle.load(f)

with open("Bio_testing_predict_result_proba_1.pickle",'rb') as f:
    pos_predict_result = pickle.load(f)

with open("Bio_testing_predict_result_proba_0.pickle",'rb') as f:
    neg_predict_result = pickle.load(f)


for key,value in ground_truth.items():
	print("ground truth and prediction for {}".format(key))
	print(value)
	try:
		print("clf's positive predication is{}".format(pos_predict_result["d"+key]))
	except KeyError:
		print("there is no positive prediction in {}".format(key))
	try:
		print("clf's negtive predication is{}".format(neg_predict_result["d"+key]))
	except:
		print("there is no negtive prediction in {}".format(key))
	print("xxxxxxxxxxxxxxxxxxxxxxxx")
#################################################










# def mutation_finder(id):
# 	mutation_rec = set()
# 	url = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Mutation/"+id+"/json/"
# 	sock = urllib.request.urlopen(url) 
# 	htmlSource = sock.read  ()                            
# 	sock.close()
# 	d=json.loads(htmlSource)
# 	text = d["text"]
# 	ans = []
# 	for mutation in d["denotations"]:
# 		begin = mutation["span"]["begin"]
# 		end = mutation["span"]["end"]
# 		ans.append(text[begin:end])
# 	#print(ans)
# 	return ans




# xmldoc_AIMED = minidom.parse('Bio_testing.xml')
# predict_result_with_mutation = {}
# a=0
# for key,value in predict_result.items():
# 	print(key)
# 	temp = []
# 	mut = mutation_finder(key[1:])
# 	mut.append("mut")
# 	mut.append("Mut")
# 	for i in value:
# 		have = 0
# 		id = list(i)[0].split(".")[1]
# 		itemlist = xmldoc_AIMED.getElementsByTagName('sentence')
# 		for sentence in itemlist:
# 			if sentence.attributes["id"].value.split(".")[2]==id:
# 				sen = sentence.attributes['text'].value
# 		#print(sen)
# 		for m in mut:
# 			if m in sen:
# 				temp.append(i)
# 				break
# 	if temp==[]:
# 		predict_result_with_mutation[key]=value
# 	else:
# 		predict_result_with_mutation[key]=temp
# 	a+=1
# 	# if a==2:
# 	# 	break
# #print(predict_result_with_mutation)




# for key,value in predict_result.items():
# 	print(key)
# 	print(value)



# with open("Bio_testing_predict_result.pickle",'rb') as f:
#     predict_result = pickle.load(f)



# count=0
# modified_result = {}#make the format of dict like: 26101090:{7673;890}
# for key,value in predict_result.items():

# 	temp = []
# 	for i in value:
# 		pair = []
# 		a=list(i)
# 		for q in a:
# 			pair.append(q.split(".")[0])
# 		if set(pair) not in temp:
# 			temp.append(set(pair))
# 	count+=len(temp)
# 	modified_result[key[1:]]=temp



# remove_single={}
# single = 0
# for key,value in modified_result.items():
# 	temp=[]
# 	for i in value:
# 		if len(list(i))>1:
# 			temp.append(i)
# 	single+=len(temp)
# 	remove_single[key]=temp

# count=0
# for key,value in remove_single.items():
# 	count+=len(value)
# print(count)





# #load ground truth
# data = json.load(open('/Users/fanision/Desktop/Thesis_Research/Text-Mining--BioCreativeVI/PMtask_Relations_TestSet.json'))




# ground_truth={}
# for i in data["documents"]:
# 	ground_truth[i["id"]]=[]
# 	for w in i["relations"]:
# 		ground_truth[i["id"]].append({w["infons"]["Gene1"],w["infons"]["Gene2"]})


# #just add up all of predicted positive ones when there is a relation in the dict
# all_positive = 0
# for id,value in ground_truth.items():
# 	if len(value)>0:
# 		try:
# 			all_positive+=len(remove_single[id])
# 			# print(id)
# 			# print(ground_truth[id])
# 			# print(remove_single[id])
# 		except KeyError:
# 			continue
# #print(all_positive)








# TP=0
# for key,value in remove_single.items():
# 	print(key)
# 	print(ground_truth[key])
# 	print(value)
# 	for i in value:
# 		if i in ground_truth[key]:

# 			TP+=1




# print("xxxxxxxxxxxxxxxxxxx")
# print(TP)














