import glob
import os
import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer 
import math
from scipy import spatial


lemmatizer = WordNetLemmatizer()
dic={}
p_index={}
term_count_in_each_doc={}
wfreq={}
doclist=[]
tfidf={}
stwl = {}



def Readstopwords():
    global stwl
    fObj = open('Stopword-List.txt',mode='r',encoding='utf-8')
    stwl = fObj.read()
    stwl = stwl.split()
    
    files = glob.glob('ShortStories/*')  #to read file names for doc id
    for i in files:
        p=os.path.basename(i)
        p=p.split('.')[0]
        doclist.append(int(p))
    #Creating a list of documents
    doclist.sort()

    
def RemovePun(text):
    return text.translate({ord(i): "" for i in "!@#$%^&*()[]{};:,./<>?\"'|——`~-=_’+”“"})


def ReadFiles():
    
    for x in doclist:
        obj = open("ShortStories/"+str(x)+".txt",mode='r',encoding='utf-8').read()
        fullfile = RemovePun(obj.lower())
        fullfile = fullfile.split()
        # file path names to use as doc id
        temp = []
        for word in fullfile:
            if word not in stwl:
                temp.append(lemmatizer.lemmatize(word))
        dic[x]=temp


def calpindex():
    for x in dic.keys():
        for words in dic[x]:
            if words not in wfreq:
                wfreq[words] = {}
                wfreq[words]['df'] = 1
                wfreq[words][x] = dic[x].count(words)
            elif x not in wfreq[words]:
                wfreq[words][x] = dic[x].count(words)
                wfreq[words]['df'] += 1
    p_file = open("wfreq.txt",mode='w',encoding='utf-8')   
    p_file.write(json.dumps(wfreq))     
        
    
    
def DocVec():
    for words in wfreq.keys():
        idf = math.log10(wfreq[words]['df'])/len(doclist)
        for ids in doclist:
            if ids not in tfidf.keys():
                tfidf[ids] = []
            tfid = idf * wfreq[words].get(ids,0)  
            tfidf[ids].append(round(tfid,6))
                      
    t_file = open("TFIDF.txt",mode='w',encoding='utf-8')  
    t_file.write(json.dumps(tfidf))        
       
       
def Readtfidf():
    global wfreq , tfidf
    try:

        T_file = open("TFIDF.txt",mode='rb')
        F_file = open("wfreq.txt",mode='rb')
        T_index = json.loads(T_file.read())
        F_index = json.loads(F_file.read()) 
        if len(T_index) == 0 or len(F_index) == 0:
            ReadFiles()
            calpindex()
            DocVec()
        else:
            tfidf = T_index.split()
            wfreq = F_file.split() 
    except:
        ReadFiles()
        calpindex() 
        DocVec()

  
     
def CosineSimilarity(queryVec,c):
    cosineVector={}
    for i in tfidf.keys():
        result = round(1 - spatial.distance.cosine(tfidf[i], queryVec),3)
        cosineVector[i]=result
        
    counter=1
    for i in cosineVector:
        if(cosineVector[i] > c):
            print(counter,"----> Doc",i," ---->",cosineVector[i])
            counter=counter+1   
    print("Length: ", counter -1)
 
     
def Query():

    search = input("Enter the query: ")
    alpha = float(input("Enter the cutoff value : ")) 
    search = RemovePun(search.lower()).split()
    query = []
    queryVec = []

    for words in search:
        if words not in stwl:
            query.append(lemmatizer.lemmatize(words))            
    print(query)
    
    for words in wfreq.keys():
        widf = query.count(words) * math.log10(wfreq[words].get('df',0))/len(doclist)
        queryVec.append(round(widf,6))                   
    CosineSimilarity(queryVec,alpha) 
                
def main():
    Readstopwords()
    ReadFiles()
    calpindex()
    DocVec()
    while 1:
        Query()   
        
main()