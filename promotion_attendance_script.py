#%%
#TODO - append venue_finder_cagematch_script.py script onto this script
#%% load libraries and define dataclasses
from dataclasses import dataclass
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs
import yaml
from enum import IntEnum
from datetime import date
from bs4 import BeautifulSoup, SoupStrainer
import requests
import pandas as pd
from datetime import datetime, date
import urllib
import yaml
import csv
import codecs
import numpy as np
import glob
from itertools import chain
#%% today's date
today = date.today().strftime('%Y-%m-%d')
print(today)
#%%
TYPE_FIELD = 'id'
ID_FIELD = 'nr'

class ContentType(IntEnum):
    WRESTLER = 2
    PROMOTION = 8
    TAG_TEAM = 28
    STABLE = 29


@dataclass
class Promotion:
    id: int
    name: str


@dataclass
class Show:
    arena: str
    date: date
    show_name: str
    promotion: Promotion
    attendance: str
    show_id: str
    location: str

new_cagematch_links = []
#%%
def read_yaml_file(filename):
    with open(filename, 'r') as stream:
        try:
            print(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)
#%%
list_of_years = [
                # '1974',
                # '1975',
                # '1976',
                # '1977',
                # '1978',
                # '1979',
                # '1980',
                # '1981',
                # '1982',
                # '1983',
                # '1984',
                # '1985',
                # '1986',
                # '1987',
                # '1988',
                # '1989',
                # '1990',
                # '1991',
                # '1992',
                # '1993',
                # '1994',
                # '1995',
                # '1996',
                # '1997',
                # '1998',
                # '1999',
                # '2000',
                # '2001',
                # '2002',
                # '2003',
                # '2004',
                # '2005',
                # '2006',
                # '2007',
                # '2008',
                # '2009',
                # '2010',
                # '2011',
                # '2012',
                # '2013',
                # '2014',
                # '2015',
                # '2016',
                # '2017',
                # '2018',
                # '2019',
                # '2020',
                # '2021',
                # '2022',
                # '2023',
                '2024'
                ]
list_of_promotion_numbers = [
                        '6', #AJPW,
                        '7', #NJPW
                        '8', #NOAH
                        '118', #DDT
                        '96', #DG
                        '2965', #GLEAT
                        '602', #FREEDOMS
                        '117', #BJW
                        '13', #ZERO-1
                        '745', #STARDOM
                        '1467', #TJPW,
                        '1613', #Marvelous
                        '1763', #SEAdLINNNG
                        '137', #Active Advance,
                        '2516', #JTO 
                        '665', #Ice Ribbon
                        '154', #Sendai Girls,
                        '676' #Kyushu Pro
                    ]
list_of_promotions = [
        'AJPW',
        'NJPW',
        'NOAH',
        'DDT',
        'DG',
        'GLEAT',
        'FREEDOMS',
        'BJW',
        'ZERO-1',
        'STARDOM',
        'TJPW',
        'Marvelous',
        'SEAdLINNNG',
        'Active Advance',
        'JTO',
        'Ice Ribbon',
        'Sendai Girls',
        'Kyushu Pro'
]
list_of_months = [
                  '01',
                #   '02',
                #   '03',
                #   '04',
                #   '05',
                #   '06',
                #   '07',
                #   '08',
                #   '09',
                #   '10',
                #   '11',
                #   '12'
                ]
#
# 
# https://www.cagematch.net/?id=1&view=search&sEventName=&sPromotion=7&sDateFromDay=01&sDateFromMonth=01&sDateFromYear=2023&sDateTillDay=31&sDateTillMonth=12&sDateTillYear=2023&sRegion=&sEventType=&sLocation=&sArena=&sAny=
#%%
show_list = []
lst = []
for promotion_number in list_of_promotion_numbers:
    promotion = np.select([
        promotion_number == "6",
        promotion_number == "8",
        promotion_number == "7",
        promotion_number == "118",
        promotion_number == "96",
        promotion_number == "2965",
        promotion_number == "602",
        promotion_number == "117",
        promotion_number == "13",
        promotion_number == "745",
        promotion_number == "1467",
        promotion_number == "1613",
        promotion_number == "1763",
        promotion_number == "137",
        promotion_number == "2516",
        promotion_number == "665",
        promotion_number == "154",
        promotion_number == "676"
    ],
    [
        'AJPW',
        'NOAH',
        'NJPW',
        'DDT',
        'DG',
        'GLEAT',
        'FREEDOMS',
        'BJW',
        'ZERO-1',
        'STARDOM',
        'TJPW',
        'Marvelous',
        'SEAdLINNNG',
        'Active Advance',
        'JTO',
        'Ice Ribbon',
        'Sendai Girls',
        'Kyushu Pro'
    ]
    )
    promotion_string = str(promotion)
    print(promotion_string)
    for year in list_of_years:
        for month in list_of_months:
            print(year, month)
            url = ('https://www.cagematch.net/?id=1&view=search&sEventName=&sPromotion='
                   + promotion_number + 
                   '&sDateFromDay=01&sDateFromMonth='
                   +str(month)+'&sDateFromYear='+str(year) +
                    '&sDateTillDay=31&sDateTillMonth=' + 
                    str(month)+'&sDateTillYear='+str(year)+'&sRegion=&sEventType=&sLocation=Japan&sArena=&sAny=')
            cagematch = requests.get(url, headers={'Accept-Encoding': 'identity'}).text
            soup = BeautifulSoup(cagematch)
            links = soup.find_all('a')
            cagematch_links = [] 
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            for link in links:
                if((len(link)) == 15):
                    cagematch_links.append(link)
                    string = "https://www.cagematch.net/"
                    new_cagematch_links = [string + link for link in cagematch_links]
            show_list.append(new_cagematch_links)

#%%
print(show_list)
#%%
#for promotion in list_of_promotions:
 #   files = glob.glob('promotion YAML files/' + promotion +' YAML Files/*.yaml')
  #  for file in files:
   ##    cagematch_links = []
     #   cagematch_links.append(read_yaml_file(file))

show_list = list(filter(('https://www.cagematch.net/?view=roulette').__ne__, show_list))
show_list = list(chain.from_iterable(show_list))
#%% 
def parse_promotion_info(promotion_str):
#TODO - check if this is still needed
    """
    From the contents of the 'Promotion' infobox, check for a link. If a link exists, and the content type in the URL
    indicates the link is to a Promotion page, parse the promotion information from the text.
    :param promotion_str: The contents of the 'Promotion: ' infobox.
    :return: a Promotion object
    """
    if promotion_str is not None:
        query_parts = parse_qs(urlparse(promotion_str.attrs['href']).query)
        link_type = int(query_parts.get(TYPE_FIELD)[0]) 
        if link_type == ContentType.PROMOTION:
            promotion_id = int(query_parts.get(ID_FIELD)[0])
            return Promotion(promotion_id, promotion_str.text)
    else:
        print("No promotion found, input was {0}".format(promotion_str))
        return Promotion(-1, "")

def get_CageMatch_information(show):
    url = urllib.request.urlopen(show)
    content = url.read()
    soup = BeautifulSoup(content)
    show_table = soup.find("div", {"class": "InformationBoxTable"})
    keys = [span.get_text() for span in show_table.find_all("div", {"class": "InformationBoxTitle"})]
    values = [span.contents[0] for span in show_table.find_all("div", {"class": "InformationBoxContents"})]
    dictionary = dict(zip(keys, values))
    if "Arena:" in dictionary:
        arena = dictionary["Arena:"].get_text()
    else:
        arena = "Arena not available."#    dd, mm, yy = date_str.split(".")
    date_str = dictionary["Date:"].get_text()
    location = dictionary["Location:"].get_text()
    dd, mm, yy = date_str.split(".")
    if "Attendance:" in dictionary:
        attendance_str = dictionary["Attendance:"].get_text()
        attendance = attendance_str.replace('.', ',')
    else:
        attendance = "Attendance not available."#    dd, mm, yy = date_str.split(".")
    date_obj = date(int(yy), int(mm), int(dd))
    show_name = dictionary["Name of the event:"]
    promotion_str = dictionary["Promotion:"]
    promotion = parse_promotion_info(promotion_str)
    show_id = url
    return Show(arena, date_obj, show_name, promotion, attendance, show_id, location)

#%%
show_DF = pd.DataFrame

def extract_show_information(show):
    url = show
    show_info = get_CageMatch_information(show)
    arena = show_info.arena
    promotion_name = show_info.promotion.name 
    show_date = show_info.date
    show_name = show_info.show_name
    attendance = show_info.attendance
    location = show_info.location
    return(promotion_name, location, arena, show_date, show_name, attendance, url)

#%% write 2023 
show_information = []

for show in show_list:
    show_info = extract_show_information(show)
    print(show_info)
    show_information.append(show_info)
#%%
all_promotions_total_attendance = pd.DataFrame(show_information, columns=['Promotion', 'Location', 'Venue', 'Show Date', 'Show Name', 'Attendance', 'Cagematch URL'])
all_promotions_total_attendance['Show Date'] = all_promotions_total_attendance['Show Date']
all_promotions_total_attendance.to_csv(
    'CSV files/' + today + ' - All promotions attendance stats.csv', index=False, encoding='utf-8', date_format='%Y-%m-%d')
print('Current show stats done.')
#%% remove duplicates


all_promotions_df = pd.read_csv('CSV files/' + today + ' - All promotions attendance stats.csv')
all_promotions_df.drop_duplicates(inplace=True)
all_promotions_df.to_csv('CSV files/' + today + ' - All promotions attendance stats.csv', index=False)


