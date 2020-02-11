from lxml import etree
import requests
import simplejson as json
import re
from lxml import html
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

def download_from_url(url, counter):
    #url - the url to fetch dynamic content from.
    #delay - second for web view to wait
    #block_name - id of the tag to be loaded as criteria for page loaded state.
    def fetchHtmlForThePage(url, delay, block_name):
        #supply the local path of web driver.
        #in this example we use chrome driver
        browser = webdriver.Chrome('/Applications/chromedriver')
        #open the browser with the URL
        #a browser windows will appear for a little while
        browser.get(url)
        try:
        #check for presence of the element you're looking for
            element_present = EC.presence_of_element_located((By.ID, block_name))
            WebDriverWait(browser, delay).until(element_present)

        #unless found, catch the exception
        except TimeoutException:
            print ("Loading took too much time!")

        #grab the rendered HTML
        html = browser.page_source
        #close the browser
        browser.quit()
        #return html
        return html


    #call the fetching function we created
    html1 = fetchHtmlForThePage(url, 5, 're-Searchresult')
    #grab HTML document
    soup = BeautifulSoup(html1)
    tree = html.fromstring(str(soup))
    video_url = tree.xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div/div[2]/div/div[1]/video/@src')
    urllib.request.urlretrieve(video_url[0], 'video_name' + str(counter) + '.mp4')

# url = "https://www.twitch.tv/thijs/clip/AmorphousCooperativeCatNotATK"
counter = 0


urls = ["https://www.twitch.tv/thijs/clip/AmorphousCooperativeCatNotATK", "https://www.twitch.tv/nymn/clip/QuaintGeniusStarSSSsss"]
for url in urls:
    download_from_url(url, counter)
    counter += 1

