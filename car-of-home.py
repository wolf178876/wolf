from selenium import webdriver
from bs4 import BeautifulSoup
import time

drivers = webdriver.Firefox()


for i in range(2,101) :
    time.sleep(5)
    url = f'https://www.che168.com/china/a0_0msdgscncgpi1ltocsp{i}exx0/?pvareaid=102179#currengpostion'
    drivers.get(url)
    htmld = drivers.page_source


    htmlx = BeautifulSoup(htmld, 'html.parser')
    datas = htmlx.select('#goodStartSolrQuotePriceCore0 >ul >li')
    # print(datas)
    od = open('e:usedcar.csv', 'a+', encoding='utf-8-SIG')
    for data in datas:
        # print(data)
        aa = data.find('a').find('div', {'class': 'cards-bottom'}).find('h4').get_text()
        # print(aa)
        bb = data.find('a').find('div', {'class': 'cards-bottom'}).find('p').get_text()
        bbb = bb.replace('万公里',' ')
        b = bbb.split('／')
        # print(b)
        cc = data.find('a').find('div', {'class': 'cards-bottom'})\
            .find('div', {'class': 'cards-price-box'})\
            .find('span', {'class': 'pirce'}).get_text()
        c = cc.replace('万',' ')
        ccc = c.replace('抢购价',' ')
        # print(c)
        od.write(aa + ',' + b[0] + ',' + b[1] + ',' + b[2] + ','+ b[3] + ','+ ccc + "\n")


