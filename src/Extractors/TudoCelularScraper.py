from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class TudoCelular:
    def __init__(self):
        self.path = "C:\Program Files (x86)\chromedriver.exe"
        self.base_url = "https://www.tudocelular.com/"
        self.name = "TudoCelular"
        self.article_links = []
        self.articles = []
        self.driver = webdriver.Chrome(self.path)
        self.driver.get(self.base_url)

        # define the data we want and the structure to store it

    def search_for_items(self, keyword=None):
        if keyword:
            self.target_search(keyword)
        link_elements = self.driver.find_elements(By.CLASS_NAME, 'title_new')
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
                "title": self.driver.find_element(By.XPATH, '//*[@id="hero"]/h2').text,
                "author": self.driver.find_element(By.CLASS_NAME, 's_author').text,
                "date": self.driver.find_element(By.XPATH, '//*[@id="hero"]/p').text,
                "text": self.driver.find_element(By.CLASS_NAME, 'textblock').text
            }
            self.articles.append(article)

        return self.articles

    def target_search(self, keyword):
        # search for articles based on keywords
        search_bar = self.driver.find_element(By.XPATH, '//*[@id="topsearch-text"]')
        search_bar.click()
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)