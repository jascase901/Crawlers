import pandas as pd

from bs4 import BeautifulSoup

import requests
import time


dog_breeds_url = 'https://www.akc.org/dog-breeds/'
r  = requests.get(dog_breeds_url) 
soup = BeautifulSoup(r.text)


def DogStatsFromUrl(breed , url):

    time.sleep(.4)
    r  = requests.get(url) 
    soup = BeautifulSoup(r.text)
    title_bar_divs = soup.findAll('h4', {"class": 'bar-graph__title'}) # find all links
    titles = [title_bar_div.findAll(text=True)[0] for title_bar_div in title_bar_divs]
    rank_divs = soup.findAll('div', {"class": 'bar-graph__bg'}) # find all links
    percentages = [link.find('div')["style"].split(":")[1] for link in rank_divs]
    rank_ints = [int(v.replace("%;","").strip()) for v in percentages]
    d = dict(zip(titles, rank_ints))
    d['breed']=breed
    return d

options = soup.findAll('div', {"class": 'custom-select'})[0] # find all links
url_d  =  dict([(breed.findAll(text=True)[0],breed['value']) for breed in options.findAll('option')])
records = []
for breed in url_d.keys():
    #too may request at once make some websites sad
    i = i + 1 
    #First element in list is the select a breed label
    if "Select A Breed" in breed:
        continue

    records.append(DogStatsFromUrl(breed, url_d[breed]))

df = pd.DataFrame(records)
#df.to_csv("all.csv")
HighlyTrainable = (df[df['Trainability']==100.0])
HighlyTrainable.sort_values(by="Shedding")
print(HighlyTrainable.count())






