# Opens random wikipedia article and you have to guess the topic
from urllib.request import urlopen
from bs4 import BeautifulSoup
import textwrap
from tkinter import*
import os

bracketCount = 0
bracketCount2 = 0
titleCount = 0
guessCount = 0

wikiRand = urlopen('https://en.wikipedia.org/wiki/Special:Random')
wikiBs = BeautifulSoup(wikiRand.read(), "html.parser")

#Title of the wikipedia article
title = str(wikiBs.h1)
#Body of the wiki article
body = str(wikiBs.p)

root = Tk()


for i in range(len(body)):
    if(body[i] == '<'):
        bracketCount += 1
for i in range(len(body)):
    if(body[i] == '['):
        bracketCount2 += 1
# Get title from html header
def getTitle(t):
    for i in range(len(t)):
        if(t[i] == '>'):
            t = t[i+1:len(t)]
            break
    for i in range(len(t)):
        if(t[i] == '<'):
            t = t[0:i]
            break
    for i in range(len(t)):
        if(t[i] == '('):
            t = t[0:i]
            break
    return t
def callback():
    global guessCount
    guessCount += 1
    answer = answerInput.get()
    for i in range(len(titleList)):
        if(titleList[i] == answer):
            answerLabel.config(text='Correct')
            os.execl(sys.executable, sys.executable, *sys.argv)
        elif(guessCount == 5):
            answerLabel.config(text=title)
        elif(guessCount >= 6):
            answerLabel.config(text=title)
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
             answerLabel.config(text='Wrong')
    
        
# Parses through the text and only keeps what is not surrounded in brackets
def getBody(b):
    beforeBracket = ''
    afterBracket = ''
    for i in range(len(b)):
        if(b[i] == '<'):
            beforeBracket = b[0:i]
            for j in range(len(b)+i):
                if(b[j+i] == '>'):
                    afterBracket = b[j+i+1:len(b)]
                    break
            break
    return beforeBracket+afterBracket
# Removes square brackets
def getBody2(b):
    beforeBracket = ''
    afterBracket = ''
    for i in range(len(b)):
        if(b[i] == '['):
            beforeBracket = b[0:i]
            for j in range(len(b)+i):
                if(b[j+i] == ']'):
                    afterBracket = b[j+i+1:len(b)]
                    break
            break
    return beforeBracket+afterBracket
    
#Removes title from the body text
def removeTitleFromBody(tList,b):
    before = ''
    after = ''
    for i in range(len(b)):
        for j in range(len(tList)):
            if(tList[j] == b[i:i+len(tList[j])]):      
                before = b[0:i]
                after = b[i+1+len(tList[j]):len(b)]
                return before + '_'*len(tList[j])+after
                    
    
#Title of article
title = getTitle(title)
#If title has spaces split it into separate words
titleList = title.split()
#If it has no title reset
if(len(titleList) == 0):
    os.execl(sys.executable, sys.executable, *sys.argv)

#remove html from body
for i in range(bracketCount):  
    body = getBody(body)
for i in range(bracketCount2):  
    body = getBody2(body)

for i in range(len(body)):
    for j in range(len(titleList)):
        if(titleList[j] == body[i:i+len(titleList[j])]):
            titleCount += 1
            
#remove strings in titleList from the body paragraph
for i in range(titleCount):
    body = removeTitleFromBody(titleList, body)


guessCount = 0
#UI
bodyLabel = Label(root, text=textwrap.fill(body,80))
guessLabel = Label(root, text='Guess topic')
answerInput = Entry(root)
answerButton = Button(root, text='OK',command=callback)
answerLabel = Label(root, text='?')

#Packs UI elements
bodyLabel.pack()
guessLabel.pack()
answerInput.pack()
answerButton.pack()
answerLabel.pack()
root.mainloop()
guessCount = 0



        
    


    

