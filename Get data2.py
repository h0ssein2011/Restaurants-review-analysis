import requests
# Set headers
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})


from bs4 import BeautifulSoup

url = "https://snappfood.ir/restaurant/city/Tehran/near/275?lat=35.698066949844&long=51.372826695442&services=RESTAURANT"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')
# print(soup.prettify())

base_link='https://snappfood.ir/'
restaurant_links=[]
for sp in soup.findAll('a'):

    hrefs=sp.attrs['href']
    request=requests.get(base_link+hrefs)
    if request.status_code==200:
        restaurant_links.append(base_link+hrefs)


print(restaurant_links)
