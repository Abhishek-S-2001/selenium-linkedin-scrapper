import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from imports import *

from src.data_model import CompanyData
from src.get_driver import get_chrome_driver
from src.popup import close_popup
from src.scrap_company import scrap_company_data
from src.scrap_posts import scrap_company_posts


def scrape_thread(url, result_queue, number_of_posts):
    """
    Function to be run in each thread for scraping data
    """
    try:
        driver = get_chrome_driver(url)
        close_popup(driver)
        
        company_data = CompanyData()
        scrap_company_data(driver, company_data)
        posts = scrap_company_posts(driver, number_of_posts)
        company_data.posts = posts
        
        result_queue.put(company_data)
        driver.quit()
    except Exception as e:
        logging.error(f"Error in thread: {e}")
        result_queue.put(None)


def handler(event=None, context=None):

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
    number_of_posts = 50

    start_time = time.time()
    logging.info("Starting multi-threaded scraping with urls")
    
    # Create a queue to store results
    result_queue = queue.Queue()
    # Create and start 10 threads
    threads = []
    
    for i in range(len(urls)):
        thread = threading.Thread(target=scrape_thread, args=(urls[i], result_queue, number_of_posts))
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
    else:
        print("No successful results collected")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Code executed in {elapsed_time:.2f} seconds.")

    # Convert DataFrame to a dictionary
    response = company_df.to_dict(orient='records')
    
    return {
        "statusCode": 200,
        "body": response
    }