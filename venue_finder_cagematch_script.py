# %%
from bs4 import BeautifulSoup, SoupStrainer
import requests
import pandas as pd
import sys
import re
from datetime import datetime, date
import urllib
import yaml
# %% find events from cagematch
first_year = 2020
last_year = 2023
venue = "korakuen+hall"
lst = []
url = ('https://www.cagematch.net/?id=1&view=search&sEventName=&sPromotion=&sDateFromDay=01&sDateFromMonth=01&sDateFromYear='+str(first_year) +
        '&sDateTillDay=31&sDateTillMonth=12&sDateTillYear='+str(last_year)+'&sRegion=&sEventType=&sLocation=&sArena='+str(venue)+'&sAny=')
print(url)
#%%
cagematch = requests.get(url, headers={'Accept-Encoding': 'identity'}).text
soup = BeautifulSoup(cagematch)
print(soup)
#%%
links = soup.find_all('a')
print(links)
#%%
cagematch_links = []
links = [a.get('href') for a in soup.find_all('a', href=True)]
print(links)
for link in links:
    if((len(link)) == 15):
        cagematch_links.append(link)
#%%
string = "https://www.cagematch.net/"
new_cagematch_links = [string + link for link in cagematch_links]
print(new_cagematch_links)
#%% export to YAML
#%% write to yaml
with open(r'new Korakuen show list.yaml', 'w') as file:
    documents = yaml.dump(new_cagematch_links, file)