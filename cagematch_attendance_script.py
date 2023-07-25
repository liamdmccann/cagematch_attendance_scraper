#%%
#TODO - append venue_finder_cagematch_script.py script onto this script
#%% load libraries and define dataclasses
from dataclasses import dataclass
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlparse
from urllib.parse import parse_qs
import yaml
from enum import IntEnum
from datetime import date
import pandas as pd
import csv

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
#%% list of venues
#TODO - build list of venues, to allow iterating over list in next section
#%% load korakuen shows (manual list)
with open(f'Korakuen Hall shows.yaml','r') as file:
    Korakuen_showlist = yaml.safe_load(file)
#%% load korakuen shows (automated list from venue_finder_cagematch_script.py)
with open(f'new Korakuen show list.yaml','r') as file:
    new_Korakuen_showlist = yaml.safe_load(file)
#%% load ryogoku shows
with open(f'Ryogoku Kokugikan shows.yaml','r') as file:
    Ryogoku_showlist = yaml.safe_load(file)
#%% load ota shows
with open(f'Ota Ward Central Gymnasium shows.yaml','r') as file:
    Ota_showlist = yaml.safe_load(file)
#%% load EDION #2 shows
with open(f'Osaka EDION #2 shows.yaml','r') as file:
    EDION_2_showlist = yaml.safe_load(file)
#%% load historical Carnival shows
with open(f'Champion_Carnival_shows.yaml','r') as file:
    Carnival_showlist = yaml.safe_load(file)

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

#%%
def get_CageMatch_information(show):
    url = urllib.request.urlopen(show)
    content = url.read()
    soup = BeautifulSoup(content)
    show_table = soup.find("div", {"class": "InformationBoxTable"})
    keys = [span.get_text() for span in show_table.find_all("div", {"class": "InformationBoxTitle"})]
    values = [span.contents[0] for span in show_table.find_all("div", {"class": "InformationBoxContents"})]
    dictionary = dict(zip(keys, values))
    arena = dictionary["Arena:"].get_text()
    date_str = dictionary["Date:"].get_text()
    if dictionary['Attendance:'].get_text() != " ":
        attendance_str = dictionary["Attendance:"].get_text()
        attendance = attendance_str.replace('.', ',')
    else:
        dictionary['Attendance'] = 'Attendance not available.'
#    dd, mm, yy = date_str.split(".")
#    date_obj = date(int(yy), int(mm), int(dd))
    show_name = dictionary["Name of the event:"]
    promotion_str = dictionary["Promotion:"]
    promotion = parse_promotion_info(promotion_str)
    show_id = url
    return Show(arena, date_str, show_name, promotion, attendance, show_id)

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
    return(arena, promotion_name, show_date, show_name, attendance, url)
#%%
for show in Korakuen_showlist:
    print(extract_show_information(show))
#%%
for show in new_Korakuen_showlist:
    print(extract_show_information(show))
#%%
for show in Ryogoku_showlist:
    print(extract_show_information(show))
#%%
for show in Ota_showlist:
    print(extract_show_information(show))
#%%
for show in Carnival_showlist:
    print(extract_show_information(show))

#%%
#TODO - iterate over list of venues in 
with open('CSV files/Korakuen Hall cagematch_stats.csv', 'w') as file:
    writer=csv.writer(file, delimiter=',',lineterminator='\n',)
    writer.writerow(['Arena', 'Promotion', 'Show Date', 'Show Name', 'Attendance', 'Cagematch URL'])
    for show in Korakuen_showlist:
        show_information = extract_show_information(show)
        row = show_information
        writer.writerow(row)

#%%
with open('CSV files/Ryogoku Kokugikan cagematch_stats.csv', 'w') as file:
    writer=csv.writer(file, delimiter=',',lineterminator='\n',)
    writer.writerow(['Arena', 'Promotion', 'Show Date', 'Show Name', 'Attendance', 'Cagematch URL'])
    for show in Ryogoku_showlist:
        show_information = extract_show_information(show)
        row = show_information
        writer.writerow(row)

#%%
with open('CSV files/Ota Ward Central Gymnasium cagematch_stats.csv', 'w') as file:
    writer=csv.writer(file, delimiter=',',lineterminator='\n',)
    writer.writerow(['Arena', 'Promotion', 'Show Date', 'Show Name', 'Attendance', 'Cagematch URL'])
    for show in Ota_showlist:
        show_information = extract_show_information(show)
        row = show_information
        writer.writerow(row)
#%%
with open('CSV files/EDION Arena #2 cagematch_stats.csv', 'w') as file:
    writer=csv.writer(file, delimiter=',',lineterminator='\n',)
    writer.writerow(['Arena', 'Promotion', 'Show Date', 'Show Name', 'Attendance', 'Cagematch URL'])
    for show in EDION_2_showlist:
        show_information = extract_show_information(show)
        row = show_information
        writer.writerow(row)


#%%
with open('Korakuen + Ota + Ryogoku cagematch stats.csv', 'w') as file:
    writer=csv.writer(file, delimiter=',',lineterminator='\n',)
    writer.writerow(['Arena', 'Promotion', 'Show Date', 'Show Name', 'Attendance', 'Cagematch URL'])
    for show in Korakuen_showlist:
        show_information = extract_show_information(show)
        row = show_information
        writer.writerow(row)
    for show in Ota_showlist:
        show_information = extract_show_information(show)
        row = show_information
        writer.writerow(row)
    for show in Ryogoku_showlist:
        show_information = extract_show_information(show)
        row = show_information
        writer.writerow(row)


#%%
with open('Champion Carnival cagematch_stats.csv', 'w') as file:
    writer=csv.writer(file, delimiter=',',lineterminator='\n',)
    writer.writerow(['Arena', 'Promotion', 'Show Date', 'Show Name', 'Attendance', 'Cagematch URL'])
    for show in Carnival_showlist:
        show_information = extract_show_information(show)
        row = show_information
        writer.writerow(row)
