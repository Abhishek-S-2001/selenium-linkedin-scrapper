from imports import *

def get_chrome_driver(company_url: str):
    """
    Initialize and return a Chrome WebDriver instance configured for LinkedIn scraping.
    
    Args:
        company_url (str): The LinkedIn company page URL to navigate to.
        
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance in incognito mode.
        
    Example:
        driver = get_chrome("https://www.linkedin.com/company/example")
    """
    # Set Chrome options
    chrome_options = Options()

    service = webdriver.ChromeService("/opt/chromedriver")
    chrome_options.binary_location = '/opt/chrome/chrome'

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x1696")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_options.add_argument(f"--data-path={mkdtemp()}")
    chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-port=9222")

    chrome_options.add_argument("--incognito")  # Open in incognito mode
    chrome_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,         # Disable images
        "profile.default_content_setting_values.media_stream": 2,     # Disable media streams
        "profile.default_content_setting_values.automatic_downloads": 2,  # Block automatic downloads
        "profile.default_content_setting_values.popups": 2            # Block pop-ups
    })


    # Initialize the WebDriver with options
    driver = webdriver.Chrome(options=chrome_options, service=service)
    driver.get(company_url)

    return driver