import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Specify the URL of the business page on Google Maps
url = "https://www.google.com/maps/place/McDonald's+-+Buah+Batu/@-6.9389008,107.6226618,17z/data=!4m8!3m7!1s0x2e68e867e4833eed:0x312047115647ad11!8m2!3d-6.9389061!4d107.6252367!9m1!1b1!16s%2Fg%2F12ml2ldyr?entry=ttu"

# Create an instance of the Chrome driver
driver = webdriver.Chrome("E:/Fadhel/DOKUMEN/BRAINCORE/DATA/scraping-reviews-from-googlemaps/Driver/chromedriver.exe")

# Navigate to the specified URL
driver.get(url)

# Wait for the reviews to load
wait = WebDriverWait(driver, 30)  # Increased the waiting time

# Scroll down to load more reviews
body = driver.find_element(By.XPATH, "//div[contains(@class, 'm6QErb') and contains(@class, 'DxyBCb') and contains(@class, 'kA9KIf') and contains(@class, 'dS8AEf')]")
num_reviews = len(driver.find_elements(By.CLASS_NAME, 'wiI7pd'))
while True:
    body.send_keys(Keys.END)
    time.sleep(30)  # Adjust the delay based on your internet speed and page loading time
    new_num_reviews = len(driver.find_elements(By.CLASS_NAME, 'wiI7pd'))
    if new_num_reviews == num_reviews:
        # Scroll to the top to ensure all reviews are loaded
        body.send_keys(Keys.HOME)
        time.sleep(10)
        break
    num_reviews = new_num_reviews

# Wait for the reviews to load completely
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'wiI7pd')))

# Extract the text of each review
review_elements = driver.find_elements(By.CLASS_NAME, 'wiI7pd')
reviews = [element.text for element in review_elements]

# Save reviews to CSV
with open('gmaps_reviews.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Review'])
    for review in reviews:
        writer.writerow([review])

# Close the browser
driver.quit()
