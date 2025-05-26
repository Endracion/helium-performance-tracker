from selenium import webdriver

# Initialize the Firefox driver
driver = webdriver.Firefox()

# Open a webpage
driver.get('http://example.com')

# Remember to close the driver once you're done
driver.quit()