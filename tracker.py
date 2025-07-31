from selenium import webdriver
from selenium.webdriver.common.by import By  # Import By from selenium's webdriver module
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import calendar
from datetime import datetime
import pandas as pd
import time
import random
import os
from dotenv import load_dotenv

# Open a webpage to the specified URL from the provided csv and for each
# apply start and end date according user input and submit with the button
# scrape name and perfromance data
# write name and performance data to csv file that's generated with a timestamp
# apply 0.2 and 0.3 to performance data and save it as well
# print name of saved csv file

# Global variables for start and end dates, input by the user
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")

# Credentials (use environment variables)
load_dotenv()  # Load .env file

email = os.getenv("HT_EMAIL")
password = os.getenv("HT_PASSWORD")

if not email or not password:
    print("Email or password not found in environment variables.")
    exit(1)

def login(driver, email, password):
    login_url = "https://heliumtracker.io/users/sign_in"
    driver.get(login_url)

    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user_email"))
        )
        password_input = driver.find_element(By.ID, "user_password")
        login_button = driver.find_element(By.XPATH, "//button[text()='Login']")

        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)
        login_button.click()

        # Wait until login completes, maybe by checking a dashboard element
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/users/sign_out']"))
        )
        print("Login successful.")
    except TimeoutException:
        print("Login failed or took too long.")
        driver.quit()
        exit(1)

def validate_date(date_str):
    try:
        date_object = datetime.strptime(date_str, "%Y-%m-%d") # Parse the date string into a datetime object
        today = datetime.now().date() # Get the current date without time for comparison
        
        if date_object.date() > today: # Check if the provided date is in the future
            print(f"Error: {date_str} is a future date. Please enter a valid past or current date.")
            return False
        
        return True
        
    except ValueError:
        return False

if not (validate_date(start_date) and validate_date(end_date)):
    print ("Start or end date is not valid.")
    start_date = input("Re-enter start date (YYYY-MM-DD): ")
    end_date = input("Re-enter end date (YYYY-MM-DD): ")

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
print("Selenium driver initialized, please wait...")
driver = webdriver.Firefox() # Adjust this if you're using a different browser driver for Selenium

login(driver, email, password)

# Load input data
df = pd.read_csv('tracker_input.csv', dtype=str) # This loads the csv file into pandas DataFrame

for index, row in df.iterrows(): # Iterate through each row in the DataFrame
    Id = str(row['Id'])
    url = (f'https://heliumtracker.io/hotspots/{Id}') # Construct the URL using the Id
    driver.get(url) # This opens the URL in the browser through Selenium

    try:
        start_date_input(driver, start_date) # Call the function to input the start date
        end_date_input(driver, end_date) # Call the function to input the end date

        submit_button = driver.find_element(By.NAME, 'commit')  # 'commit' is the name attribute of the submit button
        submit_button.click()
        
        # Extract name and performance data
        try:
            # Find the element using XPath and extract the text from the elements
            span_element_name = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[2]/div/div[1]/div/div[1]/h1/span[1]') # XPath to the name element
            id_name = span_element_name.text
            
            span_element_performance = driver.find_element(By.XPATH, '/html/body/div[2]/section/div/div[2]/div/div[2]/div[3]/div/div/div/div[2]/div[1]') # XPath to the performance element
        
            id_performance = span_element_performance.text
            id_performance = id_performance.replace(" HNT", "") # Remove " HNT" from the performance text to be able to convert it to a float
            id_performance = float(id_performance) # Convert the performance text to a float

        except (NoSuchElementException, TimeoutException, ValueError):
            id_performance = 0.0
            print(f"Error retrieving data for ID {Id}. Setting performance to 0.")

        id_20_perf = round(id_performance*0.2,5) # Calculate 20% of the performance
        id_30_perf = round(id_performance*0.3,5) # Calculate 30% of the performance

        print('Extracted name:', id_name) # Print results to make sure we're getting the right data
        print('Extracted perf:', id_performance) # Print results to make sure we're getting the right data
        print('0.2 of perf:', id_20_perf) # Print 20% of the performance
        print('0.3 of perf:', id_30_perf) # Print 30% of the performance

        # Update DataFrame
        df.at[index, 'Name'] = id_name
        df.at[index, 'Start'] = start_date
        df.at[index, 'End'] = end_date
        df.at[index, 'Performance'] = id_performance # Convert performance to float for calculations
        df.at[index, '0.2'] = id_20_perf # Calculate 20% of the performance
        df.at[index, '0.3'] = id_30_perf # Calculate 30% of the performance

        write_results_to_csv(df, start_date, end_date)

        # Wait for a few seconds before proceeding to the next URL
        wait_time = random.randint(10, 20)
        print(f"Waiting for {wait_time} seconds before processing the next ID...")
        time.sleep(wait_time) # Adjust the number of seconds depending on your needs
        
    except Exception as e: # Catch any exceptions that occur during the process
        print(f"General error processing ID {Id}:", e)

print("All IDs processed successfully; closing the driver.")
# Remember to close the driver once you're done
driver.quit()