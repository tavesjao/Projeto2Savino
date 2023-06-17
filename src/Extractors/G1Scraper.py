
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class G1:
    def __init__(self):
        self.path = "C:\Program Files (x86)\chromedriver.exe"
        self.base_url = "https://g1.globo.com/busca"
        self.name = "G1"
        self.article_links = []
        self.articles = []
        self.driver = webdriver.Chrome(self.path)
        self.driver.get(self.base_url)

        #define the data we want and the structure to store it

    def search_for_items(self, keyword=None):
        if keyword:
            self.target_search(keyword)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@class="widget widget--card widget--info"]//a')))
        link_elements = self.driver.find_elements(By.XPATH, '//li[@class="widget widget--card widget--info"]//a')
        for link_element in link_elements:
            href = link_element.get_attribute('href')
            self.article_links.append(href)

        return self.article_links

    def get_articles(self, keyword=None):
        links = self.search_for_items(keyword)
        print(len(links))
        for link in links:
            self.driver.get(link)
            article = {
                #"author": self.driver.find_element(By.XPATH, '//p[@class="content-publication-data__from"]').text,
                #get text and join it in a single string
                "text": ' '.join([p.text for p in self.driver.find_elements(By.XPATH, '//p[@class="content-text__container "]')]),
                "link": link
            }
            self.articles.append(article)
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        with open(os.path.join(data_dir, 'G1.json'), 'w') as f:
            json.dump(self.articles, f)

        return self.articles

    def target_search(self, keyword):
        #search for articles based on keywords
        search_bar = self.driver.find_element(By.NAME, 'q')
        search_bar.click()
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)



