from requests_html import HTMLSession
import pandas as pd
from tqdm import tqdm
import time

s = HTMLSession()

url = 'https://www.flipkart.com/search?q=watch&page=2'

r = s.get(url)
data = []
container = r.html.find('div._2kHMtA')
for item in container:
	try:
		product = item.find('div._4rR01T', first=True).text
	except:
		product = ''
	try:
		rating = item.find('div._3LWZlK', first=True).text
	except:
		rating = ''
	try:
		summary = item.find('ul._1xgFaf', first=True).text
	except:
		summary = ''
	try:
		price = item.find('div._30jeq3._1_WHN1', first=True).text.replace('₹', '')
	except:
		price = ''
	try:
		sprice = item.find('div._3I9_wc._27UcVY', first=True).text.replace('₹', '')
	except:
		sprice = ''
	url = 'https://www.flipkart.com' + item.find('a._1fQZEK', first=True).attrs['href']

	data.append([product, rating, summary, price, sprice, url])
	time.sleep(1)

df = pd.DataFrame(data, columns=['product', 'rating', 'summary', 'price', 'sprice', 'url'])
df.to_csv('Flipkart dataset.csv', index=False)