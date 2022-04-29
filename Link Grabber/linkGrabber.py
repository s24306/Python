from googlesearch import search
import requests
from bs4 import BeautifulSoup
import csv


def join_results(hits_list):
    hits = ''
    for x in hits_list:
        hits += str(x)
    return hits


def grab_links(site, word):
    links_list = []
    for l in search(site+word, tld='com', lang='en', num=10, start=0, stop=10, pause=2.0):
        links_list.append(l)
    return links_list


def grab_results(site, word):
    with requests.Session() as s:
        url = f"http://www.google.com/search?q={site}+{word}"
        headers = {
            "referer":"referer: https://www.google.com/",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                         " (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
            }
        s.post(url, headers=headers)
        response = s.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        result_list = soup.find_all(id='result-stats')[0].text
        results_string = join_results([int(s) for s in result_list.split() if s.isdigit()])
    return f"{word}: {results_string}"


keywords = open('keywords.txt', 'r').read().split(" ")
query = 'site:https://www.searchenginejournal.com/'

for w in keywords:
    links = grab_links(query, w)
    with open("links.csv", "a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
        for link in links:
            file_writer.writerow(link)
    results = grab_results(query, w)
    with open("results.csv", "a", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
        for result in results:
            file_writer.writerow(result)
