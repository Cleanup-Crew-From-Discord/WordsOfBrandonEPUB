rm *index*
for i in {1..10}; do
wget "https://wob.coppermind.net/events/?page=$i&" --restrict-file-names=windows
done
> links.txt

for i in *\&; do
 for line in $(cat "$i" | grep 'href="/events/[0-9]'); do
  line=$(echo "${line%/*}")
  line=$(echo "${line#*/}")
  if [[ "$line" != "<a" ]]; then
   echo "https://wob.coppermind.net/$line/" >> links.txt
  fi
 done
done

if cmp --silent links.txt ../links.txt; then
echo "no change, quitting..."
exit 1
else
cp links.txt ../links.txt
fi
