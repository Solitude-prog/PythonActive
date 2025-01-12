import time
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.chrome.options import Options

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

class IP():
    def __init__(self, address, port, update):#
        self.address = address
        self.port = port
        self.update = update



def get_IP(pages):
    result=[]
    # 创建Chrome浏览器的选项
    options = Options()
    options.add_argument('--headless')  # 浏览器不提供可视化页面，无头模式
    options.add_argument('--disable-gpu')  # 无gpu图形化界面，提升兼容性
    options.add_argument('--no-sandbox')  # 解决在Linux下权限问题
    options.add_argument('--disable-dev-shm-usage')  # 解决资源限制问题
    options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    options.add_argument('--disable-extensions')  # 禁用所有扩展
    options.add_argument('--disable-popup-blocking')  # 禁用弹窗拦截
    options.add_argument('--disable-infobars')  # 隐藏“Chrome正在受到自动测试软件控制”的提示
    options.add_argument('--log-level=3')  # 只显示错误级别的日志
    options.add_argument('--silent')  # 静默模式
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁用控制台日志
    options.add_argument('--start-maximized')  # 最大化窗口
    options.add_argument('--window-size=100,100')  # 设置窗口大小（解决部分无头模式分辨率问题）
    options.add_argument('--remote-debugging-port=9222')  # 使用远程调试防止弹窗问题
    options.add_argument('--ignore-certificate-errors')  # 关闭ssl
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 设置ChromeDriver的路径
    chrome_driver_path = r'D:/ProgramData/driver/chromedriver/chromedriver.exe'  # 替换为你的ChromeDriver的实际路径
    # 创建Chrome浏览器的服务
    service = Service(executable_path=chrome_driver_path)
    # 初始化Chrome浏览器
    driver = webdriver.Chrome(service=service, options=options)

    for page in range(1, pages+1):
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "-----------",f"第 {page} 页的IP及端口号 开始采集")
        url = f"https://www.kuaidaili.com/free/dps/{page}"
        # 加载网页
        driver.get(url)
        time.sleep(random.uniform(0.3, 3))
        for i in range(1, 13):
            time.sleep(random.uniform(0.3, 3))
            # 使用 XPath 获取指定 tr 中的第一个 td 内容（即 IP 地址）
            address = driver.find_element(By.XPATH,f'//*[@id="table__free-proxy"]/div/table/tbody/tr[{i}]/td[1]').text.strip()
            port = driver.find_element(By.XPATH,f'//*[@id="table__free-proxy"]/div/table/tbody/tr[{i}]/td[2]').text.strip()
            update = driver.find_element(By.XPATH,f'//*[@id="table__free-proxy"]/div/table/tbody/tr[{i}]/td[8]').text.strip()
            ip=IP(address=address,port=port,update=update)
            result.append(ip)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "-----------", f"采集完成")
    return result


def check_ip(IPS):
    can_use = []
    url = "http://baidu.com"
    for ip in IPS:
        proxies = {
            'http': f"{ip.address}:{ip.port}",
            'https': f"{ip.address}:{ip.port}"
        }
        time.sleep(random.uniform(0.5, 5))
        try:
            resp = requests.get(url=url, proxies=proxies, headers=headers, timeout=3)
            print(resp.status_code)
            if resp.status_code == 200:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "------------", ip.address, ":", ip.port, "可用")
                can_use.append(ip)
        except Exception as e:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "------------", ip.address, ":", ip.port, "不可用")
    return can_use


if __name__ == '__main__':
    start = time.time()
    ips = get_IP(pages=5)
    can = check_ip(IPS=ips)
    print(can)
    duration = ((time.time() - start) / 60)
    print("代码运行时长为", '%.2f' % duration)
