rm links.txt
cd webget
python3 webGetter.py
cd ..
mkdir -p python/html python/text python/sortedtext/ outBook/Text
rm python/html/* python/text/* python/sortedtext/* outBook/toc.ncx outBook/content.opf outBook/Text/*
for i in $(cat links.txt); do
fname=$(echo "$i" | rev | cut -c 2- | rev | sed 's:.*/::')
wget "$i" -O python/html/$fname.html
sed -i -e 's/<em>/*start*/g' python/html/$fname.html
sed -i -e 's,</em>,*end*,g' python/html/$fname.html
sed -i -e 's/&lt;/(/g' python/html/$fname.html
sed -i -e 's,&gt;,),g' python/html/$fname.html
done
cd python
python3 parser.py
python3 sorter.py
python3 makeTOC.py
mv toc.ncx ../outBook
mv sortedText/*.html ../outBook/Text
mv TOC.xhtml ../outBook/Text
mv content.opf ../outBook
cd ../outBook
dateMade=$(date +%F)
zip "Words Of Brandon $dateMade.epub" * -r
mv "Words Of Brandon $dateMade.epub" ..
cd ..