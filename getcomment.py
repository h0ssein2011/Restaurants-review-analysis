import requests
from bs4 import BeautifulSoup
url = "https://fidilio.com/restaurants/barcoo1/%D8%A8%D8%A7%D8%B1%DA%A9%D9%88/"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')
comment_body = soup.find(class_='tab review-paginate')
comment=comment_body.find_all(class_='text-limitation show all mobile-hd')
#number of comment 
reviewlist=soup.find(id='review-list')
re_count=re.find(class_='reviews-count')
nazar_number=re_count.get_text()
nazar_number=nazar_number.replace(' ','')
nazar_number=nazar_number.replace('تعدادنظرات:','')
s=int(nazar_number)

for i in range(s):
    comments.append(comment[i].get_text())
comments