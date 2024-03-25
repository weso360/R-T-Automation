from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

# Initialize the WebDriver
driver = webdriver.Chrome()

# Define the base URL
base_url = "https://www.dailyinfo.co.uk/food-and-drink?page={}"

# Start from the first page
page_number = 1

# Loop until the final page is reached
while True:
    # Navigate to the current page
    driver.get(base_url.format(page_number))

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-interface-result")))

    # Find all the search results
    search_results = driver.find_elements(By.CSS_SELECTOR, ".search-interface-result")

    # Iterate over each search result
    for result in search_results:
        # Find the title link within the search result
        title_link = result.find_element(By.CSS_SELECTOR, "div.title a")

        # Scroll the element into view
        driver.execute_script("arguments[0].scrollIntoView(true);", title_link)

        # Click on the title link
        try:
            title_link.click()
        except ElementClickInterceptedException:
            # Handle click interception (e.g., cookie consent banner)
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "cc-window")))
            
            # Try clicking again after the banner disappears
            title_link.click()

        try:
            # Wait for the website link to be present
            website_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.button[href^='http']")))

            # Extract the website link from the href attribute
            website_link = website_element.get_attribute("href")

            # Remove the "http://" or "https://" prefix
            website_link = website_link.replace("http://", "").replace("https://", "")

            # Split the website link by the "/" character and take the first part (domain name)
            website_link = website_link.split("/")[0]
        except TimeoutException:
            website_link = "none"


        # Output the collected information
        print("Website:", website_link)

        # Go back to the previous page
        driver.back()

    # Increment the page number
    page_number += 1

    # Check if there is a next page
    try:
        next_page_link = driver.find_element(By.CSS_SELECTOR, "a[rel='next']")
        next_page_link.click()
    except:
        # No next page, break out of the loop
        break

# Close the browser window
driver.quit()
