import requests
from bs4 import BeautifulSoup
import time

crawled_links = list()
seed_links = list()
to_visit_links = list()
write_file = open('Task_URL.txt', 'w')
write_URL_links = open('Index.txt', 'w')
MAX_LINKS = 1000

def web_crawler_task (seed, max_depth):
    crawled_links.append(seed)
    to_visit_links.append(seed)
    write_file.write(seed)
    wiki_crawler(max_depth)

def web_crawler_dfs (seed, max_depth):
    seed_links.append("1" + seed)
    depth_first(max_depth)

def web_crawler_bfs (seed,max_depth):
    crawled_links.append(seed)
    to_visit_links.append(seed)
    write_file.write(seed)
    breadth_first(max_depth)

def wiki_crawler(max_depth):
    depth = 1
    while depth <= max_depth:
        seed_links = to_visit_links[:]
        del to_visit_links[:]
        while seed_links:
            url = seed_links.pop(0)
            source_code = requests.get(url)
            plain_text = source_code.text
            soup = BeautifulSoup (plain_text, "html.parser")
            for link in soup.findAll('a'):
                if len(crawled_links) == MAX_LINKS: break
                # politeness policy of 1 second
                time.sleep(1)
                if check_URL(str(link.get('href'))):
                    add_URL_to_list("https://en.wikipedia.org" + str(link.get('href')))
            if not seed_links: depth+=1
        if len(crawled_links) == MAX_LINKS: break
    #write_HTML_files(crawled_links)

def depth_first(max_depth):
    depth = 0
    while seed_links and len(crawled_links) != MAX_LINKS:
        url = seed_links.pop(0)
        depth_value = url[0]
        url = url[1:]
        # The part of the url after the '#' is removed
        if ("#" in url):
            url = url[0:url.index('#')]
        if int(depth_value) > 5:
            continue
        if url not in crawled_links:

            crawled_links.append(url)
            add_URL_to_list_DFS(url)

            try:
                source_code = requests.get(url)
            except requests.exceptions.ConnectionError as e:
                pass
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "html.parser")
            depth= int(depth_value)+1
            index = -1
            for link in soup.findAll('a',href = True):
                # politeness policy of 1 second
                time.sleep(1)
		
                # function to check if the URL contains 'solar' keyword
                if check_solar_URL(link.get('href')):
                    hyperlink = "https://en.wikipedia.org" + str(link.get('href'))
                    if (hyperlink not in crawled_links or check_seed_links(hyperlink,seed_links)):
                        index = index+1
                        seed_links.insert(index, str(depth) + hyperlink)
                # function to check if the anchor text contains 'solar' keyword
		
                elif check_anchor_text(link.get_text()):
		    
                    if check_URL(link.get('href')):
                        hyperlink = "https://en.wikipedia.org" + str(link.get('href'))
                        if (hyperlink not in crawled_links or check_seed_links(hyperlink,seed_links)):
                            index = index+1
                            seed_links.insert(index, str(depth) + hyperlink)

    #write_HTML_files(crawled_links)

def breadth_first(max_depth):
    depth = 1
    while depth <= max_depth:
        seed_links = to_visit_links[:]
        del to_visit_links[:]
        while seed_links:
            url = seed_links.pop(0)
            try:
                source_code = requests.get(url)
            except requests.exceptions.ConnectionError as e:
                pass
            plain_text = source_code.text
            soup = BeautifulSoup (plain_text, "html.parser")
            for link in soup.findAll('a',href = True):
                if len(crawled_links) == MAX_LINKS: break
                # politeness policy of 1 second
                time.sleep(1)
                # function to check if the URL contains 'solar' keyword
		
                if check_solar_URL(link.get('href')):
                    add_URL_to_list("https://en.wikipedia.org" + str(link.get('href')))
                # function to check if the anchor text contains 'solar' keyword
                if check_anchor_text(link.get_text()):
                    if check_URL(link.get('href')):
                        hyperlink = "https://en.wikipedia.org" + str(link.get('href'))
                    add_URL_to_list(hyperlink)
            if not seed_links: depth += 1
        if len(crawled_links) == MAX_LINKS: break

    #write_HTML_files(crawled_links)

# this function checks if the URL crawled from the webpage already exists in the seed_links list
def check_seed_links (hyperlink,seed_links):
    for i in range(0,len(seed_links)):
        url_test = seed_links[i]
        url_test = url_test [1:]
        if hyperlink in url_test:
            return False
    return True

def check_anchor_text (anchor_text):
    anchor_text = anchor_text.encode('utf-8')
    anchor_text = str(anchor_text)
    if ("solar" in anchor_text.lower()) :
        return True
    else: return False

def check_solar_URL (hyperlink):
    hyperlink = hyperlink.encode('utf-8')
    hyperlink = str(hyperlink)
    if (hyperlink.startswith("/wiki")) and  (":" not in hyperlink) and ("solar" in hyperlink.lower()):
        return True
    else: return False

# function to write the URL to the file
def add_URL_to_list_DFS(hyperlink):
    write_file.write(hyperlink)
    write_file.write('\n')
    print(hyperlink)

def check_URL (hyperlink):
    hyperlink = hyperlink.encode('utf-8')
    hyperlink = str(hyperlink)
    if (hyperlink.startswith("/wiki")) and  (":" not in hyperlink):
        return True
    else: return False

def add_URL_to_list (hyperlink):
    if ("#" in hyperlink):
        hyperlink = hyperlink[0:hyperlink.index('#')]
    if (hyperlink not in crawled_links):
        crawled_links.append(hyperlink)
        to_visit_links.append(hyperlink)
        write_file.write('\n')
        write_file.write (hyperlink)
        print(hyperlink)

# this function is used to write the raw files of the crawled web pages
def write_HTML_files(crawled_links):
    for i in range(1,len(crawled_links)+1):
        hyperlink = crawled_links.pop(0)
        HTML_to_text = open('RawFile_' + str(i), 'w')
        try:
            html = BeautifulSoup(urllib.request.urlopen (hyperlink), "html.parser")
        except urllib.error.HTTPError as e:
            HTML_to_text.write("HTTP 404 error: File not found on the web")
        HTML_to_text.write (hyperlink+'\n'+str(html.encode("utf-8")))
        print(hyperlink)
        write_URL_links.write ('RawFile_'+str(i)+': '+ hyperlink+'\n')



