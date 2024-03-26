from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def scrape_movie_reviews(movie_name):
    """
        Scrapes Google reviews for a given movie and saves them to a text file.

        Parameters:
        movie_name (str): The name of the movie to search for.
        """
    # Replace the path with the path to your ChromeDriver
    CHROME_DRIVER_PATH = "C:/Users/Lenovo/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

    # Set up the service object pointing to the ChromeDriver
    service = Service(executable_path=CHROME_DRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Set the headless option

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=service, options=options)

    # Open Google
    driver.get("https://www.google.com")

    # Find the search box
    search_box = driver.find_element(By.NAME, "q")

    # Type in the search term and press Enter
    search_box.send_keys(f"{movie_name} movie google review")
    search_box.send_keys(Keys.RETURN)

    # Wait for page to load results
    time.sleep(3)

    try:
        # Click on the first search result
        all_reviews_link = driver.find_elements(By.XPATH, '//span[contains(text(),"More audience reviews")]')[0]
        all_reviews_link.click()

        movie_reviews = []

        time.sleep(7)

        total_records = driver.find_elements(By.XPATH, '//div[@jsname="HeNW9"]//*[@class="T7nuU" and @jsname="QUIPvd"]')

        for elements in total_records:
            driver.execute_script("arguments[0].style.display = 'block';", elements)
            movie_review = elements.text
            movie_reviews.append(movie_review)
            movie_reviews.append('--------------------')
            time.sleep(1)

        all_text = '\n'.join(movie_reviews)

        # Wait for the page to load
        time.sleep(2)

        # Write the data to a text file
        with open("movie_review.txt", "w", encoding="utf-8") as file:
            file.write(all_text)
    finally:
        driver.quit()