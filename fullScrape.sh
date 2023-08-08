cd webget
./webGetter.sh || exit 1  #generate a list of ALL coppermind WoB pages. quit with error if nothing has changed since last run.
cd ..
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
