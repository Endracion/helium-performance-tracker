from selenium import webdriver
from selenium.webdriver.common.by import By  # Import By from selenium's webdriver module
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import time
import random

# Ppen a webpage to the specified URL from the provided csv and for each
# apply start and end date according to csv on the page and submit with the button
# scrape name and perfromance data
# write name and performance data to csv file that's generated with a timestamp
# apply 0.2 and 0.3 to performance data and save it as well
# print name of csv file

def start_date_input(driver, date):
    # Wait for the start date input field to be available and locate it by 'id'
    start_date_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, start_date)))
    # Clear the field and enter the desired start date
    start_date_field.clear()
    start_date_field.send_keys(start_date)  # Push the start date into the input field

def end_date_input(driver, date):
    end_date_field = driver.find_element(By.ID, end_date) # Locate the end date input field by 'id'
    end_date_field.clear()
    end_date_field.send_keys(end_date) # Push the end date into the input field

def write_results_to_csv(df):
    # Write your updates back to the CSV
    filename = f"tracker_results_{start_date}_{end_date}.csv"
    df.to_csv(f'{filename}', index=False)

# Initialize the Firefox driver
driver = webdriver.Firefox() # Adjust this if you're using a different browser driver for Selenium

df = pd.read_csv('tracker_results.csv', dtype=str) # This loads the csv file into pandas DataFrame

for index, row in df.iterrows():
    Id = str(row['Id'])
    url = (f'https://heliumtracker.io/hotspots/{Id}') # Construct the URL using the Id
    driver.get(url) # This opens the URL in the browser through Selenium

    try:
        # Wait for the start date input field to be available and locate it by 'id'
        start_date_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'start_date')))

        # Clear the field and enter the desired start date
        start_date = '2025-04-27'  # Adjust this date as needed, will be loaded from the csv in the future
        start_date_field.clear()
        start_date_field.send_keys(start_date)  # Push the start date into the input field

        end_date = '2025-05-20'  # Adjust this date as needed, will be loaded from the csv in the future
        end_date_field = driver.find_element(By.ID, 'end_date') # Locate the end date input field by 'id'
        end_date_field.clear()
        end_date_field.send_keys(end_date) # Push the end date into the input field

        submit_button = driver.find_element(By.NAME, 'commit')  # 'commit' is the name attribute of the submit button
        submit_button.click()

        # Find the element using XPath
        span_element_name = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[2]/div/div[1]/div/div[1]/h1/span[1]') # XPath to the name element
        span_element_performance = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[2]/div/div[2]/div[3]/div/div/div/div[2]/div[1]') # XPath to the performance element
        
        # Extract the text from the elements
        id_name = span_element_name.text
        id_performance = span_element_performance.text
        id_performance = id_performance.replace(" HNT", "") # Remove " HNT" from the performance text to be able to convert it to a float

        print('Extracted name:', id_name) # Print results to make sure we're getting the right data
        print('Extracted perf:', id_performance) # Print results to make sure we're getting the right data

    # Update DataFrame
        df.at[index, 'Name'] = id_name
        df.at[index, 'Performance'] = float(id_performance)

        # df.loc[df['Id'] == Id, 'Name'] = id_name # match the data to the right column for the dataframe
        # df.loc[df['Id'] == Id, 'Performance'] = id_performance # match the data to the right column for the dataframe

    except Exception as e: # Catch any exceptions that occur during the process
        print(f"Error processing ID {Id}:", e)

    # Wait for a few seconds before proceeding to the next URL
wait_time = random.randint(10, 20)
time.sleep(wait_time) # Adjust the number of seconds depending on your needs

# Write your updates back to the CSV
filename = f"tracker_results_{start_date}_{end_date}.csv"
df.to_csv(f'{filename}', index=False)

print(f"Data successfully written to file: {filename}")


# Remember to close the driver once you're done
driver.quit()