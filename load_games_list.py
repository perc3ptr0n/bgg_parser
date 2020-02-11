from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint


# global variables
choose_from = 'wishlist'  # Want in Trade, Want To Play, Want To Buy, Wishlist, The Hotness, TOP 10 by Category, TOP 100-1000 BGG etc
games_list = []
dump_path = 'games_list.txt'
username = '****'
password = '****'

chromedriver_path = './chromedriver'  # Change this to your own chromedriver path!
webdriver = webdriver.Chrome(executable_path=chromedriver_path)


def login_to_bgg(webdriver, username, password):
    sleep(1)
    webdriver.get('https://boardgamegeek.com/')
    sleep(2)
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
    last_page_num = int(
        webdriver.find_element_by_css_selector('#collection > div:nth-child(3) > span > a').text)
    for page in range(last_page_num):

        part_of_id_to_find = "results_objectname"
        elements = webdriver.find_elements_by_css_selector('[id*="%s"]' % part_of_id_to_find)

        for el in range(1, len(elements) + 1):
            game = webdriver.find_element_by_css_selector('#results_objectname%d' % el).text
            print(game)
            games_list.append(game)
    sleep(5)
# Here we could add other options

with open(dump_path, 'w') as f:
    for game in games_list:
        f.write(game + '\n')

print('Collected %d board games. Saved them to %s' % (len(games_list), dump_path))
webdriver.close()
