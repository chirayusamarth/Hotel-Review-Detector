import string, sys, re, math
from _collections import defaultdict

fModel= open('nbmodel.txt','w')

EntireVocab=set()
VocabCount=int(0)
docCount=int(0)

TruthfulPositiveDocCount=int(0)
DeceptivePositiveDocCount=int(0)
TruthfulNegativeDocCount=int(0)
DeceptiveNegativeDocCount=int(0)

TruthfulPositiveCount=int(0)
DeceptivePositiveCount=int(0)
TruthfulNegativeCount=int(0)
DeceptiveNegativeCount=int(0)

TruthfulPositiveDict=defaultdict(int)
DeceptivePositiveDict=defaultdict(int)
TruthfulNegativeDict=defaultdict(int)
DeceptiveNegativeDict=defaultdict(int)

stop_words = ['the', 'that', 'to', 'as', 'there', 'has', 'and', 'or', 'is', 'not', 'a', 'of', 'but', 'in', 'by', 'on', 'are', 'it', 'if', 'very', 'where', 'you',
'your', 'with', 'who', 'yet', 'why', 'whose', 'whom', 'we', 'were', 'was', 'us', 'until', 'while', 'under', 'than', 'thus', 'their', 'then', 'them', 
'such','still', 'so']


text={}
labels={}

trainingFile= sys.argv[-2]
labelsFile= sys.argv[-1]

fText= open(trainingFile,'r')
lines= fText.readlines()

#Remove punctuations, Make all the words lower-case and add words to vocab
#Add lines to Dictionary 'text'
for word in lines:
	key, word= word.strip().split(' ',1)
	for c in string.punctuation:
	  	word= word.replace(c,"")
	wordInLowerCase= word.split(' ')

	for w in wordInLowerCase:
		w= w.lower()
		if w.isalpha() and w not in EntireVocab and w not in stop_words:
			EntireVocab.add(w)
	text[key]= wordInLowerCase


#Add Labels to Dictionary 'labels'
fLabels= open(labelsFile,'r')
labelline= fLabels.readlines()
for l in labelline:
	key, l= l.strip().split(' ',1)
	labels[key]= l

for key in labels:
	if key in text.keys():
		if labels[key]=='truthful positive':
			TruthfulPositiveDocCount+=1
			for s in text[key]:
				TruthfulPositiveDict[s]+=1
				TruthfulPositiveCount+=1
		elif labels[key]=='truthful negative':
			TruthfulNegativeDocCount+=1
			for s in text[key]:
				TruthfulNegativeDict[s]+=1
				TruthfulNegativeCount+=1
		elif labels[key]=='deceptive positive':
			DeceptivePositiveDocCount+=1
			for s in text[key]:
				DeceptivePositiveDict[s]+=1
				DeceptivePositiveCount+=1
		elif labels[key]=='deceptive negative':
			DeceptiveNegativeDocCount+=1
			for s in text[key]:
				DeceptiveNegativeDict[s]+=1
				DeceptiveNegativeCount+=1

VocabCount= len(EntireVocab)


classes={
	'TruthfulPositive': (TruthfulPositiveCount, TruthfulPositiveDict, TruthfulPositiveDocCount),
	'TruthfulNegative': (TruthfulNegativeCount, TruthfulNegativeDict, TruthfulNegativeDocCount),
	'DeceptivePositive': (DeceptivePositiveCount, DeceptivePositiveDict, DeceptivePositiveDocCount),
	'DeceptiveNegative': (DeceptiveNegativeCount, DeceptiveNegativeDict, DeceptiveNegativeDocCount),
}

totalDocCount= TruthfulPositiveDocCount + TruthfulNegativeDocCount + DeceptivePositiveDocCount + DeceptiveNegativeDocCount

for className in classes:
	wordCount, dic, docCount= classes[className]
	prior= docCount/float(totalDocCount)
	print prior
	fModel.write(className+" "+str(prior)+"\n")

for className in classes:
	wordCount, dic, docCount= classes[className]
	for word in EntireVocab:
		if word in dic:
			condprob= (dic[word]+1)/float(VocabCount+wordCount)
		else:
			condprob= (1)/float(VocabCount+wordCount)
		fModel.write(className+" "+word+" "+str(condprob)+"\n")
