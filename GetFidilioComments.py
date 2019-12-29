import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set headers
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
base_link = 'https://fidilio.com'

def getRestaurantLink(url):
	links = []
	req = requests.get(url, headers)
	soup = BeautifulSoup(req.content, 'html.parser')
	#print(soup.prettify())
	restaurant_links=[]
	for sp in soup.find_all("a", class_="restaurant-link"):
		links.append(sp.get('href'))

	return links

def getRestaurantInfo(link):
	url = base_link + link
	print(url)
	req = requests.get(url, headers)
	soup = BeautifulSoup(req.content, 'html.parser')	

	restaurant = {}
	comments = []

	for div in soup.find_all("div", class_="venue-name-box"):
		restaurant['name'] = div.find('h1').string
	for div in soup.find_all("div", class_="text-limitation show all mobile-hd"):
		comments.append(div.string)

	restaurant['comments'] = comments
	df = pd.DataFrame(restaurant)
	df.to_csv('commentsdata1.csv', mode='a', header=False)


for i in range(10):
	url = base_link + "/restaurants/in/tehran/تهران/?p=" + str(i)
	restaurantLinks = getRestaurantLink(url);
	for link in restaurantLinks:
		getRestaurantInfo(link)
		

