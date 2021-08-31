# Get all the Minnesota counties from Wikipedia
# and put the data in sqlite
from bs4 import BeautifulSoup
import requests
import sqlite3
import re

conn = sqlite3.connect('minnesota.sqlite3')
c = conn.cursor()

c.execute('''CREATE TABLE counties
(county text primary key,
    fips_code text,
    county_seat text,
    est int,
    origin text,
    etymology text,
    population int,
    area int)
''')

page = requests.get(
    "https://en.wikipedia.org/wiki/List_of_counties_in_Minnesota").text
soup = BeautifulSoup(page, 'lxml')
rows = soup.find('table').find('tbody').find_all('tr')
for row in rows[1:]:
    county = row.find('th').text.strip()
    td = row('td')[:-1]
    fips, seat, est, origin, etymology, population, area = [
        tag.text.strip() for tag in td]
    population = int(population.replace(',', ''))
    area = int(re.search(r'(\d+,)?\d{3}', area)[0].replace(',', ''))
    c.execute('INSERT INTO counties VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              (county, fips, seat, est, origin, etymology, population, area))
conn.commit()
c.close()
conn.close()
