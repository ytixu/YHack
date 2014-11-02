# -*- coding: utf-8 -*-
import requests
import urllib
import re

from lxml import etree
from kivy.uix.image import Image
from kivy.uix.label import Label

APP_ID = "RRVHV2-QTHHW63Y8J"

def createPopupFromCommand(command, result):
    result[0] = getQueryFromCommand(command)
    return
def getQueryFromCommand(command):
    match = re.match(r'(definition\sof|define|(?:image|picture)\sof|math\s(:?graph|plot)|math)', command, re.I)
    if(match == None):
        return "Undefind command."
    cmd = match.group().lower()
    if(cmd == "definition of" or cmd == "define"):
        return getDefinition(command)
    elif(cmd == "image of" or cmd == "picture of"):
        return getImage(command)
    elif(cmd == "math graph" or cmd == "math plot"):
        return getImage(command.split(" ",1)[1])
    elif(cmd == "math"):
        return getMathRepresentation(command)
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
    return etree.fromstring(r.content)

def getDefinition(query):
    root = searchWolfram(query)
    partial_result = ''
    for plaintext in root.iter('plaintext'):
        if(plaintext.text):
            partial_result += ('\n' + plaintext.text)
    return partial_result


def getImage(query):
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

def getMathRepresentation(query):
    math = query.split(' ',1)[1]
    root = searchWolfram(math)
    for img in root.iter('img'):
        if(img is not None):
            urllib.urlretrieve(img.attrib['src'], "math.png")
            return "math.png"
        break