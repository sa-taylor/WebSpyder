import requests
from bs4 import BeautifulSoup
    
def get_sitemap(url):
    # Fetch the sitemap at the given URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the 'Categories' tag
        categories_tag = soup.find('h3', string='Categories')

        # If the tag is found, extract the sitemap links
        if categories_tag:
            sitemap_links = []

            for sibling in categories_tag.find_next_siblings():
                if sibling.get('data-content-region') == 'page_builder_bottom_content':
                    break
                for tag in sibling.find_all('a'):
                    if 'href' in tag.attrs:
                        sitemap_links.append(tag['href'])

            return sitemap_links
        else:
            print("Error: Unable to find the Categories tag.")
            return None
    else:
        print("Error: Unable to fetch the sitemap.")
        return None

def save_links_to_file(links, filename):
    # Save the given list of links to a file
    with open(filename, 'w') as file:
        for link in links:
            file.write(f"{link}\n")

def filter_parent_links(links):
    # Filter out parent links from the given list of links
    filtered_links = []
    for link in links:
        is_parent = False
        for other_link in links:
            if other_link.startswith(link) and other_link != link:
                is_parent = True
                break
        if not is_parent:
            filtered_links.append(link)
    return filtered_links

if __name__ == '__main__':
    # Get the sitemap links and filter out parent links
    sitemap_url = 'https://www.levelninesports.com/sitemap/categories/'
    sitemap_links = get_sitemap(sitemap_url)

    if sitemap_links:
        filtered_links = filter_parent_links(sitemap_links)
        print("Filtered sitemap links:")
        for link in filtered_links:
            print(link)
        
        # Save the filtered links to a file
        save_links_to_file(filtered_links, 'filtered_sitemap_links.txt')