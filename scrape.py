import csv
import os
import math
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def read_links_from_file(filename):
    with open(filename, 'r') as file:
        links = [line.strip() for line in file.readlines()]
    return links

def remove_link_from_file(filename, link):
    with open(filename, 'r') as file:
        links = [line.strip() for line in file.readlines()]

    links.remove(link)

    with open(filename, 'w') as file:
        for link in links:
            file.write(f"{link}\n")

def wait_for_page_load(driver, timeout, locator):
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located(locator))
        return True
    except TimeoutException:
        return False

def scrape_website(driver, base_url):
    page_param = 'page='

    driver.get(base_url)
    html_text = driver.page_source

    soup = BeautifulSoup(html_text, 'html.parser')

    item_count_element = soup.find(class_='blm-product-search-toolbar__count')

    if item_count_element:
        item_count = int(item_count_element.text.split('(')[1].split(')')[0])
    else:
        print(f"No items found on {base_url}. Skipping...")
        return

    items_per_page = 32

    num_pages = math.ceil(item_count / items_per_page)

    titles = []
    brands = []
    prices = []
    sizes = []

    for page in range(1, num_pages + 1):
        url = f'{base_url}?{page_param}{page}'

        print(f'Scraping page {url}...')

        driver.get(url)

        max_retries = 3
        retries = 0
        page_loaded = False
        locator = (By.CLASS_NAME, 'product')

        while retries < max_retries and not page_loaded:
            page_loaded = wait_for_page_load(driver, 60, locator)
            if not page_loaded:
                print(f'Page {url} failed to load. Retrying...')
                driver.refresh()
                retries += 1

        if not page_loaded:
            print(f'Page {url} failed to load after {max_retries} retries. Skipping...')
            continue

        html_text = driver.page_source

        soup = BeautifulSoup(html_text, 'html.parser')

        products = soup.find_all(class_='product')

        for product in products:
            title = product.find(class_='card-title').text.strip()
            brand = product.find(class_='card-text').text.strip()

            try:
                price = product.find('div', {'class': 'card-text', 'data-test-info-type': 'price'}).text.strip()
            except AttributeError:
                price = None

            size_element = product.find(class_='Size')

            if size_element:
                sizes_list = size_element.find_all(class_='size-block')
                sizes_str = ', '.join([size['data-size'] for size in sizes_list])
            else:
                sizes_str = None

            titles.append(title)
            brands.append(brand)
            prices.append(price)
            sizes.append(sizes_str)

            print('Title:', title)
            print('Brand:', brand)
            print('Price:', price)
            print('Sizes:', sizes_str)
            print('---')

        print(f'Scraping of page {url} completed.')
        print('---')

    data = []
    for title, brand, price, size in zip(titles, brands, prices, sizes):
        data.append({'Title': title, 'Brand': brand, 'Price': price, 'Sizes': size})

    url_parts = base_url.strip('/').split('/')
    file_name = f"{'_'.join(url_parts[-2:])}.csv"

    folder_name = "scraped_data"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, file_name)
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Title', 'Brand', 'Price', 'Sizes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

    sitemap_file = 'filtered_sitemap_links.txt'
    links = read_links_from_file(sitemap_file)
    
    for base_url in links:
        scrape_website(driver, base_url)
        remove_link_from_file(sitemap_file, base_url)

    driver.quit()