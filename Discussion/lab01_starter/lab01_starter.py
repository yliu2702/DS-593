# -*- coding: utf-8 -*-
"""lab01_starter.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1akh7NDZVfgsajVazdHeS4zeUQS8Ra1eK
"""

!pip install requests
!pip install beautifulsoup4
!pip install lxml

import requests
from bs4 import BeautifulSoup

movie_url = "https://www.boxofficemojo.com/chart/top_lifetime_gross/"
r = requests.get(movie_url)
# r.content (b), r.text
if r.status_code ==200:
    print(r.content)
    print(r.text)

# image fetch from r.content (download jpg)
img_url = "https://m.media-amazon.com/images/M/MV5BOTAzODEzNDAzMl5BMl5BanBnXkFtZTgwMDU1MTgzNzE@._V1_SY139_CR1,0,92,139_.jpg"
r = requests.get(img_url)
with open('temp_img.jpg', 'wb') as f:
    f.write(r.content)

# fetch
with open('/content/sample_html.html') as f:
  data = f.read()

soup = BeautifulSoup(data, 'html')

# 'p' 文本内容，'a'超链接/网址
soup.find('table') #find_all()

# find string
soup.find(string = "List Item One").parent.parent

soup.find('a')

# Get the Country and Population Table and store it in SQLite3 database

wiki_url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"

response = requests.get(wiki_url)
print(response.status_code == 200)

soup = BeautifulSoup(response.content, 'html')

tables = soup.find_all('table')
len(tables)

# find the class of desired table
for table in tables:
  if table.find(string = '1 Jul 2024'):
    print(table['class'])

table = soup.find('table', class_ = ['wikitable', 'sortable', 'sticky-header', 'sort-under', 'mw-datatable', 'col2left', 'col6left'])

table_1 = soup.find_all('table',{'class': 'wikitable'})

type(table),type(table_1) # want Tag for further operation

for row in table.find('tbody').find_all('tr')[2:]:
  print("The Location is: ", row.find_all('td')[1].text)
  print("The population is ",row.find_all('td')[2].text)
  break

countries = []
populations = []
for i, row in enumerate(table.find('tbody').find_all('tr')[2:]):
  if i == 1:
    countries.append(row.find_all('td')[1].text.strip())
    populations.append(row.find_all('td')[2].text.strip())
    print("The Location is: ", row.find_all('td')[1].text)
    print("The population is ",row.find_all('td')[2].text)
  else:
    countries.append(row.find_all('td')[1].text.strip())
    populations.append(row.find_all('td')[2].text.strip())

    print("The Location is: ",row.find_all('td')[1].text)
    print("The population is ",row.find_all('td')[2].text)

import pandas as pd
import sqlite3
df = pd.DataFrame.from_dict({'countryname': countries, 'population':populations})
conn = sqlite3.connect('somedatabase.db')
<<<<<<< HEAD
df.to_sql('populations', conn, if_exists='replace')
=======
df.to_sql('populations', conn, if_exists='replace')

>>>>>>> 71ed72cf2a7063ef6673808104bd908760320141
