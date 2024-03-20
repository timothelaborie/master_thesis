# Importing necessary libraries:
# - os, json, time for file, data and time operations respectively.
# - requests for making HTTP requests.
# - BeautifulSoup for parsing HTML content.
# - Other imports for logging, data manipulation, progress indication, and more.
import os
import json
import time
import munch
import requests
import argparse
import pandas as pd
from tqdm import tqdm
from datetime import date
from loguru import logger
from random import randint
from bs4 import BeautifulSoup, NavigableString

from preprocessing.preprocessing_sub_functions import remove_emojis
from torch import save,load


# This function reads a JSON file named "website_format.json".
# The file contain a list of user agents.
# User agents are strings that browsers send to websites to identify themselves.
# This list is likely used to rotate between different user agents when making requests,
# making the scraper seem like different browsers and reducing the chances of being blocked.
def get_web_component():
    # Opening JSON file
    with open("website_format.json") as json_file:
        website_format = json.load(json_file)
    website_format = munch.munchify(website_format)
    return website_format.USER_AGENTS


# This function fetches a webpage's content.
# It randomly selects a user agent from the provided list to make the request.
# After fetching, it uses BeautifulSoup to parse the page's HTML content.
def get_web_content(url, USER_AGENTS):
    if os.path.exists("cache.pt"):
        cache = load("cache.pt")
        if url in cache:
            return cache[url]
    else:
        cache = {}
    random_agent = USER_AGENTS[randint(0, len(USER_AGENTS) - 1)]
    headers = {"User-Agent": random_agent}
    req = requests.get(url, headers=headers)
    req.encoding = req.apparent_encoding
    soup = BeautifulSoup(req.text, features="lxml")
    cache[url] = soup
    save(cache, "cache.pt")
    return soup


# This function extracts pagination links from a page.
# These links point to other pages of content, often seen at the bottom of forums or search results.
# The function returns both the individual page links and the "next" link,
# which points to the next set of results.
def get_pages_urls(url, USER_AGENTS, next_50_pages):
    time.sleep(1)
    soup = get_web_content(url, USER_AGENTS)
    # Finding the pagination links based on their HTML structure and CSS classes.
    first_td = soup.find('td', class_='middletext')
    nav_pages_links = first_td.find_all('a', class_='navPages')
    href_links = [link['href'] for link in nav_pages_links]

    next_50_link = None
    if next_50_pages:
        next_50_link = href_links[-3] # HACK: Assuming the third-last link is the "next" link.

    href_links.insert(0, url)
    return href_links, next_50_link

# This function loops through the main page and its paginated versions to collect URLs.
# It repeatedly calls 'get_pages_urls' to fetch batches of URLs until the desired number (num_of_pages) is reached.
def loop_through_source_url(USER_AGENTS, url, num_of_pages):
    pages_urls = []
    while len(pages_urls) < num_of_pages:
        time.sleep(0.8)
        next_50_pages = num_of_pages >= 50
        href_links, next_50_link = get_pages_urls(url, USER_AGENTS, next_50_pages)
        pages_urls.extend(href_links)
        pages_urls = list(dict.fromkeys(pages_urls))  # Remove any duplicate URLs.
        url = next_50_link
    return pages_urls

def get_subpages_urls(url, USER_AGENTS):
    soup = get_web_content(url, USER_AGENTS)
    middletext = soup.find('td', class_='middletext')
    nav_pages_links = middletext.find_all('a', class_='navPages')

    return nav_pages_links[:-1]

def loop_through_posts(USER_AGENTS, post_url, board, num_of_pages, remove_emoji):
    # print("loop_through_posts: num_of_pages =",num_of_pages)
    try:
        href_links = loop_through_source_url(USER_AGENTS, post_url, num_of_pages)

        df = pd.DataFrame(columns=['timestamp', 'last_edit', 'author', 'post', 'topic', 'attachment', 'link', 'original_info'])

        for url in tqdm(href_links):
            df = read_subject_page(USER_AGENTS, url, df, remove_emoji)

        topic_id = post_url.split('topic=')[1]
        df.to_csv(f'data/{board}/data_{topic_id}.csv', mode='w', index=False)

    except Exception as e:
        print(e)
        with open(f"data/{board}/error_log.txt", "a") as f:
            f.write(f"{post_url}\n -- {e}\n")

# This function processes a post page. It extracts various details like timestamps, author information, post content, topic, attachments, links, and original HTML information.
# The function returns a dictionary containing all this extracted data.
def read_subject_page(USER_AGENTS, post_url, df, remove_emoji):
    time.sleep(1)
    soup = get_web_content(post_url, USER_AGENTS)
    form_tag = soup.find('form', id='quickModForm')
    table_tag = form_tag.find('table', class_='bordercolor')
    td_tag = table_tag.find_all('td', class_='windowbg')
    td_tag.extend(table_tag.find_all('td', class_='windowbg2'))
    
    for comment in td_tag:
        res = extract_useful_content_windowbg(comment, remove_emoji)
        if res is not None:
            df = pd.concat([df, pd.DataFrame([res])])
    
    return df

# This function extracts meaningful content from a given HTML element (`tr_tag`). This tag is likely a row in a table, given its name.
# The function checks the presence of specific tags and classes within this row to extract information such as timestamps, author, post content, topic, attachments, and links.
# The extracted data is returned as a dictionary.
def extract_useful_content_windowbg(tr_tag, remove_emoji=True):
    """
    Timestamp of the post (ex: September 11, 2023, 07:49:45 AM; but if you want just 11/09/2023 is enough)
    Author of the post (ex: SupermanBitcoin)
    The post itself
    
    The topic where the post was posted (ex: [INFO - DISCUSSION] Security Budget Problem) eg.  Whats your thoughts: Next-Gen Bitcoin Mining Machine With 1X Efficiency Rating.
    Number of characters in the post --> so this is an integer
    Does the post contain at least one attachment (image, video etc.) --> if yes put '1' in the column, if no, just put '0'
    Does the post contain at least one link --> if yes put '1' in the column, if no, just put '0'
    """
    headerandpost = tr_tag.find('td', class_='td_headerandpost')
    if not headerandpost:
        return None
    
    timestamp = headerandpost.find('div', class_='smalltext').get_text()
    timestamps = timestamp.split('Last edit: ')
    timestamp = timestamps[0].strip()
    last_edit = None
    if len(timestamps) > 1:
        if 'Today ' in timestamps[1]:
            last_edit = date.today().strftime("%B %d, %Y")+', '+timestamps[1].split('by')[0].split("Today at")[1].strip()
        last_edit = timestamps[1].split('by')[0].strip()

    poster_info_tag = tr_tag.find('td', class_='poster_info')
    anchor_tag = poster_info_tag.find('a')
    author = "Anonymous" if anchor_tag is None else anchor_tag.get_text()

    link = 0

    post_ = tr_tag.find('div', class_='post')
    texts = []
    for child in post_.children:
        if isinstance(child, NavigableString):
            texts.append(child.strip())
        elif child.has_attr('class') and 'ul' in child['class']:
            link = 1
            texts.append(child.get_text(strip=True))
    post = ' '.join(texts)

    topic = headerandpost.find('div', class_='subject').get_text()

    image = headerandpost.find('div', class_='post').find_all('img')
    if remove_emoji:
        image = remove_emojis(image)
    image_ = min(len(image), 1)
    
    video = headerandpost.find('div', class_='post').find('video')
    video_ = 0 if video is None else 1
    attachment = max(image_, video_)

    original_info = headerandpost

    return {
        'timestamp': timestamp, 
        'last_edit': last_edit, 
        'author': author.strip(), 
        'post': post.strip(), 
        'topic': topic.strip(), 
        'attachment': attachment, 
        'link': link, 
        'original_info': original_info,
    }



# A utility function to save a list (e.g., URLs) to a text file.
# Each item in the list gets its own line in the file.
def save_page_file(data, file_name):
    with open(file_name, 'w') as filehandle:
        for listitem in data:
            filehandle.write('%s\n' % listitem)


# This function sets up command-line arguments for the script, allowing users to provide input without modifying the code.
# Possible inputs include the starting URL, whether or not to update data, the board's name, and how many pages or posts to process.
def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url for the extraction")
    parser.add_argument("--board", help="board name")
    parser.add_argument("--num_of_pages", '-pages', help="number of pages to extract", type=int)
    parser.add_argument("remove_emoji", help="remove emoji from the post", action="store_true")
    return vars(parser.parse_args())


def main(url, board, num_of_pages, remove_emoji):
    USER_AGENTS = get_web_component()
    loop_through_posts(USER_AGENTS, url, board, num_of_pages, remove_emoji)
    


if __name__ == "__main__":
    main(**parse_args())

# python topic_crawling.py https://bitcointalk.org/index.php?topic=28402.0 --board miners --num_of_pages 843