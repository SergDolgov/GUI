
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class SeleniumApi:
     
    def __init__(self, main_window):
        self.main_window = main_window
        self.driver = webdriver.Chrome()
    
    def find(self, url):
        self.driver.get(url)
        # for selection input with name attribute "name"
        elem = self.driver.find_element(By.ID, "id-search-field")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        self.main_window.logger.info("ok")