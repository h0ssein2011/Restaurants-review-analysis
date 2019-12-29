import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
# Set headers
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
base_link='https://fidilio.com'

def getRestaurantLink(url):
	links = []
	req = requests.get(url, headers)
	soup = BeautifulSoup(req.content, 'html.parser')
	#print(soup.prettify())
	restaurant_links=[]
	for sp in soup.find_all("a", class_="restaurant-link"):
		links.append(sp.get('href'))

	return links
restaurant_name = {}
restaurant_name['name'] = []
restaurant_name['comment'] = []

def getRestaurantInfo(link):
	url = base_link + link
	print(url)
	req = requests.get(url, headers)
	soup = BeautifulSoup(req.content, 'html.parser')	
	# f = open("comments.csv", "a")


	for div in soup.find_all("div", class_="text-limitation show all mobile-hd"):
		restaurant = soup.find_all("h1" , property="name")
		restaurant = restaurant[0].text

		restaurant_name['name'].append(restaurant)
		restaurant_name['comment'].append(div.string)

	df=pd.DataFrame(restaurant_name)
	df.to_csv('commentsdata.csv',index=False)


		#write data to csv file
		# f.write(restaurant_name)
		# f.write(div.string)
	# 	f.write(" ---------------  \n")
	#
	# f.write(" ---------------  \n")
	# f.write(" ---------------  \n")
	# f.write(" ---------------  \n")
	# f.close()




for i in range(10):
	url = "https://fidilio.com/restaurants/in/tehran/تهران/?p=" + str(i)
	restaurantLink = getRestaurantLink(url);
	for i in restaurantLink:
		getRestaurantInfo(i)
		

