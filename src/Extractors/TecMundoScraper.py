#create a scraper for TecMundo tech articles
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import os

class TecMundo:
    def __init__(self):
        self.path = "C:\Program Files (x86)\chromedriver.exe"
        self.base_url = "https://www.tecmundo.com.br/dispositivos-moveis"
        self.name = "TecMundo"
        self.article_links = []
        self.articles = []
        self.driver = webdriver.Chrome(self.path)
        self.driver.get(self.base_url)

        #define the data we want and the structure to store it 

    def search_for_items(self, keyword=None):
        if keyword:
            self.target_search(keyword)
        # Find all the links with the class name 'tec--card__title__link'
        link_elements = self.driver.find_elements(By.CSS_SELECTOR, '.tec--list__item a.tec--card__title__link')
        # Iterate over the link elements and extract the href attribute
        for link_element in link_elements:
            #ipdb.set_trace()
            href = link_element.get_attribute('href')
            self.article_links.append(href)

        return self.article_links

    def get_articles(self, keyword=None):
        links = self.search_for_items(keyword)
        print(len(links))
        for link in links:
            self.driver.get(link)
            #grab all text from current page
            #ipdb.set_trace()
            article = {
                "title": self.driver.find_element(By.CLASS_NAME, 'tec--article__header__title').text,
                #"author": self.driver.find_element(By.CSS_SELECTOR, '').text,
                "date": self.driver.find_element(By.CLASS_NAME, 'tec--timestamp__item').text,
                "text": self.driver.find_element(By.CLASS_NAME, 'tec--article__body-grid').text,
                "link": link
            }
            self.articles.append(article)
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        with open(os.path.join(data_dir, 'TecMundo.json'), 'w') as f:
            json.dump(self.articles, f)
    
        return self.articles

    def target_search(self, keyword):
        #search for articles based on keywords
        search_bar = self.driver.find_element(By.NAME, 'q')
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)