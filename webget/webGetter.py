import urllib3
import os
import re
from filecmp import cmp

root=os.path.dirname(__file__)

def getLinks(location):
    i = 1
    previous=""
    http = urllib3.PoolManager()
    with open(location,'w') as links:
        while True:
            response = http.request("GET",f"https://wob.coppermind.net/events/?page={i}&")
            if response.data == previous: #coppermind returns the last page if you go past it's number with requests, so it must be manually checked
                print("All pages read")
                break
            data=f"{response.data}".replace("\\n","\n")
            for line in data.splitlines():
                if re.search(r'href="/events/[0-9]',line):
                    links.write(f'https://wob.coppermind.net/{line.split("/")[-2]}/\n')
            previous=response.data
            print(f"Page {i} read")
            i+=1

#check if the generated links are identical. If they are, quit
def checkFiles(file1,file2):
    try:
        return cmp(file1,file2)
    except FileNotFoundError:
        return False #they dont match if one doesn't exist
if __name__ == '__main__':
    getLinks(location=os.path.join(root,"links.txt"))
    if checkFiles(os.path.join(root,"links.txt"),os.path.join(root,"..","links.txt")): #files are the same
        print("files are the same")
        exit()
    print("moving files...")
    os.rename(os.path.join(root,"links.txt"),os.path.join(root,"..","links.txt"))