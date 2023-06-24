from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SocialMedia:
    def __init__(self):
        self.path = "C:\Program Files (x86)\chromedriver.exe"
        self.base_url = "https://app.brand24.com/panel/results/1072087150?p=1&or=2&cdt=days&dr=4&rt=1&va=1&d1=2023-05-22&d2=2023-06-21"
        self.name = "SocialMedia"
        self.tweets = []
        self.text = []
        self.driver = webdriver.Chrome(self.path)
        self.driver.get(self.base_url)

    def search_for_items(self):
        #login
        self.__login__()
        #wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="sc-ktLMLx gHpgkT"]')))
        link_elements = self.driver.find_elements(By.XPATH, '//div[@class="sc-ktLMLx gHpgkT"]')
        for link_element in link_elements:
            self.tweets.append(link_element)

        return self.tweets

    def get_tweets(self, save=False):
        tweets = self.search_for_items()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@class="sc-itMJkM ldmVch"]')))
        authors = self.driver.find_elements(By.XPATH, '//span[@class="sc-itMJkM ldmVch"]')
        texts = self.driver.find_elements(By.XPATH, '//a[@class="sc-edLOhm CNQVI"]')
        sentiments = self.driver.find_elements(By.XPATH, '/html/body/div[1]/div[3]/main/div/div[3]/div/div/div[2]/div[1]/div/div/div/header/div[3]/div/span')
        wait = WebDriverWait(self.driver, 10)

        for tweet in tweets:
            article = {
                "author": authors[tweets.index(tweet)].text,
                "text": texts[tweets.index(tweet)].text,
                "sentiment": sentiments[tweets.index(tweet)].text
            }
            self.text.append(article)

        if save:
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
            with open(os.path.join(data_dir, 'Twitter.json'), 'w') as f:
                json.dump(self.text, f)

        return self.text

    def __login__(self, login_email, password):
        # login to the website
        #wait for page to load
        self.driver.implicitly_wait(10)
        login_button = self.driver.find_element(By.XPATH, '//div[@class="signup-email"]')
        login_button.click()
        input = self.driver.find_element(By.ID, 'login')
        input.send_keys(login_email)
        password = self.driver.find_element(By.XPATH, '//div[@class="signup-password"]')
        password.click()
        input_password = self.driver.find_element(By.ID, 'password')
        input_password.send_keys(password)
        login = self.driver.find_element(By.XPATH, '//input[@class="button-signup login_button"]')
        login.click()

def main():
    scraper = SocialMedia()
    items = scraper.get_tweets(save=True)
    print(len(items))
    print(items)

if __name__ == "__main__":
    main()
