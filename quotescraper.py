from bs4 import BeautifulSoup
import requests
import os
import sys
import pandas as pd

finalquotes = []
finalauthors = []

def quotescraping():
    #there are 100 quotes across 10 pages, scrape every quote by visiting all 10 pages in a loop and pass to an array
    for i in range(1,11):
        x = requests.get(f"https://quotes.toscrape.com/page/{i}")

        soup = BeautifulSoup(x.text,'html.parser')

        quotes = soup.find_all('span',class_='text')
        authors = soup.find_all('small',class_='author')
    
        quotes_scraped = [quote.text for quote in quotes]
        authors_scraped = [author.text for author in authors]
        finalquotes.extend(quotes_scraped)
        finalauthors.extend(authors_scraped)

    data = {
        "Author":finalauthors,
        "Quote":finalquotes
    }
    #pull scraped data into dataframe, convert to csv
    df = pd.DataFrame(data)
    df.to_csv('scrapedquotes.csv') 

def randomquote():
    import random

    df = pd.read_csv('scrapedquotes.csv')
    #read in csv, check for full csv scrape by checking for null values and length of df
    if len(df) != 100 or df.isnull().values.any() == 1:
        print('scrape incomplete')
        sys.exit(1)
    elif len(df) == 100 and df.isnull().values.any() == 0:
        row = df.iloc[random.randint(0,len(df))] #roll random row and print quote and author
        print(f"{row['Quote']}\n{row['Author']}")

if __name__ == '__main__':
        if os.path.exists('scrapedquotes.csv'):
            randomquote()
        else:
            print("scrapedquotes.csv not found, proceeding with scraping")
            quotescraping()
            randomquote()

#initialization logic checks for existing scrape by name of quotescraping() output, if the name is changed the subsequent logic also needs to be edited to match
