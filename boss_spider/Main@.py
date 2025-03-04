import requests
import json
import time
import urllib.parse
import sqlite3
import os
###


# ============================
# 1. 设置 SQLite 数据库 (Set up SQLite Database)
# ============================
db_file = '../scraped_data.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 创建保存详情数据的表（如果不存在则创建）
cursor.execute('''
CREATE TABLE IF NOT EXISTS boss_interview_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    securityFormId TEXT,
    linkUrl TEXT,
    content TEXT,
    answer TEXT,
    detail_response TEXT,
    is_answer_by_ai integer default 0,
    scraped_time INTEGER
)
''')
conn.commit()

# ============================
# 2. 获取上次爬取的页码 (Determine Starting Page)
# ============================
page_file = 'last_page.txt'
if os.path.exists(page_file):
    with open(page_file, 'r') as f:
        start_page = int(f.read().strip())
else:
    start_page = 1  # 如果文件不存在则从第1页开始

# 本次运行计划爬取的页数（例如：爬取 3 页）
pages_to_scrape = 3
end_page = start_page + pages_to_scrape - 1

# ============================
# 3. 读取本地 cookies (Load Local Cookies)
# ============================
cookies_file = 'cookies_cache.json'
try:
    with open(cookies_file, 'r') as f:
        cached_cookies = json.load(f)
    print("从本地缓存文件读取到 cookies")
except FileNotFoundError:
    print("本地缓存文件未找到，无法读取 cookies")
    cached_cookies = {}

# 列表接口 URL
list_url = "https://m.zhipin.com/wapi/moment/interview/question/list"

# ============================
# 4. 循环爬取每一页 (Loop Through Each Page)
# ============================
for page in range(start_page, end_page + 1):
    current_timestamp = int(time.time() * 1000)  # 毫秒级时间戳

    params = {
        "positionCode": "100512,100507,100506,100509,100508,100511",
        "sortType": "1",
        "page": str(page),
        "_t": current_timestamp
    }

    print(f"\n正在爬取第 {page} 页数据...")
    list_response = requests.get(list_url, params=params, cookies=cached_cookies)
    print("列表接口状态码:", list_response.status_code)
    # 延迟 1 秒
    time.sleep(1)

    try:
        list_data = list_response.json()
    except json.JSONDecodeError:
        print("无法解析列表接口返回的 JSON")
        continue

    # ============================
    # 5. 处理每个条目 (Process Each Item)
    # ============================
    for item in list_data.get("zpData", {}).get("list", []):
        link_url = item.get("questionInfo", {}).get("linkUrl", "")
        content = item.get("questionInfo", {}).get("content", "")
        if not link_url:
            continue

        # 解析 link_url 中的查询参数
        parsed_link = urllib.parse.urlparse(link_url)
        query_params = urllib.parse.parse_qs(parsed_link.query)
        inner_url_encoded = query_params.get("url", [None])[0]

        if inner_url_encoded:
            inner_url = urllib.parse.unquote(inner_url_encoded)
            # 解析内部 URL 的查询参数，提取 securityFormId
            parsed_inner = urllib.parse.urlparse(inner_url)
            inner_params = urllib.parse.parse_qs(parsed_inner.query)
            securityFormId = inner_params.get("securityFormId", [None])[0]
            if not securityFormId:
                print("未找到 securityFormId")
                continue
            print("提取的 securityFormId:", securityFormId)

            # 构造详情接口的 URL
            detail_page = 1
            detail_url = f"https://m.zhipin.com/wapi/moment/interview/question/detail?securityFormId={securityFormId}&page={detail_page}&sortType=1"
            print("构造的详情接口 URL:", detail_url)

            # 发起详情接口的请求
            detail_response = requests.get(detail_url, cookies=cached_cookies)
            print("详情接口响应状态码:", detail_response.status_code)
            # 延迟 1 秒
            time.sleep(1)

            try:
                detail_json = detail_response.json()
            except json.JSONDecodeError:
                print("无法解析详情接口返回的 JSON")
                print("无法解析的数据为：", detail_response.text)
                continue

            # 根据 likeCount 选出最大的回答
            answer_list = detail_json.get("zpData", {}).get("answerList", [])
            if answer_list:
                max_answer_item = max(answer_list, key=lambda x: x.get("answer", {}).get("likeCount", 0))
                selected_answer = max_answer_item.get("answer", {}).get("content", "")
            else:
                selected_answer = ""
            # 替换 answer 中的 &nbsp 编码
            selected_answer = selected_answer.replace('&nbsp;', ' ')
            print("选取的 answer 内容:", selected_answer)

            # 替换 detail_response 中的 &nbsp 编码
            detail_response_text = detail_response.text.replace('&nbsp;', ' ')

            # 将获取的数据保存到 SQLite 数据库
            cursor.execute('''
                INSERT INTO boss_interview_questions (securityFormId, linkUrl, content, answer, detail_response, scraped_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (securityFormId, link_url, content, selected_answer, detail_response_text, int(time.time())))
            conn.commit()
            print("保存 detail 数据到数据库")
        else:
            print("未找到嵌套的 URL 参数。")

# ============================
# 6. 更新下次爬取的起始页 (Update Next Starting Page)
# ============================
new_start_page = end_page + 1
with open(page_file, 'w') as f:
    f.write(str(new_start_page))
print(f"\n更新本地页码，下一次从第 {new_start_page} 页开始爬取。")

# 关闭数据库连接
conn.close()
