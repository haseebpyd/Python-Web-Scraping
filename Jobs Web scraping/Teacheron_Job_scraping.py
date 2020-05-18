import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import re

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
url = "https://www.teacheron.com/online-python-tutor-jobs"
headers={'User-Agent':user_agent,} 
request=urllib.request.Request(url,None,headers) #The assembled request
response = urllib.request.urlopen(request)
data = response.read() # The data u need


soup = BeautifulSoup(data, 'html.parser')

title=soup.find_all('h3')
pt=list()
pdd=list()
loc=list()

for i in range(len(title)):
   pt.append((title[i].a.get_text().strip()))

for i in range(len(title)):
   loc.append(str(re.findall("in (.+)", pt[i])))

desc=soup.find_all('p')
for i in range(len(desc)):
   pdd.append(desc[i].get_text().strip())

python_stuff=pd.DataFrame(
  {
    "Title":pt,
    "Location":loc,
    "Describtion":pdd   
  })

print(python_stuff)
python_stuff.to_csv('python_jobs.csv')
print(loc)

