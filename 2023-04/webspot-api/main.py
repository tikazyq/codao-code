import requests
from pprint import pprint

# API endpoint
api_endpoint = 'https://webspot-zhishuyun.azurewebsites.net/api'
# api_endpoint = 'https://webspot.crawlab.net/api'
# api_endpoint = 'http://81.68.199.110:9090/api'
# api_endpoint = 'http://localhost:80/api'
# api_endpoint = 'http://localhost:19999/api'

# call API to recognize list results
res = requests.post(f'{api_endpoint}/links', json={
    # 'url': 'https://news.yahoo.com',
    # 'url': 'https://news.sina.com.cn/',
    # 'url': 'https://news.163.com',
    # 'url': 'https://www.36kr.com/information/web_news/latest/',
    # 'url': 'https://cuiqingcai.com/archives/',
    # 'url': 'http://bang.dangdang.com/books/newhotsales',
    # 'url': 'https://www.bbc.co.uk/news',
    # 'url': 'https://www.cnblogs.com/',
    # 'url': 'https://techcrunch.com/',
    # 'url': 'https://www.g3mv.com/search/lw?q=%E6%B2%A5%E9%9D%92%E8%B7%AF%E9%9D%A2&t=0&year=2023',
    'url': 'https://www.npr.org/sections/news/',
    # 'html': '<html>...</html>',
})
results = res.json()
pprint(results)
