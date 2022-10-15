import requests
from bs4 import BeautifulSoup


def main():
    res = requests.get('https://github.com/trending')
    sel = BeautifulSoup(res.content)
    rows = sel.select('article.Box-row')
    for row in rows:
        try:
            repo_name = '/'.join(map(lambda x: x.strip(), row.select('h1 a')[0].text.strip().split('/')))
        except IndexError:
            repo_name = ''
        try:
            description = row.select('p')[0].text.strip()
        except IndexError:
            description = ''
        try:
            stars = row.select('a.Link--muted')[0].text.strip()
        except IndexError:
            stars = ''
        print(f'{repo_name} ({stars} stars): {description}')


if __name__ == '__main__':
    main()
