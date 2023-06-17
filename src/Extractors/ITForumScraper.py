import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

class ITForum:
    def __init__(self):
        self.path = "C:\Program Files (x86)\chromedriver.exe"
        self.base_url = "https://itforum.com.br/colunas/"
        self.name = "ITForum"
        self.columnist_links = []
        self.articles = []
        self.driver = webdriver.Chrome(self.path)
        self.driver.get(self.base_url)

        # define the data we want and the structure to store it

    def search_for_columnists(self):
        self.driver.execute_script("window.scrollTo(0, 1000);")
        colunistas_button = self.driver.find_element(By.XPATH, '//li[@class="list-inline-item"]')
        colunistas_button.click()
        link_elements = self.driver.find_elements(By.XPATH, '//div[@class="card card-colunista mb-4"]//a')
        # Iterate over the link elements and extract the href attribute
        for link_element in link_elements:
            href = link_element.get_attribute('href')
            self.columnist_links.append(href)

        return self.columnist_links

    def get_articles(self, save=False):
        links = self.search_for_columnists()
        for link in links:
            self.driver.get(link)
            try:
                time.sleep(2)
                href = self.driver.find_elements(By.XPATH, '//div[@class="row align-items-center"]//a')
                for link_element in href:
                    article_link = link_element.get_attribute('href')
                    if any(article_link == article['link'] for article in self.articles):
                        print('Skipping duplicate article: ' + article_link)
                        continue
                    self.driver.get(article_link)
                    print('Getting article: ' + article_link)
                    author = self.driver.find_element(By.XPATH, '//div[@class="author"]')
                    text = ' '.join([p.text for p in self.driver.find_elements(By.XPATH, '//div[@class="col-12"]')])
                    article = {"author": author.text, "text": text, "link": article_link}
                    self.articles.append(article)
                    self.driver.back()
                print('Finished getting articles for columnist: ' + link)
            except:
                print('No articles found for columnist: ' + link)
                continue
        print('Finished getting articles for all columnists')
        print('Total articles: ' + str(len(self.articles)))

        if save:
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
            with open(os.path.join(data_dir, 'TecMundo.json'), 'w') as f:
                json.dump(self.articles, f)

        return self.articles