from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

# 初始化浏览器驱动
driver = webdriver.Chrome()

# 打开 BOSS 直聘登录页面
driver.get("https://www.zhipin.com/web/user/?ka=header-login")
time.sleep(3)

try:
    # 定位并点击切换扫码登录的按钮
    target_element = driver.find_element(By.CSS_SELECTOR, '#wrap > div > div.login-entry-page > div.login-register-content > div.btn-sign-switch.ewm-switch')
    target_element.click()
    print("成功点击元素")

    # 等待用户完成扫码登录
    input("请完成扫码登录，登录完成后按回车键继续...")

    # 获取 Selenium 中的所有 cookies
    selenium_cookies = driver.get_cookies()
    cookies_dict = {}
    for cookie in selenium_cookies:
        cookies_dict[cookie['name']] = cookie['value']
    print("获取到的 cookies:", cookies_dict)

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

    # 使用 requests 模块发送 GET 请求，并附带 Selenium 获取的 cookies
    response = requests.get(url, params=params, cookies=cookies_dict)
    print("响应状态码:", response.status_code)
    print("响应内容:", response.text)

except Exception as e:
    print("操作时出现错误:", e)

finally:
    driver.quit()
