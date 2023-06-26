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

class OlharDigital:
    def __init__(self):
        self.path = "C:\Program Files (x86)\chromedriver.exe"
        self.base_url = "https://olhardigital.com.br/"
        self.name = "OlharDigital"
        self.article_links = []
        self.articles = []
        self.driver = webdriver.Chrome(self.path)
        self.driver.get(self.base_url)

        # define the data we want and the structure to store it

    def get_article_links(self):
        self.driver.get(self.base_url + 'editorias/reviews')
        for page in range(1, 30):
            link_elements = self.driver.find_elements(By.XPATH, '//a[@class="card-post type8 img-effect1"]')
            for link_element in link_elements:
                href = link_element.get_attribute('href')
                self.article_links.append(href)
            self.go_to_next_page()

        return self.article_links

    def get_articles(self, save=False):
        links = self.get_article_links()
        for link in links:
            try:
                self.driver.get(link)
                # wait for page to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="post-content wp-embed-responsive"]//p')))
                print('getting article ' + link)
                article = {
                    "author": self.driver.find_element(By.XPATH, '//span[@class="autor"]/a').text,
                    "text": ' '.join([p.text for p in self.driver.find_elements(By.XPATH,
                                                                                '//div[@class="post-content wp-embed-responsive"]//p')]),
                    "link": link
                }
                self.articles.append(article)
            except Exception as e:
                print(f"Error getting article: {e}")
                continue

        if save:
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
            with open(os.path.join(data_dir, 'OlharDigital.json'), 'w') as f:
                json.dump(self.articles, f)

        return self.articles

    def go_to_next_page(self):
        try:
            next_page = self.driver.find_element(By.XPATH, '//a[@class="next page-numbers"]')
            next_page.click()
            return True
        except (NoSuchElementException, StaleElementReferenceException) as e:
            return False