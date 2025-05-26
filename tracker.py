from selenium import webdriver

# Initialize the Firefox driver
driver = webdriver.Firefox()

# Open a webpage
driver.get('https://heliumtracker.io/hotspots/618961')

# Remember to close the driver once you're done
driver.quit()