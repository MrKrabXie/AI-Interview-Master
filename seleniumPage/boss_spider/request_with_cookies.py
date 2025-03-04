import requests
import json
import time

# 构造关键接口的请求 URL 和查询参数
url = "https://m.zhipin.com/wapi/moment/interview/question/list"
# 生成当前时间戳（毫秒级）
current_timestamp = int(time.time() * 1000)

params = {
    "positionCode": "100512,100507,100506,100509,100508,100511",
    "sortType": "1",
    "page": "3",
    "_t": current_timestamp
}

# 从本地文件读取 cookies
try:
    with open('cookies_cache.json', 'r') as f:
        cached_cookies = json.load(f)
    print("从本地缓存文件读取到 cookies")
except FileNotFoundError:
    print("本地缓存文件未找到，无法读取 cookies")
    cached_cookies = {}

# 使用 requests 模块发送 GET 请求，并附带 Selenium 获取的 cookies
response = requests.get(url, params=params, cookies=cached_cookies)
print("响应状态码:", response.status_code)
print("响应内容:", response.text)