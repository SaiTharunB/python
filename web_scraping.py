import requests
from bs4 import BeautifulSoup

html=requests.get("https://en.wikipedia.org/wiki/Machine_learning")
bsObj=BeautifulSoup(html.content,"html.parser")
print(bsObj.title.string) #printing the title 
a_tags=bsObj.find_all('a') #finding all a tags and storing in list
print(a_tags) #printing all the extracted tags
for l in a_tags:
    print(l.get("href")) #extracting the links and printing 