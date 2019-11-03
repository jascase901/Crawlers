import pandas as pd

from bs4 import BeautifulSoup
from bs4 import NavigableString

from pathlib import PurePath
from zipfile import ZipFile

import requests
import time
import io


base="https://cc0textures.com/"
url = "{}list.php?q=&method=&sort=latest".format(base) 
r  = requests.get(url) 
soup = BeautifulSoup(r.text)

#with open("test.html", 'w') as f:
#    f.write(soup.html.encode('utf8'))

texture_links = [link for link in soup.findAll("a") if "view.php" in link.attrs['href']]
def is_next_link(link):
    has_list_php = "list.php" in link.attrs['href']
    if not has_list_php:
        return False

    for child in link.children:
        if isinstance(child, NavigableString):
            return False
        return "next.png" in child.attrs.get("src", "")

    return False


def visit(visit_url, texture_urls, visits):
    time.sleep(5)

    r  = requests.get(visit_url) 
    soup = BeautifulSoup(r.text)
    texture_urls_on_page = [link for link in soup.findAll("a") if "view.php" in link.attrs['href']]
    texture_urls_on_page.extend(texture_urls)

    next_links = [link for link in soup.findAll("a") if is_next_link(link)]

    for link in next_links:
        new_url = "{}{}".format(base, link.attrs['href'][2:])
        print(new_url)
        return visit(new_url, texture_urls_on_page, visits+1)

    #base case "No next link"
    return texture_urls_on_page

def download_view(view_anchor):
    download_relative_path = view_anchor.attrs['href'].replace('view','download') + "&res=8"
    download_url = "{}{}".format(base, download_relative_path[2:])
    r = requests.get(download_url)
    fname = Path(r.url).stem
    z = ZipFile(io.BytesIO(r.content))
    z.extractall(fname)

i = 0
for texture in possible_textures:
    i = i + 1
    print(i, len(possible_textures))
    try:
        download_view(texture)
    except:
        pass



#
#def DogStatsFromUrl(breed , url):
#
#    time.sleep(.4)
#    r  = requests.get(url) 
#    soup = BeautifulSoup(r.text)
#    title_bar_divs = soup.findAll('h4', {"class": 'bar-graph__title'}) # find all links
#    titles = [title_bar_div.findAll(text=True)[0] for title_bar_div in title_bar_divs]
#    rank_divs = soup.findAll('div', {"class": 'bar-graph__bg'}) # find all links
#    percentages = [link.find('div')["style"].split(":")[1] for link in rank_divs]
#    rank_ints = [int(v.replace("%;","").strip()) for v in percentages]
#    d = dict(zip(titles, rank_ints))
#    d['breed']=breed
#    return d
#
#options = soup.findAll('div', {"class": 'custom-select'})[0] # find all links
#url_d  =  dict([(breed.findAll(text=True)[0],breed['value']) for breed in options.findAll('option')])
#records = []
#for breed in url_d.keys():
#    #too may request at once make some websites sad
#    #First element in list is the select a breed label
#    if "Select A Breed" in breed:
#        continue
#
#    records.append(DogStatsFromUrl(breed, url_d[breed]))

#df = pd.DataFrame(records)
#df.to_csv("all.csv")
#df =pd.read_csv("/home/jason/Crawlers/dog-crawler/results/20190828_crawl.csv")
#HighlyTrainable = (df[df['Trainability']==100.0])
#HighlyTrainable.sort_values(by="Shedding")
#print(HighlyTrainable.count())






