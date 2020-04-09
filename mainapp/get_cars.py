import requests
from bs4 import BeautifulSoup as bs

session = requests.Session()
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
           }
cars = []
PRICE = 1200


def get_soup(url):
    res = session.get(url, headers=headers)
    soup = bs(res.text, 'lxml')
    return soup


def olx_count_pages(soup):
    pages = soup.find('div', attrs={'class': 'pager rel clr'}).find_all('span', attrs={'class': 'item fleft'})
    count = pages[-1].text.strip()
    return int(count)


def rst_count_pages(soup):
    pages = soup.find('div', attrs={'class': 'results-pager'}).find('ul', attrs={'class': 'pagination'}).find_all('li')
    return len(pages)


def olx_parcing(soup):
    trs = soup.find('table', attrs={'id': 'offers_table'}).find_all('tr', attrs={'class': 'wrap'})
    for ss in trs:
        try:
            img = ss.find('img', attrs={'class': 'fleft'}).get('src')
        except:
            img = ''
        title = ss.find('a', attrs={'data-cy': 'listing-ad-title'}).text.strip()
        href = ss.find('a', attrs={'data-cy': 'listing-ad-title'}).get('href')
        price_S = ss.find('p', attrs={'class': 'price'}).text.strip()
        place_and_date = ss.find(
            'td', attrs={'class': 'bottom-cell'}).text.strip()
        pp = place_and_date.split()
        place = ' '.join(pp[:-2])
        date = ' '.join(pp[-2:])
        cars.append({
            'img': img,
            'title': title,
            'href': href,
            'price_S': price_S,
            'place': place,
            'date': date,
        })


def autoria_parcing(soup):
    sections = soup.find_all('section', attrs={'class': 'ticket-item'})
    for ss in sections:
        try:
            img = ss.find('img', attrs={'class': 'm-auto'}).get('src')
        except:
            img = ''
        title = ss.find('div', attrs={'class': 'item ticket-title'}).text.strip()
        href = ss.find('a', attrs={'class': 'address'}).get('href')
        price_S = ss.find('span', attrs={'data-currency': 'USD'}).text + ' $ '
        place = ss.find('li', attrs={'class': 'view-location'}).text.strip()
        date = ss.find('div', attrs={'class': 'footer_ticket'}).text.strip()
        # definition_data = ss.find('div', attrs={'class': 'definition-data'})
        cars.append({
            'img': img,
            'title': title,
            'href': href,
            'price_S': price_S,
            'place': place,
            'date': date,
        })


def rst_parcing(soup):
    divs = soup.find_all('div', attrs={'class': 'rst-ocb-i'})
    for dd in divs:
        try:
            img = dd.find('img', attrs={'class': 'rst-ocb-i-i'}).get('src')
        except:
            continue
        title = dd.find('h3', attrs={'class': 'rst-ocb-i-h'}).text.strip()
        href = '//rst.ua' + dd.find('a', attrs={'class': 'rst-ocb-i-a'}).get('href')
        try:
            price_S = dd.find('li', attrs={'class': 'rst-ocb-i-d-l-i'}).find('span', attrs={'class': 'rst-uix-grey'}).text.strip()
        except:
            price_S = 'не указано'
        place = dd.find('li', attrs={'class': 'rst-ocb-i-d-l-j'}).find('span', attrs={'class': 'rst-ocb-i-d-l-i-s'}).text.strip()
        d = dd.find('div', attrs={'class': 'rst-ocb-i-s'})
        span = d.select_one('span')
        span.clear()
        date = dd.find('div', attrs={'class': 'rst-ocb-i-s'}).text.strip()
        # definition_data = dd.find('div', attrs={'class': 'definition-data'})
        cars.append({
            'img': img,
            'title': title,
            'href': href,
            'price_S': price_S,
            'place': place,
            'date': date,
        })


def get_olx(count_cars):
    cars.clear()
    base_url = 'https://www.olx.ua/transport/legkovye-avtomobili/od/?search%5Bfilter_float_price%3Ato%5D={price}&search%5Bfilter_float_motor_year%3Afrom%5D=1995&search%5Bphotos%5D=1&page={page}&currency=USD'
    count_pages, page = 1, 1
    while len(cars) < count_cars and page <= count_pages:
        soup = get_soup(base_url.format(price=PRICE, page=page))
        if page == 1:
            count_pages = olx_count_pages(soup)
        olx_parcing(soup)
        page += 1
    return cars[:count_cars]


def get_autoria(count_cars):
    cars.clear()
    base_url = 'https://auto.ria.com/search/?year[0].gte=1995&categories.main.id=1&region.id[0]=12&price.USD.lte={price}&price.currency=1&abroad.not=0&custom.not=-1&damage.not=1&spareParts=0&photos.all.id.gte=1&dates.sold.not=0000-00-00%2000:00:00&page={page}&size=100'
    count_pages, page = 1, 1
    while len(cars) < count_cars and page <= count_pages:
        soup = get_soup(base_url.format(price=PRICE, page=page-1))
        autoria_parcing(soup)
        page += 1
    return cars[:count_cars]


def get_rst(count_cars):
    cars.clear()
    base_url = 'http://rst.ua/ukr/oldcars/odessa/?make[]=0&price[]=101&price[]={price}&year[]=1995&year[]=0&condition=1,2&engine[]=0&engine[]=0&fuel=0&gear=0&drive=0&results=4&saled=1&notcust=&sort=1&city=0&from=sform&start={page}'
    page = 1
    while len(cars) < count_cars:
        soup = get_soup(base_url.format(price=PRICE, page=page))
        rst_parcing(soup)
        page += 1
    return cars[:count_cars]


if __name__ == '__main__':
    cars = get_olx(10)
    print(cars)
    print(len(cars))
