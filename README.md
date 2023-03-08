# Web Scraping of House Price in Jabodetabek City (Jakarta, Bogor, Depok, Tangerang, Bekasi) in Indonesia

## About
Hello Everyone! In this project I created a simple web scraping of house price in Jabodetabek Indonesia. This personal project is created for enhancing my
data analytical skills and looking for houses in these locations.

## Tools
- Python
- Jupyter Noteboox

## Steps
### Importing Libraries
```
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import os
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
```
## Scraping the Data
```
for page, city, category in itertools.product(list_page,list_city, list_category):
    url = f'https://www.rumah123.com/jual/{str(city)}/{category}/?page={str(page)}#qid~42eeef39-13df-4144-afa7-f1229e9827be'
    r = requests.get(url, headers = header)
    c = r.content
    page = BeautifulSoup(c, 'html.parser')
    all_city = page.find_all('div',class_='ui-organism-intersection__element intersection-card-container')
    place_name = []
    address = []
    lb = []
    kt = []
    price = []
    mortage = []
    date_posted = []
    tayang = []
    for i in all_city:
        try:
            name = i.find('a').find('h2').text
        except:
            name = None
        try:
            alamat = i.find('p', class_= 'card-featured__middle-section__location').text
        except:
            alamat = None
        try:
            kamar = i.find('span', class_ = 'attribute-text').text
        except:
            kamar = None
        try:
            luas = i.find('div', class_ = 'attribute-info').find('span').text
        except:
            luas = None
        try:
            tes_harga = i.find('div', class_='card-featured__middle-section__price').find('strong').text
        except:
            tes_harga = None
        try:
            cicilan = i.find('div', class_='ui-organisms-card-r123-featured__middle-section__price').find('em').text.replace("Cicilan :","").strip()
        except:
            cicilan = None
        try:
            jadwal = i.find('div', class_='ui-organisms-card-r123-basic__bottom-section__agent').text
        except:
            jadwal = None
        place_name.append(name)
        address.append(alamat)
        kt.append(kamar)
        lb.append(luas)
        price.append(tes_harga)
        mortage.append(cicilan)
        tayang.append(jadwal)
        df = pd.DataFrame({'Place Name':place_name, 'Address':address, 'Bedroom':kt, 'Area':lb,
                            'Price':price, 'Mortage':mortage, 'Category': category, 'Tayang':tayang})
        df.to_csv(os.path.join(path, f'{page}_{city}_{category}.csv'), index=False, sep=';')
```
## Data Cleaning
```
#Combining The Data
os.chdir(path)
out = glob.glob('*.csv')
df = pd.concat(pd.read_csv(f) for f in out
```
```
#Removing Missing Value
df.isnull().sum()
df.dropna()
df.columns = [i.replace(" ","_") for i in df.columns]
```

```
#Cleaning House Price Information
df.Price.unique()
def angka(a):
    if "Miliar" in a:
        return 1000
    elif "Triliun" in a:
        return 1000000
    else:
        return 1
df['Angka'] = df.Price.apply(lambda x: angka(x))
df.Price = df.Price.str.replace(",",".").str.replace("Miliar","").str.replace("Rp","").str.replace("Juta","").str.replace("Triliun","").str.strip()
df.Price = df.Price.astype('float')
df['Price (in Million)'] = df.Price * df.Angka
del df['Angka']
```

```
#Correcting City Location
df[['Kecamatan','Kota']] = df.Address.str.strip().str.split(",",expand=True)
del df['Address']
```

```
#Correcting Area
df.price.unique()
df[['Area (m2)','Satuan']] = df['Area'].str.split("m",expand=True)
df['Area (m2)'] = df['Area (m2)'].astype('float')
```

```
#Creating Price per Area
df2['Area (m2)'] = df2['Area (m2)'].astype('float')
```

```
#Getting Year Uploaded
df[['Nama','Date Posted']] = df['Tayang'].str.split("Tayang Sejak", expand=True)
df = df.drop(columns = ['Tayang', 'Satuan','Nama'])
df['Date Posted'] = df['Date Posted'].str.strip().str.replace(",","").str.strip()
df[['Day','Month','Year']] = df2['Date Posted'].str.split(" ", expand=True)
list_month = ['11', '10', '12', '09', '08', '07',
       '06', '05', '04', '03', '02', '01', None]
df['Month'] = df['Month'].replace(df['Month'].unique(), list_month)
df['Date'] = df['Day'] + '/' +df['Month']+'/'+df['Year']
df['Date'] = pd.to_datetime(df['Date'])
```



