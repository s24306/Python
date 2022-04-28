import requests
from bs4 import BeautifulSoup
import string
import os

url = 'https://www.nature.com/nature/articles'
number_of_pages = int(input('Insert number of pages'))
chosen_tag = input('Choose a tag')
page = 1

try:
    while page <= number_of_pages:
        r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        soup = BeautifulSoup(r.content, 'html.parser')
        if r.status_code != 200:
            print(f"The URL returned {r.status_code}")
        else:
            os.mkdir(f'Page_{page}')
            os.chdir(f'Page_{page}')
            tags = list(enumerate(tag.get_text() for tag in soup.find_all('span', class_="c-meta__type")))
            links = list(enumerate(
                link['href'] for link in soup.find_all('a', class_="c-card__link u-link-inherit", href=True)))
            for i in range(len(tags)):
                if chosen_tag == tags[i][1]:
                    if chosen_tag != 'Research Highlight':
                        article_link = requests.get(
                         'https://www.nature.com' + links[i][1], headers={'Accept-Language': 'en-US,en;q=0.5'})
                        article_soup = BeautifulSoup(article_link.content, 'html.parser')
                        article_title = article_soup.find('h1').get_text()
                        article_title = article_title.translate(str.maketrans('', '', string.punctuation))
                        article_title = article_title.replace(' ', '_')
                        article = article_soup.find("div", class_='article__body cleared').text.strip()
                        article_file = open('%s.txt' % article_title, 'w', encoding='UTF-8')
                        article_file.write(article)
                        article_file.close()
                    else:
                        article_link = requests.get(
                            'https://www.nature.com' + links[i][1], headers={'Accept-Language': 'en-US,en;q=0.5'})
                        article_soup = BeautifulSoup(article_link.content, 'html.parser')
                        article_title = article_soup.find('h1').get_text()
                        article_title = article_title.translate(str.maketrans('', '', string.punctuation))
                        article_title = article_title.replace(' ', '_')
                        article = article_soup.find("div", class_='article-item__body').text.strip()
                        article_file = open('%s.txt' % article_title, 'w', encoding='UTF-8')
                        article_file.write(article)
                        article_file.close()
                else:
                    continue
        os.chdir(os.path.dirname(os.getcwd()))
        page += 1
        url = 'https://www.nature.com' + f'/nature/articles?searchType=journalSearch&sort=PubDate&page={page}'
except Exception:
    print(f"The URL returned {r.status_code}")
