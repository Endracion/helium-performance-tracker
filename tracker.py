from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import pandas as pd
import time
import random
import os
import calendar
import re
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()
email = os.getenv("HT_EMAIL")
password = os.getenv("HT_PASSWORD")

if not email or not password:
    print("Email or password not found in environment variables.")
    exit(1)

# Ask user for a past month (not current or future)
def get_valid_month():
    today = datetime.today()
    current_year = today.year
    latest_valid_month = today.month - 1

    if latest_valid_month == 0:
        latest_valid_month = 12
        current_year -= 1

    while True:
        try:
            month_num = int(input(f"Enter the month number (1-12) to retrieve data for (must be <= {latest_valid_month}): "))
            if 1 <= month_num <= latest_valid_month:
                return current_year, month_num
            else:
                print("Invalid month. Please choose a past month (not current or future).")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 12.")

# Calculate date range
year, month = get_valid_month()
start_date = f"{year}-{month:02d}-01"
_, last_day = calendar.monthrange(year, month)
end_date = f"{year}-{month:02d}-{last_day:02d}"

# Login function with timeout protection
def login(driver, email, password):
    login_url = "https://heliumtracker.io/users/sign_in"
    driver.set_page_load_timeout(15)

    try:
        driver.get(login_url)
    except TimeoutException:
        print("Login page took too long to load. Website may be down.")
        driver.quit()
        exit(1)

    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user_email"))
        )
    except TimeoutException:
        print("Login form did not appear. Page may not have loaded correctly.")
        driver.quit()
        exit(1)

    try:
        password_input = driver.find_element(By.ID, "user_password")
        login_button = driver.find_element(By.XPATH, "//button[text()='Login']")

        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)
        login_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/users/sign_out']"))
        )
        print("Login successful.")
    except TimeoutException:
        print("Login failed — check credentials or site issue.")
        driver.quit()
        exit(1)

# Setup Selenium (optional: run headless if desired)
print("Initializing Selenium driver...")
options = Options()
# options.headless = True  # Uncomment to run without opening browser window
driver = webdriver.Firefox(options=options)

# Perform login
login(driver, email, password)

# Load input CSV
df = pd.read_csv('tracker_input.csv', dtype=str)

# Iterate through each ID
for index, row in df.iterrows():
    Id = str(row['Id'])
    url = f'https://heliumtracker.io/hotspots/{Id}'
    driver.get(url)

    try:
        # Wait and fill in start and end dates
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'start_date')))
        driver.find_element(By.ID, 'start_date').clear()
        driver.find_element(By.ID, 'start_date').send_keys(start_date)

        driver.find_element(By.ID, 'end_date').clear()
        driver.find_element(By.ID, 'end_date').send_keys(end_date)

        driver.find_element(By.NAME, 'commit').click()

        # Give page time to respond
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1/span[1]"))
        )

        id_name = "Unknown"
        id_performance = 0.0

        try:
            id_name = driver.find_element(By.XPATH, "//h1/span[1]").text.strip()

            # Wait until the correct HNT value appears — not just the container
            def valid_performance_loaded(driver):
                try:
                    el = driver.find_element(By.XPATH, "//sup[contains(text(), 'HNT')]/parent::div")
                    text = el.text.strip()
                    match = re.search(r'[\d.]+', text)
                    time.sleep(1)
                    if match:
                        val = float(match.group(0))
                        return val > 0.1
                    return False
                except:
                    return False

            WebDriverWait(driver, 5).until(valid_performance_loaded)

            # Now extract the correct value
            hnt_container = driver.find_element(By.XPATH, "//sup[contains(text(), 'HNT')]/parent::div")
            perf_text = hnt_container.text.strip()

            match = re.search(r'[\d.]+', perf_text)
            if match:
                id_performance = float(match.group(0))

        except Exception as e:
            print(f"Error retrieving data for ID {Id}: {e}")
            print(f"Setting name to '{id_name}' and performance to 0.")

        # Continue
        id_20_perf = round(id_performance * 0.2, 5)
        id_30_perf = round(id_performance * 0.3, 5)

        print(f"ID {Id} | Name: {id_name} | Perf: {id_performance} | 0.2: {id_20_perf} | 0.3: {id_30_perf}")

        # Store results in DataFrame
        df.at[index, 'Name'] = id_name
        df.at[index, 'Start'] = start_date
        df.at[index, 'End'] = end_date
        df.at[index, 'Performance'] = id_performance
        df.at[index, '0.2'] = id_20_perf
        df.at[index, '0.3'] = id_30_perf

        # Random wait
        wait_time = random.randint(10, 20)
        print(f"Waiting {wait_time}s before next ID...")
        time.sleep(wait_time)

    except Exception as e:
        print(f"General error processing ID {Id}:", e)

# Save final CSV
# Format for filename: tracker_results_2025-06-01_to_2025-06-30.csv
filename = f"tracker_results_{start_date}_to_{end_date}.csv".replace("-", "_")
df.to_csv(filename, index=False)
print(f"\nAll done! Data saved to: {filename}")

# Close browser
driver.quit()
