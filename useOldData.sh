rm python/text/* python/sortedtext/* outBook/Text/* outBook/toc.ncx outBook/content.opf
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
zip "Words Of Brandon $dateMade - OLD DATA.epub" * -r
mv "Words Of Brandon $dateMade - OLD DATA.epub" ..
cd ..