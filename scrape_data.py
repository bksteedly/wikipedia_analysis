import csv
import json
import urllib.request
from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape_to_csv(file_name):
    #get the url
    search_term = "algorithm"
    offset = 0
    limit = 500
    # Create a CSV file to store the article titles
    csv_file = open(file_name, "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["article", "formatted title", "url"])  # Write the header row

    while True:
        search_url = f"https://en.wikipedia.org/w/index.php?title=Special:Search&limit=500&offset=0&profile=default&search={search_term}"
        response = requests.get(search_url)
        html_content = response.text
        # scrape webpage
        soup = BeautifulSoup(html_content, 'html.parser')
        results = soup.find_all('div', class_='mw-search-result-heading')
        for result in results:
          title = result.find('a').text.replace(" ", "_")
          formatted_title=urllib.parse.quote(title.replace(" ", "_")) # format title for url
          reads_url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/{formatted_title}/monthly/20150701/20230615"
          csv_writer.writerow([title, formatted_title, reads_url])
        # Check if there are more pages
        next_link = soup.find('a', class_='mw-nextlink')
        if not next_link:
          break
        # Update the offset value for the next page
        offset += limit
    csv_file.close()

def get_list_of_urls(file_name, column_name):
  df = pd.read_csv(file_name)
  url_list = df[column_name].tolist()
  return url_list

def get_data(wiki_url_list):
  list_of_dicts = []
  for wiki_url in wiki_url_list:
    with urllib.request.urlopen(wiki_url) as url:
      items_dict = json.loads(url.read().decode())
    # Create a list of dictionaries.
    list_of_dicts.extend( 
    {
     "project": item["project"],
      "article": item["article"],
     "granularity": item["granularity"],
     "timestamp": item["timestamp"],
     "access": item["access"],
     "agent": item["agent"],
     "views": item["views"]
    } for item in items_dict["items"])
  return list_of_dicts

def format_list_of_dicts(list_of_dicts):
    formatted_list = []
    for timestamp_dict in list_of_dicts:
        index = -1
        for item in formatted_list:
            if timestamp_dict["article"] in item.values():
                index = formatted_list.index(item)
        if index != -1:
            formatted_list[index][timestamp_dict["timestamp"]] = timestamp_dict["views"]
        else: 
            formatted_list.append({"article":timestamp_dict["article"],
                                   timestamp_dict["timestamp"]:timestamp_dict["views"]})
    return formatted_list

def append_to_csv(file_name,formatted_list):
    df1 = pd.read_csv(file_name)
    df2 = pd.DataFrame(formatted_list)
    df1.merge(df2).to_csv('final_merged.csv')

def main():
    scrape_to_csv("article_titles.csv")
    url_list = get_list_of_urls("article_titles.csv", "url")
    dict_list = get_data(url_list)
    formatted_dict_list = format_list_of_dicts(dict_list)
    append_to_csv("article_titles.csv", formatted_dict_list)

if __name__ == "__main__":
    main()
