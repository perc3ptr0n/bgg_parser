from selenium import webdriver
from time import sleep
import pandas as pd

chromedriver_path = './chromedriver'  # Change this to your own chromedriver path!
webdriver = webdriver.Chrome(executable_path=chromedriver_path)

dump_path = 'games_info.csv'
games_columns = ['game_name', 'link_on_bgg', 'game_id']
offers_columns = ['offer_name', 'link_to_offer', 'price', 'country', 'placed', 'condition']

games_table = pd.read_csv(dump_path, usecols=games_columns)
offers_table = pd.DataFrame(columns=offers_columns)
offers_path = 'offers_info.csv'

games = list(games_table['game_id'])
for id in games[:3]:
    link = 'https://boardgamegeek.com/boardgame/%s/' % str(id)
    webdriver.get(link)
    sleep(1)
    current_url = webdriver.current_url

    page_number = 1
    while(True):
        next_url = current_url + '/marketplace/geekmarket?pageid=%d' % page_number
        webdriver.get(next_url)
        sleep(1)
        current_page = int(webdriver.current_url.split('=')[-1])

        if current_page != page_number:
            break

        offers_list = webdriver.find_element_by_css_selector('#mainbody > div > div.global-body-content.pending.ready > div.content.ng-isolate-scope > div:nth-child(2) > ng-include > div > div > ui-view > ui-view > div > div > div.col-table-primary > div > geekmarket-tab-module > div > div.panel-body > ul')
        items = offers_list.find_elements_by_tag_name("li")
        for item in items:
            item_info = item.text.split('\n')

            price = item_info[0]
            condition = item_info[1].split(' ')[0]

            country_image = item.find_element_by_xpath('//a/div[1]/img')
            img_src = country_image.get_attribute('ng-src')
            country = img_src.split('/')[-1].split('_')[1].split('.')[0]

            offer_name = item.find_element_by_css_selector('a > div.summary-item-title').text.split(' ')[1:]
            offer_name = ' '.join(map(str, offer_name))

            placed = item.find_element_by_css_selector('a > div.summary-item-meta.ng-binding').text

            link = item.find_element_by_css_selector('a')
            link = link.get_attribute("href")
            print(link)

            offer_record = [offer_name, link, price, country, placed, condition]
            new_record = pd.DataFrame([offer_record[:]], columns=offers_columns)
            offers_table = offers_table.append([new_record], ignore_index=True)

        page_number += 1


offers_table.to_csv(offers_path, mode='w', header=True)
webdriver.close()