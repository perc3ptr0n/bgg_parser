from time import sleep
import pandas as pd
from selenium import webdriver

# global variables
choose_from = 'wishlist'  # Want in Trade, Want To Play, Want To Buy, Wishlist, The Hotness, TOP 10 by Category, TOP 100-1000 BGG etc
columns = ['game_name', 'link_on_bgg', 'game_id']
games_table = pd.DataFrame(columns=columns)
dump_path = 'games_info.csv'
username = '****'  # enter here your username for BGG
password = '****'  # enter here your password for BGG

chromedriver_path = './chromedriver'  # Change this to your own chromedriver path!
webdriver = webdriver.Chrome(executable_path=chromedriver_path)


def login_to_bgg(webdriver, username, password):
    sleep(1)
    webdriver.get('https://boardgamegeek.com/')
    sleep(1)
    sign_in_selector = '#global-header-outer > header > nav > div > div.global-header-nav > div > div.global-header-nav-primary-wrapper > ul > li.global-header-nav-session.global-header-nav-primary-separated.ng-scope > button'

    button_sign_in = webdriver.find_element_by_css_selector(sign_in_selector)
    button_sign_in.click()
    sleep(1)

    username_el = webdriver.find_element_by_name('username')
    username_el.send_keys(username)
    password_el = webdriver.find_element_by_name('password')
    password_el.send_keys(password)
    button_login = webdriver.find_element_by_css_selector(
        'body > div.modal.fade.ng-scope.ng-isolate-scope.in > div > div > form > div.modal-footer > button')
    button_login.click()


login_to_bgg(webdriver, username, password)

if choose_from == 'wishlist':
    link = 'https://boardgamegeek.com/wishlist/%s' % username
    webdriver.get(link)
    sleep(5)
    last_page_num = int(webdriver.find_element_by_css_selector('#collection > div:nth-child(3) > span > a').text)
    for page in range(last_page_num):

        part_of_id_to_find = "results_objectname"
        elements = webdriver.find_elements_by_css_selector('[id*="%s"]' % part_of_id_to_find)

        for el in range(1, len(elements) + 1):
            game = webdriver.find_element_by_css_selector('#results_objectname%d' % el).text
            link = webdriver.find_element_by_css_selector('#results_objectname%d > a' % el)
            href = link.get_attribute("href")
            game_id = href.split('/')[-2]
            game_record = [game, href, game_id]
            new_record = pd.DataFrame([game_record[:]], columns=columns)
            games_table = games_table.append([new_record], ignore_index=True)
    sleep(3)
# Here we could add other options
games_table.to_csv(dump_path, mode='w', header=True)

print('Collected %d board games. Saved them to %s' % (games_table.shape[0], dump_path))
webdriver.close()
