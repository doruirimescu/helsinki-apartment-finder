from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# Import Apartment object
from apartment import Apartment, Apartments, Price, Area, Year, Vastike, Floor, Rooms, Zone

# Define Chromium as used browser
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

# Loop to loop through all pages
# Scrape first the number of pages (in progress)
url_list = []
locations = '''&locations=%5B%5B814,4, \
%22Lepp%C3%A4vaara,%20Espoo%22%5D,%5B798,4, \
%22Matinkyl%C3%A4,%20Espoo%22%5D,%5B335047,4, \
%22Tiistil%C3%A4,%20Espoo%22%5D,%5B797,4, \
%22Olari,%20Espoo%22%5D,%5B815,4, \
%22Kilo,%20Espoo%22%5D,%5B5694675,4, \
%22Finnoo,%20Espoo%22%5D,%5B13736198,4, \
%22Vermonniitty,%20Espoo%22%5D,%5B13617407,3, \
%22Peril%C3%A4nniitty,%20Espoo%22%5D,%5B880,4, \
%22M%C3%A4kkyl%C3%A4,%20Espoo%22%5D%5D'''

n_pages = 1
SLEEP_TIME_S = 0

for p in range(1, n_pages + 1):
    url_01 = "https://asunnot.oikotie.fi/myytavat-asunnot?pagination="
    url_02 = str(p)
    url_03 = "&cardType=100"
    url_list.append(url_01 + url_02 + locations + url_03)


apartment_urls = []
# Loop through each url and get individual apartment urls
for page_number, i in enumerate(url_list):
    url = i
    driver.get(url)
    time.sleep(SLEEP_TIME_S)  # This will make it work no matter how many pages are scraped at once
    content = driver.page_source
    soup = BeautifulSoup(content)
    while True:
        try:
            for a in soup.findAll('div', href=False, attrs={'class': 'cards__card'}):
                url = a.find('a')['href']
                apartment_urls.append(url)
                print("Page: ", str(page_number), " url: ", url)
        except TypeError:
            break

apartment_list = []
# For each apartment url, scrape the data
for url_number, url in enumerate(apartment_urls):
    driver.get(url)
    time.sleep(SLEEP_TIME_S)
    content = driver.page_source
    soup = BeautifulSoup(content)
    try:
        for a in soup.findAll('div', href=False, attrs={'class': 'info-table__row'}):
            if a.find('dt', attrs={'class': 'info-table__title'}) is None:
                continue
            if a.find('dt', attrs={'class': 'info-table__title'}).text == "Velaton hinta":
                # Get price
                price = a.find('dd', attrs={'class': 'info-table__value'}).text
                price = price.replace("€", "")
                price = price.replace("\xa0", "")
                price=price.replace(",", ".")
                price.strip()
                price = float(price)

            if a.find('dt', attrs={'class': 'info-table__title'}).text == "Asuinpinta-ala":
                # Get area
                area = a.find('dd', attrs={'class': 'info-table__value'}).text
                area = area.replace("m²", "")
                area = area.replace("\xa0", "")
                area = area.replace(",", ".")
                area.strip()
                area = float(area)

            if a.find('dt', attrs={'class': 'info-table__title'}).text == "Sijainti":
                # Get address
                address = a.find('dd', attrs={'class': 'info-table__value'}).text
                address = address.replace("\xa0", "")
                address.strip()

            if a.find('dt', attrs={'class': 'info-table__title'}).text == "Kaupunginosa":
                # Get zone
                zone = a.find('dd', attrs={'class': 'info-table__value'}).text
                zone = zone.replace("\xa0", "")
                zone=zone.strip()

            if a.find('dt', attrs={'class': 'info-table__title'}).text == "Kerros":
                # Get floor
                floor = a.find('dd', attrs={'class': 'info-table__value'}).text
                floor.strip()
                floor = int(floor[0])

            if a.find('dt', attrs={'class': 'info-table__title'}).text == "Huoneita":
                # Get rooms
                rooms = a.find('dd', attrs={'class': 'info-table__value'}).text
                rooms.strip()
                rooms = int(rooms[0])

            if a.find('dt', attrs={'class': 'info-table__title'}).text == "Tontin omistus":
                # Get ownership
                ownership = a.find('dd', attrs={'class': 'info-table__value'}).text
                ownership.strip()

            if a.find('dt', attrs={'class': 'info-table__title'}).text == "Lämmitys":
                # Get heating
                heating = a.find('dd', attrs={'class': 'info-table__value'}).text
                heating.strip()

            if a.find('dt', attrs={'class': 'info-table__title'}).text == "Rakennuksen käyttöönottovuosi":
                # Get year
                year = a.find('dd', attrs={'class': 'info-table__value'}).text
                year = year.strip()
                year = int(year)

            if a.find('dt', attrs={'class': 'info-table__title'}).text == "Hoitovastike":
                # Get vastike
                vastike = a.find('dd', attrs={'class': 'info-table__value'}).text
                vastike = vastike.split("€")[0]
                vastike.strip()
                vastike = vastike.replace(",", ".")
                vastike = float(vastike)

    except Exception as e:
        print(e)

    appartment = Apartment(name=address, price=Price(price), area=Area(area), year=Year(
        year), vastike=Vastike(vastike), floor=Floor(floor), rooms=Rooms(rooms), zone=Zone(zone), url=url)
    apartment_list.append(appartment)

for a in apartment_list:
    print(a)

apartments = Apartments(apartment_list)
apartments.plot()
apartments.rank()