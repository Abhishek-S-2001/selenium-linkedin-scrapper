from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data_model import CompanyData
from dataclasses import asdict
import pandas as pd
import time
import logging
import threading
import queue


def get_chrome(company_url: str):
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
    chrome_options.add_argument("--incognito")  # Open in incognito mode
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,         # Disable images
        "profile.default_content_setting_values.media_stream": 2,     # Disable media streams
        "profile.default_content_setting_values.automatic_downloads": 2,  # Block automatic downloads
        "profile.default_content_setting_values.popups": 2            # Block pop-ups
    })

    # Initialize the WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(company_url)

    return driver

def close_popup(driver):
    """
    Attempt to close any modal popup that appears on the LinkedIn page.
    
    Args:
        driver (webdriver.Chrome): The active Chrome WebDriver instance.
        
    Raises:
        Exception: If the close button cannot be found or clicked.
        
    Note:
        This function waits up to 10 seconds for the popup to become clickable.
    """
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "modal__dismiss"))
        )
        close_button.click()
        
    except Exception as e:
        logging.error("Close button not found or not clickable:", e)

def scrap_company_details(driver, company_data):
    """
    Scrape detailed company information from a LinkedIn company page and populate the CompanyData object.
    
    Args:
        driver (webdriver.Chrome): The active Chrome WebDriver instance.
        company_data (CompanyData): Object to store the scraped company information.
        
    The function extracts the following information:
        - Company name
        - Industry
        - Location
        - Followers count
        - Company description
        - Total employees
        - Job opportunities link
        - Follow link
        - About us description
        - Website
        - Company size
        - Headquarters
        - Company type
        - Founded year
        - Specialties
        
    Raises:
        Exception: If there are errors extracting any of the data fields.
    """
    logging.info("Extracting foundational information.")
    try:
        logging.info("Top card view")
        top_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "top-card-layout__card"))
        )
        
        # Define a function to check if an element exists and get its text, otherwise return an empty string
        def get_text_or_default(container, by, value):
            try:
                return container.find_element(by, value).text
            except:
                return ""
        
        def get_attribute_or_default(container, by, value, attribute):
            try:
                return container.find_element(by, value).get_attribute(attribute)
            except:
                return ""

        # Extract company data with error handling
        company_name = get_text_or_default(top_container, By.CLASS_NAME, "top-card-layout__title")
        industry = get_text_or_default(top_container, By.CLASS_NAME, "top-card-layout__headline")
        location_followers = get_text_or_default(top_container, By.CLASS_NAME, "top-card-layout__first-subline")
        description = get_text_or_default(top_container, By.CLASS_NAME, "top-card-layout__second-subline")
        job_opportunities_link = get_attribute_or_default(top_container, By.CSS_SELECTOR, "a.top-card-layout__cta--primary", "href")
        follow_link = get_attribute_or_default(top_container, By.CSS_SELECTOR, "a.top-card-layout__cta--secondary", "href")
        total_employees_text = get_text_or_default(top_container, By.CSS_SELECTOR, "p.face-pile__text")
        
        # Extract and clean up location and followers if available
        if location_followers:
            location_followers = location_followers.split(" ")
            location = " ".join(location_followers[:-2])
            followers = " ".join(location_followers[-2:])
        else:
            location = ""
            followers = ""
        
        # Extract total employees if available
        if total_employees_text:
            total_employees = total_employees_text.split(' ')[-2].replace(',', '')
        else:
            total_employees = ""       
        # Store data in the data object
        company_data.name=company_name
        company_data.industry=industry
        company_data.location=location
        company_data.followers=followers
        company_data.description=description
        company_data.total_employees=total_employees
        company_data.job_opportunities_link=job_opportunities_link
        company_data.follow_link=follow_link

        logging.info("Core card view")

        core_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "core-section-container__content"))
            )
            
        # Helper function to safely get text or attribute
        def get_text_or_default(container, by, value):
            try:
                return container.find_element(by, value).text
            except:
                return ""
        
        def get_attribute_or_default(container, by, value, attribute):
            try:
                return container.find_element(by, value).get_attribute(attribute)
            except:
                return ""

        # Extract company details with error handling
        about_us = get_text_or_default(core_container, By.CSS_SELECTOR, "p[data-test-id='about-us__description']")
        website = get_attribute_or_default(core_container, By.CSS_SELECTOR, "div[data-test-id='about-us__website'] a", "href")
        industry = get_text_or_default(core_container, By.CSS_SELECTOR, "div[data-test-id='about-us__industry'] dd")
        company_size = get_text_or_default(core_container, By.CSS_SELECTOR, "div[data-test-id='about-us__size'] dd")
        headquarters = get_text_or_default(core_container, By.CSS_SELECTOR, "div[data-test-id='about-us__headquarters'] dd")
        company_type = get_text_or_default(core_container, By.CSS_SELECTOR, "div[data-test-id='about-us__organizationType'] dd")
        founded_year = get_text_or_default(core_container, By.CSS_SELECTOR, "div[data-test-id='about-us__foundedOn'] dd")
        specialties = get_text_or_default(core_container, By.CSS_SELECTOR, "div[data-test-id='about-us__specialties'] dd")

        
        # Store data in the data object
        company_data.about_us = about_us
        company_data.website = website
        company_data.industry = industry
        company_data.company_size = company_size
        company_data.headquarters = headquarters
        company_data.company_type = company_type
        company_data.founded_year = founded_year
        company_data.specialties = specialties
        

    except Exception as e:
        logging.error("Error extracting foundational data:", e)


def scrap_company_posts(driver):
    """
    Scrape company posts from the LinkedIn company page.
    
    Args:
        driver (webdriver.Chrome): The active Chrome WebDriver instance.
        
    Note:
        - The function scrolls through the page to load up to 50 posts.
        - Maximum scroll attempts is limited to 10 to prevent infinite loops.
        - There's a 5-second delay between scrolls to allow content to load.
    """
    # Function to extract all post elements
    posts = driver.find_elements(By.CSS_SELECTOR, "ul.updates__list > li")

    # check number of post
    post_count = len(posts) 
    
    # Maximum scroll attempts is limited to 10 to prevent infinite loops.
    scroll_count = 0
    max_scroll = 10

    # Loop to scroll until we have at least 50 posts or no loader
    while post_count < 50 and scroll_count < max_scroll:
        # Scroll to trigger loader
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        posts = driver.find_elements(By.CSS_SELECTOR, "ul.updates__list > li")
        # Update post count
        post_count = len(posts)
        scroll_count += 1

    # Logging final post count
    logging.info(f"Final number of posts loaded: {post_count}")

    # Initialize posts_data array
    posts_data = []
    for post in posts:
        try:
            # Extract post details
            post_link = post.find_element(By.CSS_SELECTOR, "a.main-feed-card__overlay-link").get_attribute("href")
            org_name = post.find_element(By.CSS_SELECTOR, "a.text-sm").text
            followers = post.find_element(By.CSS_SELECTOR, "p.text-color-text-low-emphasis").text
            post_time = post.find_element(By.CSS_SELECTOR, "time").text

            # Expand post text if "See more" is present
            try:
                see_more_button = post.find_element(By.XPATH, ".//button[contains(text(), 'See more')]")
                see_more_button.click()
                time.sleep(1)  # Wait for text to expand
            except:
                pass  # Ignore if "See more" is not present
            # Extract the main post content
            post_text = post.find_element(By.CSS_SELECTOR, "p.attributed-text-segment-list__content").text
            try:
                likes = post.find_element(By.CSS_SELECTOR, "span[data-test-id='social-actions__reaction-count']").text
            except:
                likes = "No likes info"
            try:
                comments = post.find_element(By.CSS_SELECTOR, "a[data-test-id='social-actions__comments']").text
            except:
                comments = "No comments info"

            # Store the post data in dictionary format in posts_data array
            posts_data.append({
                "Organization": org_name,
                "Followers": followers,
                "Post Time": post_time,
                "Post Text": post_text,
                "Post Likes": likes,
                "Post Comments": comments,
                "Link": post_link
            })
        except Exception as e:
            print("Error processing a post:", e)
    return posts_data


def scrape_thread(url, result_queue):
    """
    Function to be run in each thread for scraping data
    """
    try:
        driver = get_chrome(url)
        close_popup(driver)
        
        company_data = CompanyData()
        scrap_company_details(driver, company_data)
        posts = scrap_company_posts(driver)
        company_data.posts = posts
        
        result_queue.put(company_data)
        driver.quit()
    except Exception as e:
        logging.error(f"Error in thread: {e}")
        result_queue.put(None)

if __name__=="__main__":
    start_time = time.time()

    logging.info("Starting multi-threaded scraping with 10 threads")
    
    # Create a queue to store results
    result_queue = queue.Queue()
    
    # Create and start 10 threads
    threads = []
    urls = [
        "https://www.linkedin.com/company/hcltech?trk=companies_directory",
        # "https://www.linkedin.com/company/tata-consultancy-services?trk=companies_directory",
        # "https://www.linkedin.com/company/infosys?trk=companies_directory",
        # "https://www.linkedin.com/company/wipro?trk=companies_directory",
        # "https://www.linkedin.com/company/capgemini?trk=companies_directory",
        # "https://www.linkedin.com/company/genpact?trk=companies_directory",
        # "https://in.linkedin.com/company/credapp",
        # "https://in.linkedin.com/company/zeptonow",
        # "https://in.linkedin.com/company/datazipio",
        # "https://in.linkedin.com/company/zintlr"
        ]
    
    for i in range(len(urls)):
        thread = threading.Thread(target=scrape_thread, args=(urls[i], result_queue))
        threads.append(thread)
        thread.start()
        time.sleep(2)  # Small delay between starting threads
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Collect all results
    all_results = []
    while not result_queue.empty():
        result = result_queue.get()
        if result is not None:
            all_results.append(asdict(result))
    
    # Convert to DataFrame
    if all_results:
        company_df = pd.DataFrame(all_results)
        print(f"Successfully collected data from {len(all_results)} threads")
        company_df.to_csv("/Users/himanshushakya/Documents/MagiQ AI/Dev/Ingestion/datalake/bronze/company_data.csv")
    else:
        print("No successful results collected")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Code executed in {elapsed_time:.2f} seconds.")