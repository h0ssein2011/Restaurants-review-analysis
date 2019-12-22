import requests
from bs4 import BeautifulSoup
import json
# Set headers
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
base_link='https://snappfood.ir/'

def getRestaurantLink(url):
	links = [];
	req = requests.get(url, headers)
	soup = BeautifulSoup(req.content, 'html.parser')
	print(soup.prettify())
	restaurant_links=[]
	for sp in soup.find_all("div", class_="kk-pp-btn"):
		link=sp.find('a')
		links.append(link.get('href'));

	return links;
	
def getRestaurantInfo(code):
	url = base_link + 'restaurant/menu/new-menu/load?code=' + code + '&date=today&time=-1'
	cookies = {
		'analytics_session_token': '2875b200-8004-b107-1d30-c2da07f348ec',
		'yektanet_session_last_activity': '12/20/2019',
		'_gid': 'GA1.2.1341999565.1576783820',
		'PHPSESSID': 'ADD YOUR PHPSESSID',
		'REMEMBERME': 'ADD YOUR REMEMBERME',
		'_ga': 'GA1.2.493878719.1576783820',
		'_gcl_au': '1.1.301510012.1576783814',
		'selected_city': '1',
		'scarab.visitor': '%224D539A36AB50A1D4%22',
		'analytics_campaign': '{%22source%22:%22direct%22%2C%22medium%22:null}',
		'analytics_token': 'dca6bb2a-7a86-7c21-36ed-238474a66531'
	}

	response = requests.get(url, cookies=cookies).json();
	
	f = open("restaurant_info.txt", "a")
	f.write("Resaurant: " + response["param"]["vendor"]["title"] + "\n");
	f.write("Area: " + response["param"]["vendor"]["area"] + "\n");
	f.write("Delivery Area: " + response["param"]["vendor"]["deliveryArea"] + "\n");
	f.write("Address: " + response["param"]["vendor"]["address"] + "\n");
	f.write("Phone: " + response["param"]["vendor"]["phone"] + "\n");
	f.write("Phone: " + response["param"]["vendor"]["phone"] + "\n");
	f.write("Menu ---------------  \n");
	menu = response["param"]["menu"];
	for m in menu:
		f.write("Category: " + m["category"] + "\n");
		f.write(" ---------------  \n");
		products = m["products"]
		for product in products:
			f.write("Name: " + product["productVariationTitle"] + "\n");
			f.write("Title: " + product["title"] + "\n");
			f.write("Description: " + product["description"] + "\n");
			f.write("Price: " + str(product["price"]) + "\n");
			f.write(" ---------------  \n");

		f.write(" ---------------  \n");
		f.write(" ---------------  \n");

	f.write("****************** \n");
	f.write("****************** \n");
	f.close()


for i in range(1000):
	url = "https://snappfood.ir/restaurant/?page=" + str(i)
	restaurantLink = getRestaurantLink(url);
	for i in restaurantLink:
		code = i.split('/')[3]
		getRestaurantInfo(code)
		

