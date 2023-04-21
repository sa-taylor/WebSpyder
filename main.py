import concurrent.futures
from sitemap_parse import get_sitemap, save_links_to_file, filter_parent_links
from scrape import read_links_from_file, scrape_website, remove_link_from_file
from combine_data import combine_csv_files
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import os

def process_link(base_url):
    # Create a new Chrome web driver instance
    driver = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')

    # Scrape the website for data
    scrape_website(driver, base_url)

    # Remove the processed URL from the sitemap file
    remove_link_from_file(sitemap_file, base_url)

    # Close the web driver instance
    driver.quit()

def cleanup_links_file(filename):
    # Open the file and read all lines
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Clean up lines that do not start with 'http://' or 'https://'
    cleaned_lines = [line for line in lines if re.match(r'^https?:\/\/', line.strip())]

    # Overwrite the file with the cleaned lines
    with open(filename, 'w') as file:
        file.writelines(cleaned_lines)

def run_scrape(links):
    # Set the maximum number of threads
    max_threads = 4

    # Use ThreadPoolExecutor for multithreading
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(process_link, links)

if __name__ == '__main__':
    # Update the sitemap file
    sitemap_url = 'https://www.levelninesports.com/sitemap/categories/'
    sitemap_links = get_sitemap(sitemap_url)

    if sitemap_links:
        # Filter the parent links and save them to a new file
        filtered_links = filter_parent_links(sitemap_links)
        save_links_to_file(filtered_links, 'filtered_sitemap_links.txt')

    # Extract all of the data from the website
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    # Disable image loading
    prefs = {'profile.managed_default_content_settings.images': 2}
    chrome_options.add_experimental_option('prefs', prefs)
    
    # Disable Javascript
    chrome_options.add_argument('--disable-javascript')

    # Assign Txt file with sitemap data
    sitemap_file = 'filtered_sitemap_links.txt'
    links = read_links_from_file(sitemap_file)

    # First run of the scrape
    run_scrape(links)

    # Clean up the filtered_sitemap_links.txt file
    cleanup_links_file(sitemap_file)

    # Read the cleaned links from the file
    cleaned_links = read_links_from_file(sitemap_file)

    # Second run of the scrape
    run_scrape(cleaned_links)

    # Combine all CSV files into a single file
    input_folder = 'scraped_data'
    output_file = 'all_extracted_data.csv'
    combine_csv_files(input_folder, output_file)
    
   #If the sitemap file is empty (meaning all URLs have been scraped), then the file will be repopulated for the purpose of storing that data for reference
    if os.stat(sitemap_file).st_size == 0:
        sitemap_links = get_sitemap(sitemap_url)

        if sitemap_links:
            # Filter the parent links and save them to a new file
            filtered_links = filter_parent_links(sitemap_links)
            save_links_to_file(filtered_links, 'filtered_sitemap_links.txt')