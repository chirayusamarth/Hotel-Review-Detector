import string, sys, math, operator, re
from _collections import defaultdict

EntireVocab=set()
VocabCount=int(0)

TruthfulPositiveDict=defaultdict(int)
DeceptivePositiveDict=defaultdict(int)
TruthfulNegativeDict=defaultdict(int)
DeceptiveNegativeDict=defaultdict(int)

ConditionalProb={
	'TruthfulPositive': TruthfulPositiveDict,
	'TruthfulNegative': TruthfulNegativeDict,
	'DeceptivePositive': DeceptivePositiveDict,
	'DeceptiveNegative': DeceptiveNegativeDict
}

classes=['TruthfulPositive', 'TruthfulNegative', 'DeceptivePositive', 'DeceptiveNegative']

fOutput= open('nboutput.txt','w')
fModel= open('nbmodel.txt','r')
#lines= fModel.readlines()
prior={}

firstFourLines= fModel.readlines()[0:4]
for l in firstFourLines:
	c, prob= l.split()
	c= c.strip()
	prob= prob.strip()
	prior[c]= float(prob)
	print c, prior[c]
fModel.close()


fModel= open('nbmodel.txt','r')
lines= fModel.readlines()[5:]
for l in lines:
	className, word, condprob= l.split()
	className= className.strip()
	word= word.strip()
	condprob= condprob.strip()
	EntireVocab.add(word)
	ConditionalProb[className][word]= float(condprob)

finalProb = {
		'TruthfulPositive': float((0.0)),
		'TruthfulNegative': float(0.0),
		'DeceptivePositive': float(0.0),
		'DeceptiveNegative': float(0.0),
		}

testFile= sys.argv[-1]
fTest= open(testFile,'r')
testLines= fTest.readlines()
for line in testLines:
	for c in string.punctuation:
		line= line.replace(c,"")
	key, line= line.strip().split(' ',1)
	line= line.split(' ')
	for c in classes:
		finalProb[c]= math.log(prior[c])
		for word in line:
			word=word.lower()
			if word in EntireVocab:
				finalProb[c]+=math.log(ConditionalProb[c][word])
	className=max(finalProb.iteritems(),key=operator.itemgetter(1))[0]

	if className=='TruthfulPositive':
		fOutput.write(key+" truthful positive"+"\n")
	elif className=='TruthfulNegative':
		fOutput.write(key+" truthful negative"+"\n")
	elif className=='DeceptivePositive':
		fOutput.write(key+" deceptive positive"+"\n")
	elif className=='DeceptiveNegative':
		fOutput.write(key+" deceptive negative"+"\n")