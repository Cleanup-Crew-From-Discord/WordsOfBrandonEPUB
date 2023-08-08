import os

root=os.path.dirname(__file__)
def monthToNum(shortMonth):
    return {
            'jan': 1,
            'feb': 2,
            'march': 3,
            'april': 4,
            'may': 5,
            'june': 6,
            'july': 7,
            'aug': 8,
            'sept': 9, 
            'oct': 10,
            'nov': 11,
            'dec': 12
    }[shortMonth]
dates=[]
for file in os.listdir(os.path.join(root,"text")):
    dateTime=file.split("_")[0]
    month,day,year=dateTime.split()
    month=monthToNum(month.lower())
    dates.append((f"{year}.{month:02}.{int(day):02}",file))
dates.sort()
number=1
for i in dates:
    new,old=i
    name=old.split("_")[1].strip(".html")
    print(os.path.join(root,'text',old))
    os.system(f"cp \"{os.path.join(root,'text',old)}\" \"{os.path.join(root,'sortedtext',f'{int(number):06}')}.html\" ")
    os.system(f"echo \"{name}\" >> \"{os.path.join(root,'sortedtext',f'{int(number):06}')}.txt\"")
    number+=1