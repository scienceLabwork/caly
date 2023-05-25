import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from dateutil import parser
import datetime
import calendar
import json

nlp = en_core_web_sm.load()
today = datetime.date.today()
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
nn = datetime.datetime.now()

def nltoschedule(sent):
    doc = nlp(sent)

    def preprocess(sent):
        sent = nltk.word_tokenize(sent)
        sent = nltk.pos_tag(sent)
        return sent

    time = ""
    date = ""
    fdate = ""
    ftime = ""
    minlen = []

    for sen in doc.ents:
        if(sen.label_ == "CARDINAL"):
            time = sen.text
            minlen.append(sen.start_char)

        if(sen.label_ == "DATE"):
            date = sen.text
            if(date.lower()=="today"):
                date = today.strftime("%d %B %Y")
            elif(date.lower()=="tomorrow"):
                date = tomorrow.strftime("%d %B %Y")
            minlen.append(sen.start_char)

    for l in preprocess(sent):
        if(l[1]=="CD"):
            if(":" in l[0] and time==""):
                time = l[0]

    if minlen!=[]:
        newsent = sent[:min(minlen)]
    else:
        newsent = sent

    prepos = preprocess(newsent)
    prepos = prepos[::-1]

    i = 0
    l = []

    for x in prepos:
        if(i==0 and x[1]=='IN'):
            continue
        else:
            l.append(x[0])
        i+=1
    
    print(l)
    l = ' '.join(l[::-1])
    if(date+" "+time!=" "):
        whole = parser.parse(date+" "+time)
        fdate = str(whole.strftime("%d %a %b %Y"))
        ftime = str(whole.strftime("%I:%M %p"))

    return l,fdate,ftime