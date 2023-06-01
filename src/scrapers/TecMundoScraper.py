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

    def get_text(self):
        pass
        #grab all text from current page


    def translateArticle(self, article):
        #import googletranslate API
        pass


def __main__():
    scraper = TecMundo()
    #ipdb.set_trace()
    scraper.search_for_items() 
    print(scraper.article_links)

if __name__ == "__main__":
    __main__()