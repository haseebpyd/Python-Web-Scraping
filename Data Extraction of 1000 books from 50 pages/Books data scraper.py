#complete documentation is avalible on my website.
#http://www.visionprogrammer.com/2020/05/python-web-scraping-beautifulsoup.html


import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl="http://books.toscrape.com/catalogue/page-"
names=[]
price=[]
for i in range(1,51):
    url=baseurl+str(i)+'.html'
    print('processing '+ url)
    r=requests.get(url)
    c=r.content
    
    soup=BeautifulSoup(c,'html.parser')
    books=soup.find_all('li',{"class":"col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    
    for i in range(len(books)):
        names.append(books[i].find('h3').text)
        price.append(books[i].find('p',{'class':'price_color'}).text)
        

dict={'Book Titles':names,
      'Price':price}
      
df=pd.DataFrame(dict)
df.to_csv('Books_Details.csv')
