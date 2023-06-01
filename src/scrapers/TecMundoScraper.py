#create a scraper for TecMundo tech articles
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class TecMundo:
    def __init__(self):
        self.base_url = "https://www.tecmundo.com.br/novidades"
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
        link = self.driver.find_element("xpath",'//*[@id="js-main"]/div/div[1]/div[1]/div[3]/div[2]/article/div/h3/a')
        self.article_links.append(link.get_attribute("href"))
        return self.article_links

    def get_text(self):
        pass
        #grab all text from current page


    def translateArticle(self, article):
        #import googletranslate API
        pass


def __main__():
    scraper = TecMundo()
    scraper.search_for_items() 
    print(scraper.article_links)

if __name__ == "__main__":
    __main__()