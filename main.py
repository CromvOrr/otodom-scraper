import requests
from bs4 import BeautifulSoup

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
