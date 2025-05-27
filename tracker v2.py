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

# Global variables for start and end dates, input by the user
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

if not (validate_date(start_date) and validate_date(end_date)):
    print ("Start or end date is not in the format YYYY-MM-DD")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

def start_date_input(driver, date):
    # Wait for the start date input field to be available and locate it by 'id'
    start_date_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'start_date')))
    # Clear the field and enter the desired start date
    start_date_field.clear()
    start_date_field.send_keys(date)  # Push the start date into the input field

def end_date_input(driver, date):
    end_date_field = driver.find_element(By.ID, 'end_date') # Locate the end date input field by 'id'
    end_date_field.clear()
    end_date_field.send_keys(date) # Push the end date into the input field

def write_results_to_csv(df, start_date, end_date):
    # Write your updates back to the CSV
    filename = f"tracker_results_{start_date}_{end_date}.csv"
    df.to_csv(f'{filename}', index=False)
    print(f"Data successfully written to file: {filename}")

# Initialize the Firefox driver
driver = webdriver.Firefox() # Adjust this if you're using a different browser driver for Selenium
print("Selenium driver initialized.")

df = pd.read_csv('tracker_results.csv', dtype=str) # This loads the csv file into pandas DataFrame

for index, row in df.iterrows(): # Iterate through each row in the DataFrame
    Id = str(row['Id'])
    url = (f'https://heliumtracker.io/hotspots/{Id}') # Construct the URL using the Id
    driver.get(url) # This opens the URL in the browser through Selenium

    try:
        start_date_input(driver, start_date) # Call the function to input the start date
        end_date_input(driver, end_date) # Call the function to input the end date

        submit_button = driver.find_element(By.NAME, 'commit')  # 'commit' is the name attribute of the submit button
        submit_button.click()

        # Find the element using XPath
        span_element_name = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[2]/div/div[1]/div/div[1]/h1/span[1]') # XPath to the name element
        span_element_performance = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[2]/div/div[2]/div[3]/div/div/div/div[2]/div[1]') # XPath to the performance element
        
        # Extract the text from the elements
        id_name = span_element_name.text
        id_performance = span_element_performance.text
        id_performance = id_performance.replace(" HNT", "") # Remove " HNT" from the performance text to be able to convert it to a float
        id_performance = float(id_performance) # Convert the performance text to a float

        print('Extracted name:', id_name) # Print results to make sure we're getting the right data
        print('Extracted perf:', id_performance) # Print results to make sure we're getting the right data
        print('0.2 of perf:', id_performance*0.2) # Print 20% of the performance
        print('0.3 of perf:', id_performance*0.3) # Print 30% of the performance

    # Update DataFrame
        df.at[index, 'Name'] = id_name
        df.at[index, 'Start'] = start_date
        df.at[index, 'End'] = end_date
        df.at[index, 'Performance'] = id_performance # Convert performance to float for calculations
        df.at[index, '0.2'] = id_performance*0.2 # Calculate 20% of the performance
        df.at[index, '0.3'] = id_performance*0.3 # Calculate 30% of the performance

        # df.loc[df['Id'] == Id, 'Name'] = id_name # match the data to the right column for the dataframe
        # df.loc[df['Id'] == Id, 'Performance'] = id_performance # match the data to the right column for the dataframe

    except Exception as e: # Catch any exceptions that occur during the process
        print(f"Error processing ID {Id}:", e)

    # Wait for a few seconds before proceeding to the next URL
wait_time = random.randint(10, 20)
time.sleep(wait_time) # Adjust the number of seconds depending on your needs

write_results_to_csv(df, start_date, end_date)

# Remember to close the driver once you're done
driver.quit()