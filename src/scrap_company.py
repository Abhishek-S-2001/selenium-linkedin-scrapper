from imports import *

def scrap_company_data(driver, company_data):
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
