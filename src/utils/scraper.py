import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver



class SoapTwoDayScraper:
    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self._add_webdriver_arguments()
        self.driver = webdriver.Firefox(options=self.options)
        self.wait = WebDriverWait(driver=self.driver, timeout=10)
        self.base_url = "https://ww3.soap2dayhdz.com"


    def _add_webdriver_arguments(self):
        """An helper to add arguments to the webdriver options."""
        self.options.add_argument("--incognito")
        # self.options.add_argument("--no-sandbox")
        # self.options.add_argument("--disable-dev-shm-usage")
        # self.options.add_argument("--headless=new")

    def _scrape_result_data(self, user_query:str):
        """Scrapes the results of the searched query"""
        
        results = []
        
        try:
            
            self.driver.get(f"{self.base_url}/search/?q={user_query}")
                
            container = self.wait.until(EC.presence_of_element_located((By.ID, "resdata")))
            
            result_columns = container.find_elements(By.CLASS_NAME, "col")
            
            if not result_columns:
                raise Exception(f"No Result found for ({user_query.replace("+"," ")}) !")
            
            for result in result_columns:
                title = result.find_element(By.TAG_NAME, "h3").text
                img_link = result.find_element(By.TAG_NAME, "img").get_attribute("src")
                movie_href = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                results.append({"title":title, "img":img_link, "movie_href":movie_href})
            
            return results
        
        except Exception as err:
            print(f"Error: _scrape_result_data -> {err} (soap2day)")
            
    
    def print_result(self, results) -> int:

        count: int = 0

        for idx, result in enumerate(results):
            print(f"{idx}: {result['title']}")
            count += 1

        user_choice = int(input("Enter the num of the movie: "))

        while user_choice <= 0 or user_choice >= count:
            user_choice = int(input("Invalid choice. Enter again: "))
            
        # movie_details = {
        #     "title":results[user_choice]["title"],
        #     "img_link":results[user_choice]["img_link"],
        #     "movie_href":results[user_choice]["movie_href"],
        #     }
        return results[user_choice]
            
        
    def start(self):
        results = self._scrape_result_data(user_query='superman')
        choice = self.print_result(results=results)
        print(choice)
        self.driver.quit()


scraper = SoapTwoDayScraper()

scraper.start()

