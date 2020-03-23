import requests
from bs4 import BeautifulSoup as bs

session = requests.Session()
headers = {'accept' : '*/*',
        'user-agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
base_url = 'https://www.olx.ua/transport/legkovye-avtomobili/od/?search%5Bfilter_float_price%3Ato%5D=1200&search%5Bfilter_float_motor_year%3Afrom%5D=1995&search%5Bphotos%5D=1&page={page}&currency=USD'
cars = []

def get_html(url):
    res = session.get(url, headers=headers)
    return res.text

def get_count_pages(soup):
    pages = soup.find('div', attrs={'class':'pager rel clr'}).find_all('span', attrs={'class':'item fleft'})
    count = pages[-1].text.strip()
    return int(count)

def get_parcing(soup):
    trs = soup.find('table', attrs={'id':'offers_table'}).find_all('tr', attrs={'class':'wrap'})
    for ss in trs:
        try:
            img = ss.find('img', attrs={'class':'fleft'}).get('src')
        except:
            img = ''
        title = ss.find('a', attrs={'data-cy':'listing-ad-title'}).text.strip()
        href = ss.find('a', attrs={'data-cy':'listing-ad-title'}).get('href')
        price_S = ss.find('p', attrs={'class':'price'}).text.strip()
        place_and_date = ss.find('td', attrs={'class':'bottom-cell'}).text.strip()
        pp = place_and_date.split()
        place = ' '.join(pp[:-2])
        date = ' '.join(pp[-2:])
        cars.append({
            'img' : img,
            'title' : title,
            'href' : href,
            'price_S' : price_S,
            'place' : place,
            'date' : date,
        })

def get_cars_olx(count_cars):
    cars.clear()
    html = get_html(base_url.format(page=1))
    soup = bs(html, 'lxml')
    count_pages = get_count_pages(soup)
    page = 1
    while len(cars) < count_cars and page <= count_pages :
        html = get_html(base_url.format(page=page))
        soup = bs(html, 'lxml')
        get_parcing(soup)
        page += 1
    return cars[:count_cars]

if __name__ == '__main__':
    cars = get_cars_olx()
    print(cars)
    print(len(cars))
    