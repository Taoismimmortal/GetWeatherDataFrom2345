

import requests
import re
import pandas as pd

# 城市和对应的areaid字典
city_id_dict = {
    "黑龙江": 50953,
    "内蒙古": 53463,
    "吉林": 54161,
    "辽宁": 54342,
    "河北": 53698,
    "天津": 54527,
    "山西": 53772,
    "陕西": 57036,
    "甘肃": 52889,
    "宁夏": 53614,
    "青海": 52866,
    "新疆": 51463,
    "西藏": 55591,
    "四川": 56294,
    "重庆": 57516,
    "山东": 54823,
    "河南": 57083,
    "江苏": 58238,
    "安徽": 58321,
    "湖北": 57494,
    "浙江": 58457,
    "福建": 58847,
    "江西": 58606,
    "湖南": 57687,
    "贵州": 57816,
    "广西": 59431,
    "海南": 59758,
    "上海": 58362,
    "广东": 59287,
    "云南": 56778,
    "台湾": 59554
}


class WeatherForecast(object):
    def __init__(self, city_id=59493, city_name=None):
        # 如果提供了城市名，优先使用城市名查找ID
        if city_name and city_name in city_id_dict:
            self.city_id = city_id_dict[city_name]
            self.city_name = city_name
        else:
            self.city_id = city_id
            self.city_name = next((name for name, id in city_id_dict.items() if id == city_id), "未知城市")

        self.url = f'https://tianqi.2345.com/Pc/GetHistory?areaInfo%5BareaId%5D={self.city_id}&areaInfo%5BareaType%5D=2&date%5Byear%5D={{0}}&date%5Bmonth%5D={{1}}'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'referer': f'https://tianqi.2345.com/wea_history/{self.city_id}.htm',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin'
        }
        self.data_list = []

    def get_content(self, url):
        res = requests.get(url=url, headers=self.headers)
        content = res.json()
        return content['data']

    def parse_data(self, content):
        result = re.compile(r'<td>(?P<date>.*?)</td>.*?<td style="color:#ff5040;">(?P<max>.*?)</td>'
                            r'.*?<td style="color:#3097fd;" >(?P<min>.*?)</td>.*?<td>(?P<weather>.*?)</td>'
                            r'.*?<td>(?P<cloud>.*?)</td>.*?<td><span class="history-aqi wea-aqi.*?>(?P<sky>.*?)</span></td>',
                            re.S)
        find_result = result.finditer(content)
        for it in find_result:
            data_dict = it.groupdict()
            self.data_list.append(data_dict)
        return self.data_list

    def write_csv(self, filename=None):
        if not filename:
            filename = f'./{self.city_name}_{min(y for y, m in self._time_range)}-{max(y for y, m in self._time_range)}.csv'
        df = pd.DataFrame(self.data_list)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f'数据已保存到 {filename}')
        return df

    def run(self, start_year=2019, end_year=2021, start_month=1, end_month=12):
        self.data_list = []  # 清空之前的数据
        self._time_range = []  # 记录爬取的时间范围

        for year in range(start_year, end_year + 1):
            s_month = start_month if year == start_year else 1
            e_month = end_month if year == end_year else 12

            for month in range(s_month, e_month + 1):
                self._time_range.append((year, month))
                url = self.url.format(year, month)
                print(f'正在爬取{self.city_name}第{year}年{month}月的天气!')
                try:
                    content = self.get_content(url)
                    self.parse_data(content)
                except Exception as e:
                    print(f"爬取{year}年{month}月数据时出错: {e}")

        print('全部爬取完毕!')
        return self.data_list


# 示例用法
if __name__ == '__main__':
    # 方式1：直接使用城市ID
    weather1 = WeatherForecast(city_id=59493)
    weather1.run(2020, 2021, 1, 12)
    weather1.write_csv()

    print("可用城市列表：")
    for city, city_id in city_id_dict.items():
        print(f"{city}: {city_id}")