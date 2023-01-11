import json

import requests
from pandas import DataFrame

base_url = 'http://m.cq.bendibao.com/news/yqdengji/fxmd_add.php'


def get_risk_areas(city: str = 'cq', level: str = '高风险', district: str = None):
    res = requests.get(
        f'{base_url}',
        params={
            'city': city,
            'level': level,
            'qu': district,
        },
    )
    return json.loads(res.content)


if __name__ == '__main__':
    data = get_risk_areas(district='江北区')
    df = DataFrame(data)
