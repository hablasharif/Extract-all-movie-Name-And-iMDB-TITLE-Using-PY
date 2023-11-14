import requests
from lxml import html
from tqdm import tqdm
import csv
from concurrent.futures import ThreadPoolExecutor

# User agent string
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"

# Headers with the selected user agent
headers = {
    "User-Agent": user_agent
}

# Create a CSV file and write header
csv_file_path = "2022Moviesimdblink.csv"
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Movie Name', 'IMDb Link'])

def process_page(page_number):
    url = f"https://www.imdb.com/search/title/?title_type=feature&year=2022-01-01,2022-12-31&page={page_number}"
    response = requests.get(url, headers=headers)
    tree = html.fromstring(response.content)

    # XPath to select the movie containers
    xpath = '//div[@class="lister-item-content"]'
    elements = tree.xpath(xpath)

    # Extract IMDb links along with movie names and save to the CSV file
    for element in elements:
        movie_name = element.xpath('.//h3/a/text()')[0]
        movie_link = element.xpath('.//h3/a/@href')[0]
        full_link = f"https://www.imdb.com{movie_link}"
        # Remove unwanted part from the IMDb link
        clean_link = full_link.split("/?")[0]

        # Append the data to the CSV file
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([movie_name, clean_link])

# Number of pages to fetch
pages = list(range(1, 8))

# Use ThreadPoolExecutor to parallelize fetching data
with ThreadPoolExecutor(max_workers=5) as executor:
    list(tqdm(executor.map(process_page, pages), total=len(pages), desc="Fetching Data"))
