import requests
import xml.etree.ElementTree as ET
import urllib
import re
from kivy.uix.image import Image
from kivy.uix.label import Label

APP_ID = "RRVHV2-QTHHW63Y8J"
def createPopupFromCommand(command, result):
    result[0] = getQueryFromCommand(command)
    print result[0]
    return
def getQueryFromCommand(command):
    match = re.match(r'(definition\sof|define|(?:image|picture)\sof|math)', command, re.I)
    if(match == None):
        return "Undefind command."
    cmd = match.group().lower()
    if(cmd == "definition of" or cmd == "define"):
        return getDefinition(command)
    elif(cmd == "image of" or cmd == "picture of"):
        return getImage(command)
    elif(cmd == "math"):
        return getMath(command)
    else:
        return "Failed."

def searchWolfram(query):
    link = []
    link.append("http://api.wolframalpha.com/v2/query?")
    query = urllib.urlencode({'input': query})
    link.append(query)
    link.append("&appid=")
    link.append(APP_ID)
    
    link = ''.join(link)
    r = requests.get(link)
    x = ET.ElementTree(ET.fromstring(r.text))
    return x

def getDefinition(query):
    match = re.match(r'(definition\sof|define)', query, re.I)
    if(match is None):
        return
    root = searchWolfram(query)
    for plaintext in root.iter('plaintext'):
        if(plaintext.text):
            return plaintext.text

def getImage(query):
    match = re.match(r'((?:image|picture)\sof)', query, re.I)
    if(match is None):
        return
    root = searchWolfram(query)
    i = 0
    for img in root.iter('img'):
        if(i == 0):
            i = i + 1
        else:
            if(img is not None):
                urllib.urlretrieve(img.attrib['src'], "1.png")
                i = i + 1
                return  "1.png"

def getMath(query):
    math = query.split(' ',1)[1]
    root = searchWolfram(math)
    for img in root.iter('img'):
        if(img is not None):
            urllib.urlretrieve(img.attrib['src'], "math.png")
            return "math.png"
        break

# 
# getQueryFromCommand("image of cow")
# getQueryFromCommand("define cow")
# getQueryFromCommand("math integrate 5x - 2y dx")