from __future__ import unicode_literals
from hazm import *
import re
import string
import nltk.data
import csv
comments=[]
pos_comments=[]
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

with open('pos.txt', 'r') as f:
    pos = [i.rstrip() for i in f.readlines() ]
    f.close()
with open('neg.txt', 'r') as f:
    neg = [i.rstrip() for i in f.readlines() ]
    f.close()
with open('neutral.txt', 'r') as f:
    neutral = [i.rstrip() for i in f.readlines() ]
    f.close()

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

    
    
all_terms=[]
for i in range(len(pos_comments)):
    a=0
    for k in range(len(pos_comments[i])):
        if pos_comments[i][k][1]=='V':
            for j in range(a,k+1):
                if pos_comments[i][j][1] =='AJ' or pos_comments[i][j][1]=='AJe':
                    for j in range(a,k+1):
                        if pos_comments[i][j][0] in aspects:
                            s=''
                            for g in range(a,k+1):
                                s=s+' '+pos_comments[i][g][0]
                            all_terms.append(s)
                            a=k+1
                            break
            a=k+1                            

            
            
pos_all_terms=[]
for i in all_terms:
    pos_all_terms.append(postagger(i))

aj_list=[]
for i in range(len(pos_all_terms)):
    for j in range(len(pos_all_terms[i])):
        if pos_all_terms[i][j][1]=='AJ' or pos_all_terms[i][j][1]=='AJe':
            aj_list.append(pos_all_terms[i][j][0])
            
aj_freq=nltk.FreqDist(aj_list)
aj_most_common=aj_freq.most_common()

aj_unit=[]
for i in range(len(aj_most_common)):
    aj_unit.append(aj_most_common[i][0])

    
verb=[]
for i in range(len(pos_all_terms)):
    for j in range(len(pos_all_terms[i])):
        if pos_all_terms[i][j][1]=='V':
            verb.append(pos_all_terms[i][j][0])
verb_freq=nltk.FreqDist(verb)
verb_most_common=verb_freq.most_common()

verb_neg=[]
pat=r'^ن'
for i in range(len(verb_most_common)):
        a=re.match(pat,verb_most_common[i][0])
        if a:
            verb_neg.append(verb_most_common[i][0])
verb_check=[0]*len(all_terms)
check=0
for i in range(len(all_terms)):
    for j in verb_neg:
        if j in all_terms[i]:
            check=1
            break
    verb_check[i]=check
    check=0
    
    
noaj=[i for i in aj_unit if i not in pos and i not in neg and  i not in neutral]    
# شمارش صفات مثبت و منفی هر جمله
aj_count=[]
pos_count=0
neg_count=0
neutral_count=0
noaj_count=0
for i in range(len(pos_all_terms)):
    for j in range(len(pos_all_terms[i])):
        if pos_all_terms[i][j][1]=='AJ' or pos_all_terms[i][j][1]=='AJe':
            if pos_all_terms[i][j][0] in pos:
                pos_count=pos_count+1
            elif pos_all_terms[i][j][0] in neg:
                neg_count=neg_count+1
            elif pos_all_terms[i][j][0] in neutral:
                neutral_count=neutral_count+1
            elif pos_all_terms[i][j][0] in noaj:
                noaj_count=noaj_count+1
    aj_count.append([[i],
                     ['verb:',verb_check[i]],
                     ['pos:',pos_count],
                     ['neg:',neg_count],
                     ['neutral:',neutral_count],
                     ['noaj:',noaj_count]])
    pos_count=0
    neg_count=0
    neutral_count=0
    noaj_count=0
    
    
# تصمیم برای مثبت یا منفی کردن جمله
for i in range(len(aj_count)):
    if aj_count[i][2][1]!=0 and aj_count[i][3][1]==0:
        if aj_count[i][1][1]==1:
            aj_count[i].append('neg')
        elif aj_count[i][1][1]==0:
            aj_count[i].append('pos')
    elif aj_count[i][2][1]==0 and aj_count[i][3][1]!=0:
        if aj_count[i][1][1]==1:
            aj_count[i].append('pos')
        elif aj_count[i][1][1]==0:
            aj_count[i].append('neg')
    else:
        aj_count[i].append('None')
        
for i in range(len(all_terms)):
    all_terms[i]=[all_terms[i],aj_count[i][6]]

    
for i in [i for i in all_terms if 'کیفیت' in i[0] and 'بالا' in i[0] and i[1]=='None']:
    i[1]='pos'
for i in [i for i in all_terms if 'قیمت' in i[0] and 'افزایش' in i[0] and i[1]=='None']:
    i[1]='neg'
for i in [i for i in all_terms if 'قیمت' in i[0] and 'بالا' in i[0] and i[1]=='None']:
    i[1]='neg'
for i in [i for i in all_terms if 'قیمت' in i[0] and 'زیاد' in i[0] and i[1]=='None']:
    i[1]='neg'
    
# درآوردن صفات و جنبه های هر جمله برای ارزیابی
def aj_aspect(comment,ind):
    aj=[]
    aspect=[]
    comment_pos=postagger(comment[0])
    if comment[1]=='pos' or comment[1]=='neg' or comment[1]=='ntr':
        for i in range(len(comment_pos)):
            if comment_pos[i][0] in aspects:
                aspect.append(comment_pos[i][0])
            if comment_pos[i][1] =='AJ' or comment_pos[i][1]=='AJe':
                aj.append(comment_pos[i][0])
    return (comment[1] , aj,aspect,ind)


all_terms=[i for i in all_terms if i[1]!='None']

arzyabi=[]
for i in range(len(all_terms)):
    arzyabi.append(aj_aspect(all_terms[i],i))

    
for i in all_terms:
    if i[1]=='pos':
        i[1]=1
    elif i[1]=='neg':
        i[1]=0
        
#-------model--------------
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import numpy as np
from keras.models import Sequential
from keras.layers import Flatten, Dense
from keras.layers import Embedding
from keras.layers import LSTM

bar=[i[1] for i in all_terms]
data=[i[0] for i in all_terms]
maxlen=10
max_word=500
tokenize=Tokenizer(num_words=max_word)
tokenize.fit_on_texts(data)
sequence=tokenize.texts_to_sequences(data)
data = pad_sequences(sequence, maxlen=maxlen)

x_train,x_test,y_train,y_test=train_test_split(data,bar,test_size=0.3,random_state=15,shuffle=True)

model = Sequential()
model.add(Embedding(max_word, 64, input_length=maxlen))
model.add(LSTM(32))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
model.summary()

history = model.fit(x_train, y_train,epochs=10,batch_size=32,validation_split=0.2)

a=['غذا افتضاح رستوران افتضاح ولی فضا خوب بود']
sequence=tokenize.texts_to_sequences(a)
x_test_input = pad_sequences(sequence, maxlen=maxlen)
model.predict_classes(x_test_input)
