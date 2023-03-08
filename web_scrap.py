import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import os
import glob
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
list_page = [*range(1,101)]
list_city = ['dki-jakarta','bekasi','tangerang','bogor','depok']
list_category = ['apartemen', 'rumah']
path = r'C:\Users\PutuAndika\OneDrive - Migo\Desktop\Web Scraping\Rumah'
path_sewa = r'C:\Users\PutuAndika\OneDrive - Migo\Desktop\Web Scraping\Rumah\Sewa'
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
path = r'C:\Users\PutuAndika\OneDrive - Migo\Desktop\Web Scraping\Rumah'
path_output = r'C:\Users\PutuAndika\OneDrive - Migo\Desktop\Web Scraping\Rumah\Combined'
os.chdir(path)
out = glob.glob('*.csv')
df2 = pd.concat([pd.read_csv(f,sep = ';') for f in out])
del df2['Mortage']
df2 = df2.dropna()
df2.columns = [i.replace(" ","_") for i in df2.columns]
def angka(a):
    if "Miliar" in a:
        return 1000
    elif "Triliun" in a:
        return 1000000
    else:
        return 1
df2['Angka'] = df2.Price.apply(lambda x: angka(x))
df2.Price = df2.Price.str.replace(",",".").str.replace("Miliar","").str.replace("Rp","").str.replace("Juta","").str.replace("Triliun","").str.strip()
df2.Price.unique()
df2.Price = df2.Price.astype('float')
df2.head()
df2['Price (in Million)'] = df2.Price * df2.Angka
df2.head()
del df2['Angka']
Correcting City
df2[['Kecamatan','Kota']] = df2.Address.str.strip().str.split(",",expand=True)
del df2['Address']
Cleaning Area
df2[['Area (m2)','Satuan']] = df2['Area'].str.split("m",expand=True)
df2['Area (m2)'] = df2['Area (m2)'].astype('float')
Price per Area
df2['Price per Area'] = df2['Price (in Million)'] / df2['Area (m2)']
Getting Year Uploaded
df2[['Nama','Date Posted']] = df2['Tayang'].str.split("Tayang Sejak", expand=True)
df2 = df2.drop(columns = ['Tayang', 'Satuan','Nama'])
df2['Date Posted'] = df2['Date Posted'].str.strip().str.replace(",","").str.strip()
df2[['Day','Month','Year']] = df2['Date Posted'].str.split(" ", expand=True)
list_month = ['11', '10', '12', '09', '08', '07',
       '06', '05', '04', '03', '02', '01', None]
df2['Month'] = df2['Month'].replace(df2['Month'].unique(), list_month)
df2['Date'] = df2['Day'] + '/' +df2['Month']+'/'+df2['Year']
df2.head()
df2['Date'] = pd.to_datetime(df2['Date'])
df2.to_excel(os.path.join(path_output,'Cleaned V2.xlsx'), index = False) 
