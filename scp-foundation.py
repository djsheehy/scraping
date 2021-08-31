# Get all the SCPs
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import redis

r = redis.Redis()
for series in range(1, 7):
    url = "http://scp-wiki.wikidot.com/scp-series"
    if series > 1:
        url += f"-{series}"
    with urlopen(url) as page:
        soup = BeautifulSoup(page, 'lxml')
        links = soup.find_all(
            'a', attrs={'href': re.compile('/scp-[0-9]{3,4}')})
        for a in links:
            name = a.string
            if a.next_sibling is None:
                continue
            if a.class_ == 'newpage':
                continue
            value = a.next_sibling.string[3:]
            r.hset('scps', name, value)
