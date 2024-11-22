from imports import *

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
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "modal__dismiss"))
        )
        close_button.click()
        
    except Exception as e:
        logging.error("Close button not found or not clickable:", e)