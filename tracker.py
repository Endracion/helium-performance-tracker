from selenium import webdriver
from selenium.webdriver.common.by import By  # Import By from selenium's webdriver module
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random

# Initialize the Firefox driver
driver = webdriver.Firefox() # Adjust this if you're using a different browser

# In turn, open a webpage to the specified URL from the provided csv
# driver.get('https://heliumtracker.io/hotspots/618961')

# scrape Name
# change start and end date according to csv
# scrape perfromance data
# apply 0.2 and 0.3 to performance data
# write everthing to same csv file

df = pd.read_csv('tracker.csv')
for index, row in df.iterrows():
    url = row['Id']
    driver.get(f'https://heliumtracker.io/hotspots/{url}')
    time.sleep(10) # Adjust if necessary for page loading times
    # Your logic to fetch and process data
    # For example: data = some_function_to_fetch_data(driver)

    try:
        # Define an explicit wait
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds before throwing an exception
        # Use the correct XPath you've identified
        xpath = '/html/body/div[2]/section/div/div[2]/div/div[1]/div/div[1]/h1/span[1]'

        # Find the element using XPath
        span_element = driver.find_element(By.XPATH, xpath)

        # Extract the text from the element
        text = span_element.text

        # Print or process the extracted text
        print('Extracted text:', text)

    except Exception as e:
        print("Error extracting text:", e)

    # Add some functionality to interact with the webpage here
    # Insert actions you want to perform
    # For example: finding elements and interacting with them
    # element = driver.find_element_by_id('exampleId')
    # element.click()

    # Example of finding elements using different methods:
# element_by_id = driver.find_element_by_id('elementId')

# element_by_class = driver.find_element_by_class_name('className')

# element_by_name = driver.find_element_by_name('elementName')

# element_by_tag = driver.find_element_by_tag_name('div')

# element_by_xpath = driver.find_element_by_xpath('//div[@class="exampleClass"]')
# Note: XPaths can be very powerful, especially for more complex structures

# Retrieve the text from the element
# text = element_by_id.text  # Adjust this to match the element you located
# print('Extracted text:', text)


# $x("/html/body/div[2]/section/div/div[2]/div/div[1]/div/div[1]/h1/span[1]")
    # Step 2: Update the DataFrame with new data
    # df.loc[index, 'NewData'] = data  # Replace 'NewData' with the actual field name you're working with

    # Wait for a few seconds before proceeding to the next URL
    wait_time = random.randint(10, 20)
    time.sleep(wait_time) # Adjust the number of seconds depending on your needs

# Step 3: Write your updates back to the CSV
df.to_csv('tracker_results.csv', index=False)  # Save the updated data to a new CSV file

# Remember to close the driver once you're done
driver.quit()