import pandas as pd
from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By


def handler(event=None, context=None):
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    service = webdriver.ChromeService("/opt/chromedriver")

    options.binary_location = '/opt/chrome/chrome'
    options.add_argument("--headless=new")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")

    # Initialize the WebDriver
    chrome = webdriver.Chrome(options=options, service=service)

    # Open the webpage
    chrome.get("https://example.com/")

    # Extract data using Selenium
    page_text = chrome.find_element(by=By.XPATH, value="//html").text

    # Example: Process data into a Pandas DataFrame
    # Using page_text to populate one of the columns
    sample_data = {
        "Column1": ["Row1_Data1", "Row2_Data1", "Row3_Data1"],
        "PageText": [page_text] * 3  # Adding the same page_text to all rows
    }

    # Create a Pandas DataFrame
    df = pd.DataFrame(sample_data)

    # Print the DataFrame to debug (or save to file/database)
    print(df)

    # Quit the WebDriver
    chrome.quit()

    return df.to_dict()  # Example return: Convert DataFrame to dictionary for Lambda response
