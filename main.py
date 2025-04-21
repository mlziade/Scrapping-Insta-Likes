from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv
from datetime import datetime
import time
import os

def parse_meta_description(description):
    """Parse the meta description to extract data from Instagram posts."""
    print(f"Raw description: {description}")
    
    # Extract likes
    likes_match1 = re.search(r'([\d,.]+[KM]?)\s+likes', description)
    likes_match2 = re.search(r'"like_count":\s*([\d,.]+),', description)
    likes_str = likes_match1.group(1) if likes_match1 else (likes_match2.group(1) if likes_match2 else "0")
    
    # Extract comments
    comments_match = re.search(r'([\d,.]+[KM]?)\s+comments', description)
    comments_str = comments_match.group(1) if comments_match else "0"
    
    # Extract username
    username_match = re.search(r'-\s+([^\s]+)\s+em', description)
    username = username_match.group(1) if username_match else ""
    
    # Extract post date
    date_match = re.search(r'em\s+([^:]+):', description)
    post_date = date_match.group(1).strip() if date_match else ""
    
    # Extract caption
    caption_match = re.search(r':\s+"([^"]+)"', description)
    caption = caption_match.group(1) if caption_match else ""
    if caption:
        caption = caption.replace('\n', '. ')
    
    return {
        'name': username,
        'likes': convert_count(likes_str),
        'comments': convert_count(comments_str),
        'caption': caption,
        'post_date': post_date,
        'scrape_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def convert_count(count_str):
    """Convert counts like '744K' to their actual values."""
    if 'K' in count_str:
        return str(int(float(count_str.replace('K', '')) * 1000))
    elif 'M' in count_str:
        return str(int(float(count_str.replace('M', '')) * 1000000))
    else:
        return count_str.replace(',', '')

def connect_to_existing_chrome():
    """Connect to an already running Chrome instance."""
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    try:
        driver = webdriver.Chrome(options=options)
        print("Successfully connected to existing Chrome instance.")
        return driver
    except Exception as e:
        print(f"Error connecting to Chrome: {str(e)}")
        print("\nTo use this script, first start Chrome with remote debugging enabled:")
        print('1. Close all Chrome instances')
        print('2. Open command prompt and run:')
        print('"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222')
        print('3. Log in to Instagram in that browser')
        print('4. Run this script again')
        return None

def scrape_instagram_posts(post_urls):
    """Scrape data from a list of Instagram post URLs."""
    driver = connect_to_existing_chrome()
    if not driver:
        return []
    
    results = []
    
    for i, url in enumerate(post_urls):
        print(f"\nProcessing post {i+1}/{len(post_urls)}: {url}")
        try:
            driver.get(url)
            
            # Wait for the meta description to be available
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//meta[@name='description']"))
            )
            
            # Extract the meta description
            meta_description = driver.find_element(By.XPATH, "//meta[@name='description']").get_attribute('content')
            
            # Parse the description
            post_data = parse_meta_description(meta_description)
            post_data['post_url'] = url  # Add the post URL to the data
            results.append(post_data)
            
            print("✓ Successfully scraped post data:")
            for key, value in post_data.items():
                print(f"  {key}: {value}")
            
            # Add delay to avoid rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"✗ Error scraping {url}: {str(e)}")
    
    # Don't close the browser since it's an existing session
    return results

def save_to_csv(data, filename='instagram_posts.csv'):
    """Save scraped data to a CSV file."""
    if not data:
        print("No data to save.")
        return False
    
    filepath = os.path.join(os.getcwd(), filename)
    fieldnames = ['name', 'likes', 'comments', 'caption', 'post_date', 'scrape_date', 'post_url']  # Add 'post_url' to fieldnames
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\nData saved to {filepath}")
    return True

def main():
    # Read Instagram post URLs from input_file.txt
    try:
        with open('input_file.txt', 'r') as file:
            post_urls = [line.strip() for line in file]
            print(f"Found {len(post_urls)} URLs in input_file.txt")
    except FileNotFoundError:
        print("Error: input_file.txt not found. Please create this file and add Instagram post URLs, one URL per line.")
        return
    
    print("Instagram Post Scraper")
    print("======================")
    
    # Scrape the posts
    results = scrape_instagram_posts(post_urls)
    
    # Save the results to CSV
    if results:
        save_to_csv(results)

if __name__ == "__main__":
    main()