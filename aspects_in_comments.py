from __future__ import unicode_literals
from hazm import *
import re
import string
import nltk.data
import csv
comments=[]
pos_comments=[]
sent=[]
sent_aspect=[]

remove_digits = True
pattern = r'[^الف-ی آ-ی0-9\s]' if not remove_digits else r'[^الف-یآ-ی\s]'

with open('9k comments.csv','rt') as f:
        data = csv.reader(f)
        for row in data:
            comments.append(row)
            
with open('aspects.txt', 'r') as f:
    aspects = [i.rstrip() for i in f.readlines() ]
    f.close()
    
tagger = POSTagger(model='resources/postagger.model')
normalizer = Normalizer()

def normalize(comment):
    comment=str(comment)
    comment=re.sub(pattern, ' ', comment) #delete of english words , punctuations ,emoji , numbers ,etc ...
    comment=normalizer.normalize(comment) #normalize by hazm 
    return comment

def postagger(comment):
    return tagger.tag(word_tokenize(comment))

for i in range(len(comments)):
    comments[i]=normalize(comments[i])
    pos_comments.append(postagger(comments[i]))
    
for i in range(len(pos_comments)): #sentece tokenize by Verbs label 
    a=0
    for j in range(len(pos_comments[i])):
        if pos_comments[i][j][1]=='V':
            s=''
            for k in range(a,j+1):
                s=s+' '+pos_comments[i][k][0]
            sent.append(s)    
            a=j+1

for i in range(len(sent)): #search the aspects in sentences. 
    for j in range(len(aspects)):
        s=' '+aspects[j]+' '
        if re.search(s, sent[i]):
            sent_aspect.append(sent[i])
            break
len(sent_aspect)
