import os
from datetime import date
today = date.today()
d2 = today.strftime("%B %d, %Y")
nextDict={}

root=os.path.dirname(__file__)
with open(os.path.join(root,"toc.ncx"),'w') as ToC:
    n=1
    ToC.write('<?xml version=\'1.0\' encoding=\'utf-8\'?> <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="eng"> <head> <meta content="fa10ed69-1e99-41b6-a80d-2d1ce2f9a2ad" name="dtb:uid"/> <meta content="3" name="dtb:depth"/> <meta content="calibre (4.12.0)" name="dtb:generator"/> <meta content="0" name="dtb:totalPageCount"/> <meta content="0" name="dtb:maxPageNumber"/> </head> <docTitle> <text>The Stormlight Archive 02 - Words of Radiance</text> </docTitle><navMap>\n')
    for file in os.listdir(os.path.join(root,"sortedtext")):
        if file.endswith(".html"):
            title=""
            with open(os.path.join(root,"sortedtext",file),'r') as openFile:
                with open(os.path.join(root,"sortedtext",file.replace("html","txt")),'r') as textFile:
                    title=textFile.readline().strip()
                ToC.write(f'<navPoint class="chapter" id="np_{n}" playOrder="{n}"><navLabel><text>{title}</text></navLabel><content src="Text/{file}"/></navPoint>\n')
            nextDict[n]=((title,file))
            n+=1
    ToC.write('</navMap></ncx>\n')

with open(os.path.join(root,"TOC.xhtml"),'w') as TOCHTML:
    TOCHTML.write('<?xml version="1.0"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"> <html xmlns="http://www.w3.org/1999/xhtml"> <head> <title>Table of Contents</title> <link href="../Styles/sgc-toc.css" rel="stylesheet" type="text/css"/> </head> <body> <div class="sgc-toc-title">Table of Contents</div>\n')
    for value in nextDict.values():
        title,filename=value
        TOCHTML.write(f'<div class="sgc-toc-level-1"> <a href="{filename}">{title}</a> </div>\n')
    TOCHTML.write('</body></html>\n')

with open(os.path.join(root,"content.opf"),'w') as opf:
    opf.write(f'<?xml version="1.0" encoding="utf-8"?> <package version="2.0" unique-identifier="BookId" xmlns="http://www.idpf.org/2007/opf"> <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf"> <dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:e7268940-a653-40b4-9257-77d17d88a4f8</dc:identifier> <dc:language>en</dc:language> <dc:title>Words of Brandon</dc:title> <meta content="1.0.0" name="SandoRip Version"/> <dc:date opf:event="modification" xmlns:opf="http://www.idpf.org/2007/opf">{d2}</dc:date> </metadata> <manifest><item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>\n')
    for value in nextDict.values():
        title,filename=value
        opf.write(f'<item id="x{filename}" href="Text/{filename}" media-type="application/xhtml+xml"/>\n')
    opf.write('<item id="sgc-toc.css" href="Styles/sgc-toc.css" media-type="text/css"/> <item href="OEBPS/cover.jpg" id="cover" media-type="image/jpeg"/> <item id="TOC.xhtml" href="Text/TOC.xhtml" media-type="application/xhtml+xml"/> </manifest> <spine toc="ncx"> <itemref idref="TOC.xhtml"/>\n')
    for value in nextDict.values():
        title,filename=value
        opf.write(f'<itemref idref="x{filename}"/>\n')
    opf.write('</spine> <guide> <reference type="toc" title="Table of Contents" href="Text/TOC.xhtml"/> </guide> </package>\n')