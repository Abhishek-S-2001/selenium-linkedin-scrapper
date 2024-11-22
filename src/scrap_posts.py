from imports import *


def scrap_company_posts(driver, number_of_posts):
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
    while post_count < number_of_posts and scroll_count < max_scroll:
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