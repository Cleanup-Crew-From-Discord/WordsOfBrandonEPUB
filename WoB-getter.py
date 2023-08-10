import os
import io
import re
import urllib3
import calendar
import zipfile
from filecmp import cmp
from datetime import date

import sys

root=os.path.dirname(__file__)
#ebook metadata generation code
def generateImportantFiles(readDir,writeDir):
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    nextDict={}
    with open(os.path.join(writeDir,"toc.ncx"),'w') as ToC:
        n=1
        ToC.write('<?xml version=\'1.0\' encoding=\'utf-8\'?> <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="eng"> <head> <meta content="fa10ed69-1e99-41b6-a80d-2d1ce2f9a2ad" name="dtb:uid"/> <meta content="3" name="dtb:depth"/> <meta content="calibre (4.12.0)" name="dtb:generator"/> <meta content="0" name="dtb:totalPageCount"/> <meta content="0" name="dtb:maxPageNumber"/> </head> <docTitle> <text>The Stormlight Archive 02 - Words of Radiance</text> </docTitle><navMap>\n')
        for file in os.listdir(readDir):
            if file.endswith(".html"):
                title=""
                with open(os.path.join(readDir,file.replace("html","txt")),'r') as textFile:
                    title=textFile.readline().strip()
                os.remove(os.path.join(readDir,file.replace("html","txt")))
                ToC.write(f'<navPoint class="chapter" id="np_{n}" playOrder="{n}"><navLabel><text>{title}</text></navLabel><content src="Text/{file}"/></navPoint>\n')
                nextDict[n]=((title,file))
                n+=1
        ToC.write('</navMap></ncx>\n')

    with open(os.path.join(writeDir,"TOC.xhtml"),'w') as TOCHTML:
        TOCHTML.write('<?xml version="1.0"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"> <html xmlns="http://www.w3.org/1999/xhtml"> <head> <title>Table of Contents</title> <link href="../Styles/sgc-toc.css" rel="stylesheet" type="text/css"/> </head> <body> <div class="sgc-toc-title">Table of Contents</div>\n')
        for value in nextDict.values():
            title,filename=value
            TOCHTML.write(f'<div class="sgc-toc-level-1"> <a href="{filename}">{title}</a> </div>\n')
        TOCHTML.write('</body></html>\n')

    with open(os.path.join(writeDir,"content.opf"),'w') as opf:
        opf.write(f'<?xml version="1.0" encoding="utf-8"?> <package version="2.0" unique-identifier="BookId" xmlns="http://www.idpf.org/2007/opf"> <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf"> <dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:e7268940-a653-40b4-9257-77d17d88a4f8</dc:identifier> <dc:language>en</dc:language> <dc:title>Words of Brandon</dc:title> <meta content="1.0.0" name="SandoRip Version"/> <dc:date opf:event="modification" xmlns:opf="http://www.idpf.org/2007/opf">{d2}</dc:date> </metadata> <manifest><item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>\n')
        for value in nextDict.values():
            title,filename=value
            opf.write(f'<item id="x{filename}" href="Text/{filename}" media-type="application/xhtml+xml"/>\n')
        opf.write('<item id="sgc-toc.css" href="Styles/sgc-toc.css" media-type="text/css"/> <item href="OEBPS/cover.jpg" id="cover" media-type="image/jpeg"/> <item id="TOC.xhtml" href="Text/TOC.xhtml" media-type="application/xhtml+xml"/> </manifest> <spine toc="ncx"> <itemref idref="TOC.xhtml"/>\n')
        for value in nextDict.values():
            title,filename=value
            opf.write(f'<itemref idref="x{filename}"/>\n')
        opf.write('</spine> <guide> <reference type="toc" title="Table of Contents" href="Text/TOC.xhtml"/> </guide> </package>\n')

#html sorting code
def trimHTML(inArr):
    outString = io.StringIO()
    skipLines=0
    mode=""
    title=""
    date=""
    dateSort=""
    titleGotten=False
    outString.write('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n<html lang="en-us" xmlns="http://www.w3.org/1999/xhtml">\n<head><title></title></head>\n<body>')
    for item in inArr:
        if not skipLines:
            if "entry-content" in item: #use this tag as a line break
                outString.write("</p>\n\n<center>***</center>\n<p>")
            elif "entry-speaker" in item: #next line is a name or something else to be bolded
                skipLines=1
                mode="author"
            elif 'class="entry-event-name"' in item and not titleGotten: #the title and date are present
                title=item.split(">")[1].split(" (<")[0]
                datearr=item.split('datetime="')[1].split('"')[0].split("-")
                date=f"{calendar.month_name[int(datearr[1])]} {datearr[2]} {datearr[0]}"
                dateSort=f"{datearr[0]}{str(datearr[1]).zfill(2)}{str(datearr[2]).zfill(2)}"
                outString.write(f'<p><center><big><big><b>{title}</b></big></big></center>\n<center><big><b>{date}</b></big></center></p>\n')
                titleGotten=True
        else:
            if mode=="author":
                outString.write(f"<b>{item}:</b>\n")
                mode="skipOne"
            elif mode=="skipOne":
                mode="body"
            elif mode=="body":
                if "</div>" in item:
                    mode=""
                    skipLines-=1
                else:
                    outString.write(f"{item}\n")
    outString.write('<center>---</center>\n</body>\n</html>')
    if dateSort=="":
        dateSort="99999999"
    return outString.getvalue(),title,date,dateSort

def convertDataFromLinks(location, saveFolder): #slim down the raw HTML page to just what is needed and sorts them
    http = urllib3.PoolManager()
    sortList=[]
    with open(location,"r") as links:
        for line in links.readlines():
            response = http.request("GET",line.strip())
            rawHTML=response.data.decode()
            data,title,date,dateSort=trimHTML(rawHTML.splitlines())
            fileTitle=f"{re.sub(r'[^a-zA-Z0-9 ]', '', title)}_{date}.html"
            with open(os.path.join(saveFolder,fileTitle),'w') as outFile:
                outFile.write(data)
            sortList.append((dateSort,fileTitle))
    sortList.sort()
    for moveItem in sortList:
        discard,oldtitle=moveItem
        newname=str(sortList.index(moveItem)).zfill(8)
        os.rename(os.path.join(saveFolder,oldtitle), os.path.join(saveFolder,f"{newname}.html"))
        with open(os.path.join(saveFolder,f"{newname}.txt"),'w') as extraData:
            extraData.write(oldtitle)

#initial web getting code
def getLinks(location,mode="annotations"):
    i = 1
    previous=""
    http = urllib3.PoolManager()
    with open(location,'w') as links:
        while True:
            response = http.request("GET",f"https://wob.coppermind.net/events/?page={i}&")
            if response.data == previous: #coppermind returns the last page if you go past its number with requests, so it must be manually checked
                print("All pages read")
                break
            data=f"{response.data}".replace("\\n","\n")
            for line in data.splitlines():
                if re.search(r'href="/events/[0-9]',line):
                    if mode=="full":
                        links.write(f'https://wob.coppermind.net/events/{line.split("/")[-2]}/\n')
                    elif "annotations" in line:
                        links.write(f'https://wob.coppermind.net/events/{line.split("/")[-2]}/\n')
            previous=response.data
            print(f"Page {i} read")
            i+=1

#check if the generated links are identical. If they are, quit
def checkFiles(file1,file2):
    try:
        return cmp(file1,file2)
    except FileNotFoundError:
        return False #they dont match if one doesn't exist

if __name__ == '__main__': #standalone run function

    sys.argv[1:]
    #argument list:
    #--full: get every page and not just annotations
    #--use-old-files: rezip from already grabbed files
    #--force: refresh data even if no new links have appeared
    if "--use-old-files" not in sys.argv[1:]:
        print("Hello! Would you like to scrape some data today?")
        print("Reading every link on each page of wob.coppermind.net...")
        if "--full" in sys.argv:
            print("Full mode enabled, grabbing every link...\nThis will take a while...")
            getLinks(location=os.path.join(root,"links.txt"),mode="full")
        else:
            getLinks(location=os.path.join(root,"links.txt"))

        if checkFiles(os.path.join(root,"links.txt"),os.path.join(root,"oldlinks.txt")) and "--force" not in sys.argv:
            print("no changes have been made since last rip. Rezipping...")
            os.remove(os.path.join(root,"links.txt"))
        else:
            print("moving files...")
            os.rename(os.path.join(root,"links.txt"),os.path.join(root,"oldlinks.txt"))
            print("cleaning old files away")
            for file in os.listdir(os.path.join(root,"outBook","Text")):
                os.remove(os.path.join(root,"outBook","Text",file)) #clean folder
            try:
                os.remove(os.path.join(root,"outBook","toc.ncx"))
            except OSError:
                pass
            try:
                os.remove(os.path.join(root,"outBook","content.opf"))
            except OSError:
                pass
            print("old files removed\nGenerating pages...")
            convertDataFromLinks(os.path.join(root,"oldlinks.txt"), os.path.join(root,"outBook","Text"))
            print("Pages generated\nGenerating metadata...")
            generateImportantFiles(os.path.join(root,"outBook","Text"),os.path.join(root,"outBook"))
            os.rename(os.path.join(root,"outBook","TOC.xhtml"),os.path.join(root,"outBook","Text","TOC.xhtml"))
            print("Metadata generated\nZipping...")
    readfrom=os.path.join(root,"outBook")
    if "--use-old-files" in sys.argv:
        zipf = zipfile.ZipFile(os.path.join(root,"oldFiles.epub") , mode='w')
    elif "--full" in sys.argv:
        zipf = zipfile.ZipFile(os.path.join(root,"Words Of Brandon.epub") , mode='w')
    else:
        zipf = zipfile.ZipFile(os.path.join(root,"Cosmere Annotations.epub") , mode='w')
    lenDirPath = len(readfrom)
    for root, _ , files in os.walk(readfrom):
        for file in files:
            filePath = os.path.join(root, file)
            zipf.write(filePath , filePath[lenDirPath :] )
    zipf.close()
    print("Ebook made! Goodbye!")