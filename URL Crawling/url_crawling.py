
import pandas as pd
import requests
from bs4 import BeautifulSoup

url1 = input("Enter the URL to be Crawled:")
url = str(url1)
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

A = []
for el in soup.findAll('p'):
    A.append(el.get_text().strip().lower())


df = pd.DataFrame(columns=['Text'])

for i in range(len(A)):
    df.loc[i] = [A[i]]

df.to_csv('Text1', index=False)
