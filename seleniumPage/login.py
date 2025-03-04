from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 获取本地存储的Cookie和sessionStorage 、 localStorage

# 初始化浏览器驱动
driver = webdriver.Chrome()

# 打开BOSS直聘登录页面
driver.get("https://www.zhipin.com/web/user/?ka=header-login")

# 等待页面加载
time.sleep(3)

try:
    # 使用 CSS 选择器定位元素
    target_element = driver.find_element(By.CSS_SELECTOR, '#wrap > div > div.login-entry-page > div.login-register-content > div.btn-sign-switch.ewm-switch')
    # 点击元素
    target_element.click()
    print("成功点击元素")

    # 等待用户扫码登录
    input("请完成扫码登录，登录完成后按回车键继续...")

    # 打印 localStorage 中的所有值
    print("\nlocalStorage 中的所有值:")
    local_storage = driver.execute_script('return window.localStorage;')
    for key, value in local_storage.items():
        print(f"{key}: {value}")

    # 打印 sessionStorage 中的所有值
    print("\nsessionStorage 中的所有值:")
    session_storage = driver.execute_script('return window.sessionStorage;')
    for key, value in session_storage.items():
        print(f"{key}: {value}")

    # 打印浏览器的所有 cookie
    print("\n浏览器的所有 cookie:")
    cookies = driver.get_cookies()
    for cookie in cookies:
        print(cookie)

except Exception as e:
    print(f"操作时出现错误: {e}")

# 关闭浏览器
driver.quit()

"""
成功点击元素
请完成扫码登录，登录完成后按回车键继续...

localStorage 中的所有值:
boss_login_mode: app
bs_markUv: ed7fs2hZJP1740965129475
bs_markUvTime: 1741017599000
clear: {}
ft-/web/geek/job-recommend: {"fcp":607,"fmp":999,"tti":999}
getItem: {}
ka-uid: kauid-9ba0ee2HvTjR3Btk
key: {}
length: 8
removeItem: {}
setItem: {}
warlockjssdkcross: {"distinct_id":"195599ba0c62f23-0904c69e9628988-1c525636-6350400-195599ba0c74d8a","first_id":"","props":{},"identities":{}}
wd_guid: "6b22fd85-3ef8-404e-9eb4-d59d3ef8beb3"
wljssdk_cross_new_user: {"value":1,"expireTime":1741017599344}

sessionStorage 中的所有值:
bs_markUser: Ze2EfhGaYe1740965129475
clear: {}
getItem: {}
key: {}
length: 1
removeItem: {}
setItem: {}

浏览器的所有 cookie:
{'domain': '.zhipin.com', 'expiry': 1775525138, 'httpOnly': False, 'name': '__a', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '74651806.1740965127..1740965127.2.1.2.2'}
{'domain': '.zhipin.com', 'httpOnly': False, 'name': '__c', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1740965127'}
{'domain': '.zhipin.com', 'expiry': 1742065200, 'httpOnly': False, 'name': 'bst', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'V2RN0vFOz031tgXdJtzR0eLCmw7DrRxA~~|RN0vFOz031tgXdJtzR0eLCmw7DjVxw~~'}
{'domain': 'www.zhipin.com', 'expiry': 1775525138, 'httpOnly': False, 'name': 'ab_guid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'bf90cc14-1b58-491d-94c8-d66aac8669a5'}
{'domain': '.zhipin.com', 'httpOnly': False, 'name': '__g', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '-'}
{'domain': '.zhipin.com', 'expiry': 1742065200, 'httpOnly': True, 'name': 'zp_at', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'piBaFodVfGjboxsqxvy7nJrDg72MLzDpPZKxsyFMN1I~'}
{'domain': '.zhipin.com', 'expiry': 1742065200, 'httpOnly': True, 'name': 'wt2', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'DD7i9DgFp9uzyinDVYPOEIHd7-tSj2QwJTuQK9vA1mmU4S0R1-9e9r15wUBS8wb0n8g6huhuQKdc-SNsCXcmt8w~~'}
{'domain': '.zhipin.com', 'httpOnly': False, 'name': '__l', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'l=%2Fwww.zhipin.com%2Fweb%2Fuser%2F%3Fka%3Dheader-login&r=&g=&s=3&friend_source=0'}
{'domain': '.zhipin.com', 'expiry': 1742065200, 'httpOnly': True, 'name': 'wbg', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '0'}
"""