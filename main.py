import requests
from bs4 import BeautifulSoup
import re
import os

site = "https://mangaclash.com/manga/landlords-little-girl/"

response = requests.get(site)
soup = BeautifulSoup(response.text, 'html.parser')

lists = soup.find_all('li', {'class': "wp-manga-chapter"})

links = []
for i in lists:
    l = i.find('a', href=True)['href']
    links.append(l)

siteForImg = links[:-1]

for j in siteForImg:

    result = requests.get(j)

    soup = BeautifulSoup(result.text, 'html.parser')
    img_tags = soup.find_all('img', {'class': "wp-manga-chapter-img"})

    urls = [img['src'] for img in img_tags]

    for url in urls:
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png|jpeg))$', url)
        if not filename:
            print("Regex didn't match with the url: {}".format(url))
            continue
        print(j[51:-1])
        print(filename.group(1))
        try:
            os.mkdir(f'{j[51:-1]}')
        except:
            pass

        with open(os.path.join(f'{j[51:-1]}', filename.group(1)), 'wb') as f:
            if 'http' not in url:
                url = '{}{}'.format(site, url)
            response = requests.get(url)
            f.write(response.content)

# print(urls)
# print("\n".join(links))
# print(links[-1])
