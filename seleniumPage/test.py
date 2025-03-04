from selenium import webdriver
from selenium.webdriver.common.by import By
import time

## 切换元素
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
    # 可以在这里添加后续操作，比如等待一段时间查看点击效果
    time.sleep(5)

except Exception as e:
    print(f"点击元素时出现错误: {e}")

# 关闭浏览器
driver.quit()