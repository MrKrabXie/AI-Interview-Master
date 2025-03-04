from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

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

    # 将 cookies 保存到本地文件（作为缓存）
    with open('cookies_cache.json', 'w') as f:
        json.dump(cookies_dict, f)
    print("Cookies 已保存到本地缓存文件 cookies_cache.json")

except Exception as e:
    print("操作时出现错误:", e)

finally:
    driver.quit()