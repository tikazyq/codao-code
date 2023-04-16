from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pprint import pprint


def get_data(soup: BeautifulSoup) -> list:
    # data
    data = []

    # items
    items_elements = soup.select(list_items_selector)
    for el in items_elements:
        # row data
        row = {}

        # iterate fields
        for f in fields:
            # field name
            field_name = f['name']

            # field element
            field_element = el.select_one(f['selector'])

            # skip if field element not found
            if not field_element:
                continue

            # add field value to row
            if f['type'] == 'text':
                row[field_name] = field_element.text
            else:
                row[field_name] = field_element.attrs.get(f['attribute'])

        # add row to data
        data.append(row)

    return data


def crawl(url: str) -> list:
    # all data to crawl
    all_data = []

    while True:
        print(f'requesting {url}')

        # request url
        res = requests.get(url)

        # beautiful soup of html
        soup = BeautifulSoup(res.content)

        # add parsed data
        data = get_data(soup)
        all_data += data

        # pagination next element
        next_el = soup.select_one(next_selector)

        # end if pagination next element not found
        if not next_el:
            break

        # url of next page
        url = urljoin(url, next_el.attrs.get('href'))

    return all_data


if __name__ == '__main__':
    # API endpoint
    # api_endpoint = 'http://localhost:9999/api'
    # api_endpoint = 'https://webspot.crawlab.net/api'
    api_endpoint = 'http://localhost:80/api'

    # url to extract
    url = 'https://quotes.toscrape.com'

    # call API to recognize list page and pagination elements
    # res = requests.post(f'{api_endpoint}/requests', json={
    res = requests.post(f'{api_endpoint}/links', json={
        # 'url': 'https://quotes.toscrape.com',
        # 'url': 'https://github.com/trending',
        # 'url': 'https://github.com/search?q=spider',
        # 'url': 'https://cuiqingcai.com/archives/',
        # 'url': 'https://www.36kr.com/information/web_news/latest/',
        # 'url': 'https://news.ycombinator.com/',
        'url': 'https://news.163.com/',
    })
    results = res.json()
    pprint(results)

    # list result
    list_result = results['results']['plain_list'][0]

    # list items selector
    list_items_selector = list_result['selectors']['full_items']['selector']
    print(list_items_selector)

    # fields
    fields = list_result['fields']
    print(fields)

    # pagination next selector
    next_selector = results['results']['pagination'][0]['selectors']['next']['selector']
    print(next_selector)

    # start crawling
    all_data = crawl(url)

    # print crawled results
    pprint(all_data[:50])
