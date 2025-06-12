import requests
from bs4 import BeautifulSoup
import re
import os
import urllib3

# 禁用因跳过SSL验证而产生的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 目标URL列表
urls = ['https://monitor.gacjie.cn/page/cloudflare/ipv4.html', 
        'https://ip.164746.xyz'
        ]

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 创建一个文件来存储IP地址
with open('ip.txt', 'w', encoding='utf-8') as file:
    for url in urls:
        try:
            # 发送HTTP请求获取网页内容
            # 添加 verify=False 解决 SSL 错误, 添加 timeout 防止卡死
            response = requests.get(url, verify=False, timeout=10)
            response.raise_for_status() # 检查请求是否成功
            
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 根据网站的不同结构找到包含IP地址的元素
            if url == 'https://monitor.gacjie.cn/page/cloudflare/ipv4.html':
                elements = soup.find_all('tr')
            elif url == 'https://ip.164746.xyz':
                elements = soup.find_all('tr')
            else:
                elements = soup.find_all('li')
            
            # 遍历所有元素,查找IP地址
            for element in elements:
                element_text = element.get_text()
                ip_matches = re.findall(ip_pattern, element_text)
                
                # 如果找到IP地址,则写入文件
                for ip in ip_matches:
                    file.write(ip + '\n')
        except requests.exceptions.RequestException as e:
            print(f"无法获取URL: {url}, 错误: {e}")

print('IP地址已保存到ip.txt文件中。')
