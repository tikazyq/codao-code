import json
import os.path
from datetime import datetime
from typing import Dict, List

import requests
from bs4 import BeautifulSoup as bs
from pandas import DataFrame, to_datetime, read_csv

base_url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia'


def get_root_data(city: str = None) -> Dict:
    if city is not None:
        url = f'{base_url}?city={city}'
    else:
        url = base_url
    headers = {
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'BIDUPSID=51E8DEC2904C536E430382B402B6FC88; PSTM=1650256092; BAIDUID=51E8DEC2904C536EB6B871A9371414F1:FG=1; BDUSS=Q0M2xDR3RLbW1RbWx0TWlkakhFTDFlNDN6LURzNHJ0NlNuY3FkQUdPMExHR2xqSVFBQUFBJCQAAAAAAAAAAAEAAAB9-yYAdGlrYXp5cQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAuLQWMLi0FjUm; BDUSS_BFESS=Q0M2xDR3RLbW1RbWx0TWlkakhFTDFlNDN6LURzNHJ0NlNuY3FkQUdPMExHR2xqSVFBQUFBJCQAAAAAAAAAAAEAAAB9-yYAdGlrYXp5cQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAuLQWMLi0FjUm; H_PS_PSSID=36544_37767_37777_37724_37794_37663_37538_37674_37743_26350_37791; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=51E8DEC2904C536EB6B871A9371414F1:FG=1; PSINO=7; delPer=0; BA_HECTOR=84010l84250485048k010lnn1hnemsb1e; ZFY=86SqNbEO0rQBp65mF9lQXPy:BASpbF16aQaXcrO:BzyJ8:C',
        'referer': 'https://voice.baidu.com/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    res = requests.get(url, headers=headers)
    soup = bs(res.content, features='html.parser')
    return json.loads(soup.select('#captain-config')[0].text)


def get_sub_list(city: str) -> List[Dict]:
    data = get_root_data(city)
    data.get('component')[0].get('caseList')
    sub_list = list(filter(lambda c: c.get('area') == city, data.get('component')[0].get('caseList')))[0].get('subList')
    return sub_list


def get_sub_list_df(city: str) -> DataFrame:
    sub_list = get_sub_list(city)
    df = DataFrame(sub_list)
    df = df.drop(['dangerousAreas'], axis=1)
    df = df.rename({'city': 'area'}, axis=1)
    return df


def download_sub_list(city: str) -> str:
    df = get_sub_list_df(city)
    date = datetime.now().strftime('%Y%m%d')
    out_dir_path = f'./data/summary/city/{city}/{date}'
    if not os.path.exists(out_dir_path):
        os.makedirs(out_dir_path)
    out_path = f'{out_dir_path}/{city}-{date}.csv'
    df.to_csv(out_path, index=False)
    return out_path


def get_root_trend_data(city: str, area: str = None) -> Dict[str, List[Dict]]:
    if area is None:
        area = city
    data = get_root_data(f'{city}-{area}')
    trend_data = data.get('component')[0].get('trend')
    return trend_data


def get_root_trend_data_df(city: str, area: str = None) -> DataFrame:
    if area is None:
        area = city
    trend_data = get_root_trend_data(city, area)
    date_data = to_datetime(list(map(lambda date: f'2022.{date}', trend_data.get('updateDate'))))
    df = DataFrame(date_data, columns=['date'])
    for m in trend_data.get('list'):
        name: str = m.get('name')
        data: List[int] = m.get('data')
        df[name] = data
    return df


def download_root_trend_data(city: str, area: str = None):
    if area is None:
        area = city
    df = get_root_trend_data_df(city, area)
    date = datetime.now().strftime('%Y%m%d')
    out_dir_path = f'./data/trend/root/{date}'
    if not os.path.exists(out_dir_path):
        os.makedirs(out_dir_path)
    df.to_csv(f'./data/{city}-{area}-{date}.csv', index=False)


def get_area_trend_data(city: str, area: str = None) -> Dict:
    if area is None:
        area = city
    url = f'https://voice.baidu.com/newpneumonia/getv2?from=mola-virus&stage=publish&target=trendCity&area={city}-{area}'
    res = requests.get(url)
    data = json.loads(res.content)
    return data.get('data')[0]


def get_area_trend_data_df(city: str, area: str = None) -> (DataFrame, DataFrame):
    # all trend data
    data = get_area_trend_data(city, area)

    # daily dataframe
    trend_data_daily = data.get('trend')
    date_data = to_datetime(list(map(lambda date: f'2022.{date}', trend_data_daily.get('updateDate'))))
    df_daily = DataFrame(date_data, columns=['date'])
    for m in trend_data_daily.get('list'):
        name: str = m.get('name')
        metric_data: List[int] = m.get('data')
        padded_metric_data = (df_daily.shape[0] - len(metric_data)) * [0] + metric_data
        df_daily[name] = padded_metric_data

    # monthly dataframe
    trend_data_monthly = data.get('trendMonth')
    month_data = to_datetime(list(map(lambda month: f'{month}.01', trend_data_monthly.get('updateMonth'))))
    df_monthly = DataFrame(month_data, columns=['date'])
    for m in trend_data_monthly.get('list'):
        name: str = m.get('name')
        metric_data: List[int] = m.get('data')
        padded_metric_data = (df_monthly.shape[0] - len(metric_data)) * [0] + metric_data
        df_monthly[name] = padded_metric_data

    return df_daily, df_monthly


def download_area_trend_data(city: str, area: str = None) -> (str, str):
    if area is None:
        area = city

    # dataframes
    df_daily, df_monthly = get_area_trend_data_df(city, area)

    # current date
    date = datetime.now().strftime('%Y%m%d')

    # save daily data
    dir_path_daily = f'./data/trend/area/daily/{city}/{date}'
    out_path_daily = f'{dir_path_daily}/{city}-{area}-{date}.csv'
    if not os.path.exists(dir_path_daily):
        os.makedirs(dir_path_daily)
    df_daily.to_csv(out_path_daily, index=False)

    # save monthly data
    dir_path_monthly = f'./data/trend/area/month/{city}/{date}'
    out_path_monthly = f'{dir_path_monthly}/{city}-{area}-{date}.csv'
    if not os.path.exists(dir_path_monthly):
        os.makedirs(dir_path_monthly)
    df_monthly.to_csv(out_path_monthly, index=False)

    return out_path_daily, out_path_monthly


def download_github_covid_time_series_data():
    # current date
    date = datetime.now().strftime('%Y%m%d')
    df_confirmed_global = read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    df_deaths_global = read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    df_recovered_global = read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

