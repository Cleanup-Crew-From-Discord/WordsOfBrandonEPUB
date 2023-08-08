from html.parser import HTMLParser
import os
import io
import re

root=os.path.dirname(__file__)

tempArr=[]
authArr=[]
ts = io.StringIO()
pstate=False
author=""
authState=False
hstate=False
infstate=False

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        global pstate
        global authState
        global infstate
        global author
        if tag=="p": #this is a sign that data will start
            pstate=True
            authState=False
            infstate=False

        elif tag=="h4": #this is a sign that author name will start
            authState=True
            pstate=False
            infstate=False

        elif tag=="td":
            authState=False
            pstate=False
            infstate=True


    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        global pstate
        global prevBody
        global authState
        global author
        if pstate:
            tempArr.append((author.strip(),ts.getvalue()))
            author=""
        ts.seek(0)
        ts.truncate()
        pstate=False
        authState=False
        prevBody=True

    def handle_data(self, data):
        #print("Encountered data :", data)
        global pstate
        global author
        global infstate
        global authArr
        if pstate:
            ts.write(f"{data}")
        elif authState:
            author += f"{data} "
        elif infstate:
            authArr.append(data)


parser = MyHTMLParser()
for file in os.listdir(os.path.join(root,"html")):
    if not file.endswith("py"):
        tempArr=[] #empty temparr
        authArr=[] #empty authArr
        outArr=[]
        with open(os.path.join(root,"html",file), 'r') as toRead:
            for line in toRead:
                if "entry-content" in line:
                    tempArr.append(("!!linebreaker",""))
                else:
                    parser.feed(line.strip())

        skipcount=0
        for index in range(0,len(authArr)):
            if skipcount==0:
                if authArr[index] == "Name":
                    outArr.append(authArr[index+2])
                    skipcount=2
                elif authArr[index] == "Date":
                    outArr.append(authArr[index+2])
                    skipcount=2
            else:
                skipcount-=1

        date = re.sub(r'[^a-zA-Z0-9 ]', '', outArr[1])
        eventName = re.sub(r'[^a-zA-Z0-9 ]', '', outArr[0])
        fname=f"{date}_{eventName}.html"
        fname.strip("&").strip(".")
        queueLine=False
        with open(os.path.join(root,"text",fname),'w+') as toWrite:
            toWrite.write('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n<html lang="en-us" xmlns="http://www.w3.org/1999/xhtml">\n<head><title></title></head>\n<body>\n<p>')
            toWrite.write(f'<center><big><big><b>{eventName}</b></big></big></center>\n')
            toWrite.write(f'<center><big><b>{date}</b></big></center>\n')
            spacer=True
            for item in tempArr:
                q,a=item
                q.strip(">").strip("<")
                a.strip(">").strip("<")
                a = re.sub('\*start\*','<i>',a)
                a = re.sub('\*end\*','</i>',a)
                q = re.sub('\*start\*','<i>',q)
                q = re.sub('\*end\*','</i>',q)
                if q=='': #if this is a continuation of an author's sentence, write just it as a same line
                    toWrite.write(f" {a}")
                else:
                    if q=="!!linebreaker":
                        toWrite.write("</p>\n\n<center>***</center>\n<p>")
                    else:
                        toWrite.write(f"\n</p><p>\n<b>{q}:</b> {a}")
                    #if "brandon sanderson" in q.lower():
                    #    queueLine=True
                    #else:
                        toWrite.write("\n")
            toWrite.write('</p>\n<center>***</center>\n</body>\n</html>')