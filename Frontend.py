#Python Program to search string in text usin Tkinter
import glob
import os
import nltk
from nltk.stem import PorterStemmer
import numpy as np
from tkinter import *


dicsw={} # Dictionary without stop words
dic={}  #Dictionary with stop words
############################### Stop word list ####################################
def swl():   
    fObj = open('Stopword-List.txt',mode='r',encoding='utf-8')
    SwContent = fObj.readlines()
    swlist = [x.replace("\n","").replace(" ","") for x in SwContent]
    stwl = [x for x in swlist if x!=""]
    return stwl
###################################################################################

############################## Dictionary Creation ################################
def dictionary_creation(): 
    files = glob.glob('Stories/*') 
    for x in files:
        
        porter = PorterStemmer()
        obj = open(x,mode='r',encoding='utf-8')
        # read file and removing punctuations
        fullfile=obj.read().replace("'ve"," have").replace("'m"," am").replace("'re"," are").replace("'d"," would").replace("'ll"," will").replace("'s"," is").replace("'\'"," ").replace("_"," ").replace("."," ").replace("n't"," not").replace("'","").replace("]"," ").replace("["," ").replace(","," ").replace("?"," ").replace("\n"," ").replace("-"," ").split() 

        # stemming and lower case conversion
        lowCase=[porter.stem(x.lower()) for x in fullfile]
        
        #removing stop words
        stoplist = [x for x in lowCase if x not in swl()]
        
        #trimming the file name and removing redundant '.txt'
        #dicsw is dictionary per doc id  
        p=os.path.basename(x)
        p=p.split('.')[0]
        dic[p]=lowCase
        dicsw[p]=stoplist  
#print(dicsw.items())
#print(dicsw.keys())
#print(dic.items)
##################################################################################

############################ Inverted Index Creation #############################
def inverted_index():
    i_index={}
    for key in dicsw.keys():
        for word in set(dicsw[key]):
            if word not in i_index:
                i_index[word]=[]
                i_index[word].append(key)
            else:
                i_index[word].append(key)
    return i_index

##################################################################################

############################# Positional Index Creation ##########################
def positional_index():
    p_index={}
    for key in dic.keys():
        count=0
        for word in dic[key]:
            count+=1
            if word in swl():  # entertaining the presence of stop words in the file (increment index without doing anything)
                continue
            if word not in p_index:
                p_index[word]={}
                p_index[word][key]=[]
                p_index[word][key].append(count)
            else:
                if key not in p_index[word]:
                    p_index[word][key]=[]
                p_index[word][key].append(count)
    return p_index        

#################################Query Processing#################################
def query_processing(query):
    porter = PorterStemmer
    query = query.replace(".","").replace("n't"," not").replace("]"," ").replace("["," ").replace(","," ").replace("?","").replace("/"," / ").split()
    query = [porter.stem(x.lower()) for x in query]
    querysw = [x for x in query if x not in swl()]
    return querysw
##################################################################################
def find(st,Q):
    st = Q
    return st
#############################FrontEnd################################
root = Tk()
root.resizable(0,0)
fram = Frame(root)
Label(fram,text='Search:').pack(side=LEFT)
string = Entry(fram)
string.pack(side=LEFT, fill=BOTH, expand=1)
string.focus_set()
query = string.get()
Q = query_processing(query)
butt = Button(fram, text='GO!')
butt.pack(side=RIGHT)
fram.pack(side=TOP)

dictionary_creation()
st = "asd"
butt.config(command=find(st,Q))
text = Text(root)
text.insert('1.0',st)
text.pack(side=BOTTOM)


root.mainloop()
  
  
  