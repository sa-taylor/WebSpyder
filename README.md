Web Scraping Project

This project extracts data from the website (http://levelninesports.com) by following all links provided in the site map, then combines the scraped data into a single file and performs some light processing on it.


Requirements
To run this project, you will need Python 3 and the following Python packages:

Python 3.x
concurrent.futures
selenium
chromedriver (for selenium)
beautifulsoup4
requests

You can install them all using pip with the following command:
pip install -r requirements.txt


In addition, the project includes the following Python files:

sitemap_parse.py: contains functions to retrieve and parse sitemap links
scrape.py: contains functions to scrape data from websites
combine_data.py: contains functions to combine and process scraped data
main.py: the main script that orchestrates the scraping process


Usage

To use this scraping tool, you can run the main.py file.

Or you can run the individual scripts separately: First, you need to generate a list of URLs from the site map. You can do this by running python get_sitemap_urls.py. This will save a list of URLs to sitemap_urls.txt. If you want to filter the URLs to only include certain parent links, you can edit the filter_parent_links function in the sitemap_parse.py file.
Next, you can scrape data from each of the URLs by running python scrape_data.py. This will save the scraped data to individual text files in the scraped_data directory. You can customize the scraping process by editing the scrape_website function in the scrape.py file, such as changing the CSS selectors to scrape different data.
Finally, you can combine the scraped data into a single file by running python combine_data.py. This will save the combined data to all_extracted_data.csv. You can customize the output fields by editing the fieldnames variable in the combine_csv_files function in the combine_data.py file.

To change the target website, modify the URL in get_sitemap_urls.py.
To customize the scraping process, modify the code in scrape_data.py.
To modify the data processing performed in combine_data.py, adjust the relevant code.

Notes:
This project is intended for educational purposes only. Before scraping any website, ensure that you have the legal right to do so.
Scraping websites can put a heavy load on servers and impact the performance of the website. Use with caution and be respectful of the target website's resources.