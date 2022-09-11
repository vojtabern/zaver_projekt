import random

from bs4 import BeautifulSoup #scraping
import pandas
import requests
import urllib.request


class Scrape():
    authors = []
    quotes = []
    rand = 1

    # async def get_data(self):
    #     task1 = asyncio.ensure_future(Scrape.scrape_uryvky(self, "autor"))
    #     task2 = asyncio.ensure_future(Scrape.scrape_uryvky(self, "uryvek"))
    #     await asyncio.wait([task1, task2])
    #     print("done")
    #     return("done")

    def scrape_uryvky(self, x):
        page_num = str(1)
        URL = 'https://www.goodreads.com/quotes/tag/inspirational?page=' + page_num
        webpage = requests.get(URL)  # make request
        soup = BeautifulSoup(webpage.text, 'html.parser')  # parse text
        quoteText = soup.find_all('div', attrs={'class': 'quoteText'})
        for i in quoteText:
            quote = i.text.strip().split('\n')[0]
            # 1 quote vrati
            author = i.find('span', attrs={'class': 'authorOrTitle'}).text.strip()
            Scrape.quotes.append(quote)
            Scrape.authors.append(author)

        if x == "uryvek":
            Scrape.rand = random.randrange(0, len(Scrape.quotes))
            return Scrape.quotes[Scrape.rand]
        elif x == "autor":
            return Scrape.authors[Scrape.rand]
        else:
            return -1
        # combine_lists = []
        # for i in range(len(Scrape.quotes)):
        #     combine_lists.append(Scrape.quotes[i]+'-'+Scrape.authors[i])
        # rand = random.randrange(0, len(combine_lists))
        # uryvek = (uryv) = (combine_lists[rand])

        # return uryvek