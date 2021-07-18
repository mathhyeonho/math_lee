import requests
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

from datetime import datetime
today = datetime.today()
today_datetime_class_instance = today.strftime('%Y-%m-%d') # 타입이 datetime.datetime임 리스트가 아님
today_list = today_datetime_class_instance.split('-')

// dfd
class kospi_crawler:
    def __init__(self):
        self.address = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0'
        self.data = []

    def copy(self, a, b):
        driver = webdriver.Chrome(options=options)
        driver.get(self.address)
        for i in range(a, b):
            nextpage = driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/table[2]/tbody/tr/td[{0}]/a'.format(i))
            nextpage.click()
            if driver.current_url == self.address:
                continue
            else:
                self.address = driver.current_url
                print('----------')
                print(driver.current_url)
                print(self.address)
                print('----------')
                response = requests.get(self.address)
                soup = BeautifulSoup(response.content, 'html.parser')
                table = soup.find('table', {'class': 'type_2'})
                for tr in table.find_all('tr'):
                    tds = list(tr.find_all('td'))
                    for td in tds:
                        if td.find('a'):
                            point = td.find('a').text
                            price = tds[2].text
                            per = tds[10].text
                            percentage_of_foreign = tds[8].text
                            self.data.append([point, price, per if per != 'N/A' else 0, percentage_of_foreign if percentage_of_foreign != 'N/A' else 0])
        driver.quit()

    def wwww(self):
        gomi = []
        for i in range(len(self.data)):
            if i % 2 != 0:
                gomi.append(self.data[i])

        for i in gomi:
            self.data.remove(i)

        with open('/workspace/jupyter_notebook/copylist/{0}_{1}_{2}_kospi.csv'.format(today_list[0], today_list[1], today_list[2]), 'a') as file:
            file.write('point;price;per;percentage_of_foreign\n')
            for i in self.data:
                file.write('{0};{1};{2};{3}\n'.format(i[0], i[1], i[2], i[3]))

kospi_instance = kospi_crawler()
kospi_instance.copy(1, 13)
kospi_instance.copy(3, 14)
kospi_instance.copy(3, 14)
kospi_instance.copy(3, 5)
kospi_instance.wwww()

import pandas as pd
import matplotlib as mpl
import matplotlib .pyplot as plt

df = pd.read_csv('/workspace/jupyter_notebook/copylist/{0}_{1}_{2}_kospi.csv'.format(today_list[0], today_list[1], today_list[2]), index_col = 'point', sep = ';', thousands = ',')

for i, row in df.iterrows():
    if float(df.at[i, 'per']) < 0 or df.at[i, 'per'] == 0:
        df.at[i, 'per'] = 9999
        
df.sorted_by_values = df.sort_values(by = ['per'])
df.sorted_by_values.to_csv('/workspace/jupyter_notebook/copylist/{0}_{1}_{2}_kospi_sorted_by_per.csv'.format(today_list[0], today_list[1], today_list[2]))