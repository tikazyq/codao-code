from typing import List, Dict

from pandas import read_csv, concat

from utils import *


class Crawler(object):
    city: str = None
    sub_list: List[Dict] = None

    def __init__(self, city: str = None):
        self.city = city
        self.sub_list = get_sub_list(self.city)

    def download_area_trend_data(self):
        # city
        city = self.city

        # dataframes
        df_daily = DataFrame([])
        df_monthly = DataFrame([])

        for sub_item in self.sub_list:
            # area
            area = sub_item.get('city')

            # download and get output paths
            out_path_daily, out_path_monthly = download_area_trend_data(city, area)

            # daily
            _df_daily = read_csv(out_path_daily)
            _df_daily['city'] = city
            _df_daily['area'] = area
            df_daily = concat((df_daily, _df_daily))

            # monthly
            _df_monthly = read_csv(out_path_monthly)
            _df_monthly['city'] = city
            _df_monthly['area'] = area
            df_monthly = concat((df_monthly, _df_monthly))

        # current date
        date = datetime.now().strftime('%Y%m%d')

        # save daily
        all_dir_path_daily = f'./data/trend/city/daily/{date}'
        if not os.path.exists(all_dir_path_daily):
            os.makedirs(all_dir_path_daily)
        all_out_path_daily = f'{all_dir_path_daily}/{city}-{date}.csv'
        df_daily.to_csv(all_out_path_daily, index=False)

        # save monthly
        all_dir_path_monthly = f'./data/trend/city/monthly/{date}'
        if not os.path.exists(all_dir_path_monthly):
            os.makedirs(all_dir_path_monthly)
        all_out_path_monthly = f'{all_dir_path_monthly}/{city}-{date}.csv'
        df_monthly.to_csv(all_out_path_monthly, index=False)

    def download_area_summary_data(self):
        download_sub_list(self.city)

    def run(self):
        self.download_area_trend_data()
        self.download_area_summary_data()
