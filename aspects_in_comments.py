from __future__ import unicode_literals
from hazm import *
import re
import string
import nltk.data
import csv
comments=[]
pos_comments=[]
sent=[]
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

for i in range(len(pos_comments)): #sentence tokenize by V and aj label  
    a=0
    flag=False
    for j in range(len(pos_comments[i])):
        if pos_comments[i][j][1]=='V':
            s=''
            for k in range(a,j+1):
                if pos_comments[i][k][1]=='AJ':
                    flag=True
                    break    
            if flag==True:
                for k in range(a,j+1):
                    s=s+' '+pos_comments[i][k][0]
                flag=False
            sent.append(s)    
            a=j+1
            
def aspect_search(sent):
    #search the aspects in sentences.
    for j in range(len(aspects)):
        s=' '+aspects[j]+' '
        if re.search(s, sent):
            sent_aspect.append(sent)
            break
sent_aspect=[]
for i in range(len(sent)):
    aspect_search(sent[i])
    
# sent_aspect is first output.

#........
#aj = صفت
#adv = قید
pos_aspect=[]
for i in sent_aspect:
    pos_aspect.append(postagger(i))
all_terms=[]
for i in range(len(pos_aspect)):
    for j in range(len(pos_aspect[i])):
        if (pos_aspect[i][j][1]=='AJ' and pos_aspect[i][j-1][1]=='N'  and pos_aspect[i][j+1][1]=='V') or (pos_aspect[i][j][1]=='AJ' and pos_aspect[i][j-2][1]=='N' and pos_aspect[i][j-1][1]=='ADV' and pos_aspect[i][j+1][1]=='V'):
            s=''
            for k in range(len(pos_aspect[i])):
                s=s+' '+pos_aspect[i][k][0]
            all_terms.append(s)
            break
# all_terms is second 
#.......
terms=[]
for i in range(len(pos_aspect)):
    for j in range(len(pos_aspect[i])):
        if pos_aspect[i][j][1]=='AJ' and pos_aspect[i][j-1][1]=='N' and pos_aspect[i][j+1][1]=='V':
            terms.append( pos_aspect[i][j-1][0]+' '+ pos_aspect[i][j][0]+' ' +pos_aspect[i][j+1][0])
        if (pos_aspect[i][j][1]=='AJ' and pos_aspect[i][j-2][1]=='N' and pos_aspect[i][j-1][1]=='ADV' and pos_aspect[i][j+1][1]=='V'):
            terms.append(pos_aspect[i][j-2][0]+ ' '+pos_aspect[i][j-1][0] +' '+pos_aspect[i][j][0] +' '+ pos_aspect[i][j+1][0])
# terms is third        
