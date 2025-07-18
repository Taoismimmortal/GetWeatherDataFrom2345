# GetWeatherDataFrom2345
气象数据爬虫，可自定义城市，自定义时间获取天气数据，最新版2025
# 天气历史数据爬虫

这是一个用于抓取天气网站历史天气数据的Python爬虫工具。通过这个工具，您可以轻松获取中国各省份的历史天气数据，并将其保存为CSV格式文件进行后续分析。

## 功能特点

- 支持全国31个省级行政区的天气数据抓取
- 可自定义时间范围（年份和月份）
- 支持通过城市名称或城市ID获取数据
- 自动将数据保存为CSV格式，方便后续分析处理
- 包含日期、最高温度、最低温度、天气状况、云量和空气质量等信息

## 使用方法

### 基本用法

```python
from GetWeatherDataFrom2345 import WeatherForecast

# 方式1：使用城市ID
weather = WeatherForecast(city_id=59493)
weather.run(2020, 2021, 1, 12)  # 抓取2020年1月到2021年12月的数据
weather.write_csv()  # 保存为CSV

# 方式2：使用城市名称
weather = WeatherForecast(city_name="北京")
weather.run(2019, 2021)  # 使用默认时间范围：2019年1月到2021年12月
weather.write_csv("北京历史天气.csv")  # 指定文件名保存

city_id：城市ID，默认为59493
city_name：城市名称，优先于city_id使用
start_year/end_year：开始/结束年份
start_month/end_month：开始/结束月份

城市id可以自由扩展，自己去2345天气网站看url的id编号
比如：https://tianqi.2345.com/wea_history/54511.htm   这是北京的

依赖库
requests
pandas
