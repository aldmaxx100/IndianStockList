from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import pytz
import sys
import pandas as pd


def getData(url,filename):
    final = []
    letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','others']
    for letter in letters:
        response = requests.get(url.format(start=letter))
        print(response.status_code, letter)
        string = response.content.decode('utf-8')
        soup = BeautifulSoup(string, 'html.parser')

        tables = soup.find_all('table', {'class': 'dataTable'})

        for table in tables:
            rows = table.find_all('tr')
            for r in rows:

                name = r.find_all('td')
                # print(name)
                if len(name) > 0:
                    cname = name[0].find('a').text.replace('\t', '').replace('\n', '')
                    code = name[1].text.replace('\t', '').replace('\n', '')
                    final.append([cname, code, datetime.now().strftime('%Y-%m-%d')])

    df = pd.DataFrame(final, columns=['Company', 'Code', 'UpdationDate'])
    df.drop_duplicates(inplace=True)
    print(df)
    df.to_csv(filename, index=False)

if __name__=='__main__':
    bseurl = 'https://money.rediff.com/companies/{start}'
    nseurl = 'https://money.rediff.com/companies/nseall/{start}'
    getData(bseurl,'bselisted.csv')
    getData(nseurl,'nselisted.csv')
