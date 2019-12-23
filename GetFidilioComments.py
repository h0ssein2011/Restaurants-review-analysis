import requests
from bs4 import BeautifulSoup
import json
# Set headers
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
base_link='https://fidilio.com'

def getRestaurantLink(url):
	links = [];
	req = requests.get(url, headers)
	soup = BeautifulSoup(req.content, 'html.parser')
	#print(soup.prettify())
	restaurant_links=[]
	for sp in soup.find_all("a", class_="restaurant-link"):
		links.append(sp.get('href'));

	return links;
	
def getRestaurantInfo(link):
	url = base_link + link
	print(url)
	req = requests.get(url, headers)
	soup = BeautifulSoup(req.content, 'html.parser')	
	f = open("comments.log", "a")
	for div in soup.find_all("div", class_="text-limitation show all mobile-hd"):
		f.write(div.string);
		f.write(" ---------------  \n");

	f.write(" ---------------  \n");
	f.write(" ---------------  \n");
	f.write(" ---------------  \n");
	f.close()




for i in range(1000):
	url = "https://fidilio.com/restaurants/in/tehran/تهران/?p=" + str(i)
	restaurantLink = getRestaurantLink(url);
	for i in restaurantLink:
		getRestaurantInfo(i)
		

