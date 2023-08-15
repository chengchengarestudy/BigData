import time
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import random

options = webdriver.EdgeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.41')
driver = webdriver.Edge(options=options)

driver.get('https://login.taobao.com/member/login.jhtml')
driver.maximize_window()
number_1 = random.uniform(10, 20)
time.sleep(number_1)

header = {"name": "商品名称", "price": "商品价格", "deal": "商品销量"}
products = []

for page in range(0, 30):
    url = "https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=" + str(44*page)
    driver.get(url)
    number_2 = random.uniform(3, 7)
    time.sleep(number_2)

    page_source = driver.page_source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    target_elements = soup.select("#mainsrp-itemlist div:nth-child(1)")

    n = 45

    for i in range(1, n):
        name = soup.select("#mainsrp-itemlist > div > div > div:nth-child(1) > div:nth-child(" + str(i) + ") > div.ctx-box.J_MouseEneterLeave.J_IconMoreNew > div.row.row-2.title")
        product_name = name[0].text.strip()

        price = soup.select("#mainsrp-itemlist > div > div > div:nth-child(1) > div:nth-child(" + str(i) + ") > div.ctx-box.J_MouseEneterLeave.J_IconMoreNew > div.row.row-1.g-clearfix > div.price.g_price.g_price-highlight")
        product_price = price[0].text.strip()

        deal = soup.select("#mainsrp-itemlist > div > div > div:nth-child(1) > div:nth-child(" + str(i) + ") > div.ctx-box.J_MouseEneterLeave.J_IconMoreNew > div.row.row-1.g-clearfix > div.deal-cnt")
        product_deal = deal[0].text

        products.append(
            {header["name"]: product_name, header["price"]: product_price, header["deal"]: product_deal})

        print(
            "商品名称:" + product_name + "\n" + "商品价格:" + product_price + "\n" + "商品数量:" + product_deal + "\n")

keys = products[0].keys()
with open('电商分析.csv', 'w', newline='', encoding='utf-8-sig') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(products)

driver.quit()
