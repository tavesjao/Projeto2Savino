from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import os
import json

class CanalTech:
    def __init__(self):
        self.path = "C:\Program Files (x86)\chromedriver.exe"
        self.base_url = "https://canaltech.com.br/"
        self.name = "CanalTech"
        self.article_links = []
        self.articles = []
        self.driver = webdriver.Chrome(self.path)
        self.driver.get(self.base_url)

        # define the data we want and the structure to store it

    def search_for_items(self, keyword=None):
        if keyword:
            self.target_search(keyword)
        link_elements = self.driver.find_elements(By.CSS_SELECTOR, '.gs-title a.gs-title')
        for link_element in link_elements:
            parsed_url = urlparse(link_element.get_attribute("href"))
            if parsed_url.netloc == "canaltech.com.br" and not parsed_url.path.startswith("/produto/oferta/") and not parsed_url.path.startswith("/produto/"):
                self.article_links.append(link_element.get_attribute("href"))
        return self.article_links

    def get_articles(self, keyword=None, save=False):
        links = self.search_for_items(keyword)
        print(len(links))
        for link in links:
            self.driver.get(link)
            article = {
                #"title": self.driver.find_element(By.XPATH, '//h1[@class="c-hjJFMH"]').text,
                #"author": self.driver.find_element(By.XPATH, '//a[@class="c-iKkIqP"]').text,
                "date": self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/main/div[1]/div[1]/section[1]/div/p/span').text,
                "text": self.driver.find_element(By.XPATH, '//div[@class="c-dWLaHV"]').text,
                "link": link,
            }
            #save article to json file in data folder
            self.articles.append(article)
        if save:
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
            with open(os.path.join(data_dir, 'CanalTech.json'), 'w') as f:
                json.dump(self.articles, f)

    def target_search(self, keyword):
        # search for articles based on keywords
        search = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/nav/nav[1]/ul[2]/li')
        search.click()
        search_bar = search.find_element(By.XPATH, '//*[@id="__next"]/div[2]/nav/nav[2]/div/form/input')
        search_bar.click()
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)

