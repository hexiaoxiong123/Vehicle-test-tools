# -*- coding: utf-8 -*-
"""
Selenium Web自动化测试示例
作者：何枭雄
日期：2021-05-10
"""

# 从 selenium 中导入 webdriver
from selenium import webdriver

def main():
    """
    基础的Selenium自动化测试示例
    """
    print("[INFO] 启动Chrome浏览器...")
    
    # 设置驱动程序
    # 注意：需要下载chromedriver并放在脚本同目录或系统PATH中
    driver = webdriver.Chrome(r'chromedriver')
    
    # 设置隐式等待时间（秒）
    driver.implicitly_wait(5)
    
    # 窗口最大化
    driver.maximize_window()
    
    # 设置打开的网址
    print("[INFO] 打开百度首页...")
    driver.get("https://www.baidu.com")
    
    # 这里可以添加更多操作，例如：
    # - 查找元素
    # - 输入文本
    # - 点击按钮
    # - 断言验证
    
    print("[INFO] 测试完成！")
    print("[INFO] 5秒后关闭浏览器...")
    
    # 等待5秒观察结果
    import time
    time.sleep(5)
    
    # 关闭浏览器
    driver.quit()

if __name__ == "__main__":
    main()

