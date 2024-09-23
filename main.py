import requests
from bs4 import BeautifulSoup
import pandas as pd
import figures

# otodom.pl -> type: apartments for sale -> location: Kraków -> building type: house
url = (
    'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/malopolskie/krakow/krakow/krakow?limit=36'
    '&ownerTypeSingleSelect=ALL&buildingType=%5BHOUSE%5D&by=DEFAULT&direction=DESC&viewType=listing')

resp = requests.get(f'{url}', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 '
                  'Safari/537.36'})
initial_page = BeautifulSoup(resp.content, 'html.parser')
total_listings = initial_page.find(class_='css-15svspy ezcytw17')
total_listings = int(total_listings.text.split()[-1])

pages = []
for page in range(1, 5):  # 4 pages available
    print(f'Loading page No. {page}')
    response = requests.get(f'{url}{page}', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/123.0.0.0 Safari/537.36'})
    processed_page = BeautifulSoup(response.content, 'html.parser')
    pages.append(processed_page)

listings = []
for page in pages:
    listings += page.find_all(class_='css-136g1q2 eeungyz0')

it = len(listings)
while it > total_listings:
    del listings[-1]  # deleting unwanted ads
    it -= 1

districts = [
    'Bieńczyce', 'Bieżanów-Prokocim', 'Bronowice', 'Czyżyny', 'Dębniki', 'Grzegórzki', 'Krowodrza',
    'Łagiewniki-Borek Fałęcki', 'Mistrzejowice', 'Nowa Huta', 'Podgórze', 'Podgórze Duchackie', 'Prądnik Biały',
    'Prądnik Czerwony', 'Stare Miasto', 'Swoszowice', 'Wzgórza Krzesławickie', 'Zwierzyniec'
]

houses = []
for listing in listings:
    house = {'title': listing.find(class_='css-u3orbr e1g5xnx10').text.strip()}

    class_name = 'css-12dsp7a e1clni9t1'
    rooms = listing.find(class_=class_name).text.strip()
    beg_idx = rooms.find('pokoi') + 5
    house['rooms'] = int(rooms[beg_idx:beg_idx + 1])

    area = listing.find(class_=class_name).text.strip()
    beg_idx = area.find('chnia') + 5
    end_idx = area.find('m²')
    house['area [m2]'] = float(area[beg_idx:end_idx])

    price_per_m2 = listing.find(class_=class_name).text.strip()
    beg_idx = price_per_m2.find('y') + 1
    end_idx = price_per_m2.find('zł')
    house['price per m2 [PLN]'] = int(price_per_m2[beg_idx:end_idx].replace('\xa0', '').replace(' ', ''))

    total_price = listing.find(class_='css-2bt9f1 evk7nst0').text.strip().replace('\xa0', '').replace(' ', '').replace(
        'zł', '')
    if ',' in total_price:
        total_price = total_price[:total_price.index(',')]
    house['total price [PLN]'] = int(total_price)

    try:
        vendor_type = listing.find(class_='css-120nera es3mydq0').text
        beg_idx = vendor_type.find('Oferta prywatna')
        if beg_idx == -1:
            beg_idx = vendor_type.find('Biuro nieruchomości')
            if beg_idx == -1:
                house['vendor type'] = 'Deweloper'
            else:
                house['vendor type'] = 'Biuro nieruchomości'
        else:
            house['vendor type'] = 'Oferta prywatna'
    except (AttributeError, TypeError):
        house['vendor type'] = 'ERROR 100'

    district = listing.find(class_='css-42r2ms eejmx80').text.strip()
    for d in districts:
        if d in district:
            house['district'] = d.upper()
            break
        house['district'] = 'KRAKÓW-OBRZEŻA'

    houses.append(house)

df = pd.DataFrame(houses)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(df)

df_by_district = df.groupby('district').size().to_frame()
df_by_district.columns = ['qty']
df_by_district_dsc = df_by_district.sort_values('qty', ascending=False)
print(df_by_district_dsc)

figures.show(df, df_by_district)
