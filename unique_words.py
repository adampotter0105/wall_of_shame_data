# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 23:59:21 2022

@author: adamp
"""
# Load data
import json
data = [json.load(open('message_1.json', 'r'))]
data.append( json.load(open('message_2.json', 'r')) )
data.append( json.load(open('message_3.json', 'r')) )
data.append( json.load(open('message_4.json', 'r')) )
data.append( json.load(open('message_5.json', 'r')) )
data.append( json.load(open('message_6.json', 'r')) )

# COmpile all messages
msgs = []
for i in range(6):
    n = len(data[i]["messages"])
    for j in range(n):
        if "content" in data[i]["messages"][j].keys():
            msgs.append( [ data[i]["messages"][j]["sender_name"], data[i]["messages"][j]["content"]] )
            
names = ['Mindren Lu',
 'Adam Potter',
 'Alex Koenig',
 'Tamique De Brito',
 'Emily Wang',
 'Sreya Vangara',
 'Kat Hahn',
 'Paige Vincent',
 'Lilian Luong',
 'Patrick Kao',
 'Juliana Chew',
 'Michelle Yin',
 'Jeremy McCulloch',
 'Gloria Lin']

# Load msgs, names
all_words = dict()
people_words = dict();
for n in names:
    people_words[n] = dict()

# Find number of Words    
for i in range(len(msgs)):
    s = msgs[i][1].split()
    n = msgs[i][0]
    for w in s:
        if w not in all_words.keys():
            all_words[w] = 1
        else:
            all_words[w] += 1
        if w not in people_words[n].keys():
            people_words[n][w] = 1
        else:
            people_words[n][w] += 1
  
# Determine most unique words          
unique_words = []
second_most = []
num_ppl = len(names)
for n in names:
    most = 0
    best_word = ""
    sec = 0
    for w in people_words[n].keys():
        
        val = people_words[n][w]*(people_words[n][w] - (all_words[w]/num_ppl))/all_words[w]
        if people_words[n][w] == all_words[w]:
            val = 0
            
        if  val > most and len(w)>1:
            sec = best_word
            best_word = w
            most = val
            word = w
    unique_words.append(word)
    second_most.append(sec)
            
for i in range(num_ppl):
    print(names[i] + ": " + unique_words[i])
    
print("Second Most:")
for i in range(num_ppl):
    print(names[i] + ": " + second_most[i])