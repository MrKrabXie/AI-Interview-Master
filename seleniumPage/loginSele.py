from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 初始化浏览器驱动
driver = webdriver.Chrome()  # 如果使用其他浏览器，需相应修改

# 打开BOSS直聘登录页面
driver.get("https://www.zhipin.com/web/user/?ka=header-login")

# 等待页面加载
time.sleep(3)

# 定位并输入用户名和密码
username = driver.find_element(By.ID, "username")  # 根据实际页面的用户名输入框ID修改
password = driver.find_element(By.ID, "password")  # 根据实际页面的密码输入框ID修改

username.send_keys("your_username")  # 替换为你的用户名
password.send_keys("your_password")  # 替换为你的密码

# 模拟点击登录按钮
login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")  # 根据实际页面登录按钮的选择器修改
login_button.click()

# 等待登录完成（可根据实际情况调整等待时间）
time.sleep(5)

# 登录完成后的操作，例如获取页面信息
page_source = driver.page_source
print(page_source)

# 关闭浏览器
driver.quit()