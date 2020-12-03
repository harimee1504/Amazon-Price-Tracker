import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
headers = {
    'User-Agent': ua.chrome}
page = requests.get(
    'https://www.amazon.in/New-Apple-iPhone-11-64GB/dp/B08L8DV7BX/ref=sr_1_1?dchild=1&keywords=iphone&qid=1606706480&sr=8-1', headers=headers)
soup = BeautifulSoup(page.content, 'html5lib')
lst = []
for d in soup.findAll('div', attrs={'class': 'a-section a-spacing-none'}):
    name = d.find(
        'span', attrs={'class': 'a-size-large product-title-word-break'})
    if name != None:
        res = name.get_text()
        lst.append(res.strip())
print(lst[0])
