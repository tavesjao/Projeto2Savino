#create a scraper for TecMundo tech articles
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import ipdb

class TecMundo:
    def __init__(self):
        self.base_url = "https://www.tecmundo.com.br/dispositivos-moveis"
        self.name = "TecMundo"
        self.article_links = []
        self.articles = {
            "title": "",
            "author": "",
            "date": "",
            "text": ""
        }
        self.driver = webdriver.Chrome()
        self.driver.get(self.base_url)

        #define the data we want and the structure to store it 

    def search_for_items(self):
        # Find all the links with the class name 'tec--card__title__link'
        link_elements = self.driver.find_elements(By.CLASS_NAME,'tec--card__title__link')

        # Iterate over the link elements and extract the href attribute
        for link_element in link_elements:
            href = link_element.get_attribute('href')
            self.article_links.append(href)

        return self.article_links

    def get_articles(self):
        links = self.search_for_items()
        for link in links:
            self.driver.get(link)
            #grab all text from current page
            ipdb.set_trace()
            self.articles["text"] = self.driver.find_element(By.CLASS_NAME, 'tec--article__body-grid').text
            self.articles["title"] = self.driver.find_element(By.CLASS_NAME, 'tec--article__header__title').text
            #self.articles["author"] = self.driver.find_element(By.CLASS_NAME, 'tec--link--tecmundo').text
            self.articles["date"] = self.driver.find_element(By.CLASS_NAME, 'tec--timestamp__item').text
    
        return self.articles

    def translateArticle(self, article):
        #import googletranslate API
        pass
        


def __main__():
    scraper = TecMundo()
    #ipdb.set_trace()
    scraper.get_articles() 
    print(scraper.article_links)

if __name__ == "__main__":
    __main__()