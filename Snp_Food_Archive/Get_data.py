import requests
from bs4 import BeautifulSoup

result=requests.get('https://www.imdb.com/showtimes/?ref_=mojo')
src=result.content
soup=BeautifulSoup(src , 'lxml')

urls=[]
for sp in soup.findAll('span'):
    a_tag=sp.find('a')
    if bool(a_tag):
        hrefs=a_tag.attrs['href']
        print(hrefs)


#print(urls)
