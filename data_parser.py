# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 20:12:26 2022

@author: adamp
"""
from datetime import datetime
from matplotlib import pyplot as plt

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
reacts = []
for i in range(6):
    n = len(data[i]["messages"])
    for j in range(n):
        if "content" in data[i]["messages"][j].keys():
            time_stamp = datetime.fromtimestamp(data[i]["messages"][j]["timestamp_ms"] // 1000)
            msgs.append( [ data[i]["messages"][j]["sender_name"], data[i]["messages"][j]["content"], time_stamp] )
        if "reactions" in data[i]["messages"][j].keys():
            for r in data[i]["messages"][j]["reactions"]:
                reacts.append(r)


quotes = []
people = dict()
for i in range(len(msgs)):
    # People
    if msgs[i][0] in people.keys():
        people[msgs[i][0]].append(msgs[i][1])
    else:
        people[msgs[i][0]] = [msgs[i][1]]
    # Quotes
    if  msgs[i][1][0] == '"' and len(msgs[i][1])<200: # and "-" in msgs[i][1]
        quotes.append( msgs[i][0] + "(" + msgs[i][2].strftime('%Y-%m-%d') + ") " + msgs[i][1])
        """
        # Messages after
        adj_i = 1
        while abs( (msgs[i][2]-msgs[i+adj_i][2]).total_seconds() ) < 60: # 1 minute window
            quotes.append(msgs[i+adj_i])
            adj_i += 1
        # Messages before
        adj_i = 1
        while abs( (msgs[i][2]-msgs[i-adj_i][2]).total_seconds() ) < 180: # 3 minute window
            quotes.append(msgs[i-adj_i])
            adj_i -= 1
        """
   
# Reacts
ppl_reacts = dict()
for r in reacts:
    if r["actor"] not in ppl_reacts.keys():
        ppl_reacts[r["actor"]] = dict()
    if r["reaction"] not in ppl_reacts[r["actor"]].keys():
        ppl_reacts[r["actor"]][r["reaction"]] = 1
    else:
        ppl_reacts[r["actor"]][r["reaction"]] += 1
        
react_key = { 'ð\x9f\x98\x86' : "laugh", 'ð\x9f\x92\x97' : "beating heart", 'ð\x9f\x98®' : 
             "wow", 'ð\x9f\x91\x8d': "thumbs up",  'â\x9d¤' : "heart",  'ð\x9f\x98¢' : "sad", 'ð\x9f\x98\xa0' : "angry", 'ð\x9f\x91\x8e': "thumbs down"}

# Decode the Reacts
reacts_decoded = dict()    
for n in ppl_reacts.keys():
    reacts_decoded[n] = dict()
    for r in ppl_reacts[n].keys():
        if r in react_key.keys():
            reacts_decoded[n][react_key[r]] = ppl_reacts[n][r]
 
reacts_norm = reacts_decoded.copy()
for n in reacts_decoded.keys():
    total = sum(reacts_decoded[n].values())
    for r in reacts_decoded[n].keys():
        reacts_norm[n][r] /= total   
        
def most_react(react):
    most = 0
    name = ''
    for n in reacts_norm.keys():
        if react in reacts_norm[n].keys():
            if reacts_norm[n][react] > most:
                most = reacts_norm[n][react]
                name = n
    return name

# Finding Most Talkative Mmebers
talkative = []
names = list(people.keys())
for n in names:
    talkative.append(len(people[n]))
 
ordering = []
ordered = []
s = sorted(talkative)
while len(ordering) < len(names):
    for i in range(len(talkative)):
        if talkative[i] == s[len(s)-1]:
            ordered.append(talkative[i])
            ordering.append(i)
            s.pop()
            break


# Pie Chart of Pos Frequency
plt.pie(ordered, labels = [names[i] for i in ordering], labeldistance = 1.2)  


# Calculate Gini Coefficient
gini = 0
gini_data = []
l = len(names)
for i in range(l):
    gini += (1/l)* (sum(ordered[l-i-1:l]) / sum(ordered) )
    gini_data.append(sum(ordered[l-i-1:l]) / sum(ordered) )
gini = 1 - 2*gini
 # this would be the 5th most unequal country on earth


# times * deviation from mean
"""
file1 = open("messages.txt", "w")
file1.writelines(str(msgs))
file1.close()

file2 = open("reacts.txt", "w") 
file2.writelines(str(reacts_decoded))
file2.close() 
"""
file3 = open("quotes.txt", "w") 
for q in quotes:
    try:
        file3.write(str(q)+"\n")
    except:
        print(q)
file3.close() 
"""
Ideas:
Distribution of words for each person (and most unique) (normalize by total words)
Most common react for each person
Person posts over time
Who gives the most love (heart reac) and most hate (angry)

"""