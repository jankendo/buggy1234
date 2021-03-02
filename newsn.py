from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
def get_comment():
    diclist = []
    url = 'https://zaif.jp/instant_exchange/currency#btc'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    i = 0
    for h2 in driver.find_elements_by_tag_name('[class="content"]'):
        diclist.append(h2.text)
    driver.close()
    return(diclist)

if __name__ == '__main__':
    a = get_comment()
    print(a)