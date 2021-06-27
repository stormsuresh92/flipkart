from requests_html import HTMLSession
import pandas as pd

sesssion = HTMLSession()

def page(x):
    base_url = 'https://www.flipkart.com'
    url = f'https://www.flipkart.com/search?q={searchTerm}&page={x}'
    r = sesssion.get(url)
    results =  r.html.find('div._1AtVbE.col-12-12 > div > div > div > a')
    links = []
    for url in results:
        hrefs = url.find('a', first=True).attrs['href']
        links.append(base_url + hrefs)
    return links

def get_productdata(link):
    
    r = sesssion.get(link)
    try:
        Product_name = r.html.find('span.B_NuCI', first=True).text.replace('\xa0', '')
    except:
        Product_name = ''
    try:
        Product_Price = r.html.find('div._30jeq3._16Jk6d', first=True).text.replace('₹', '')
    except:
        Product_Price = ''
    try:
        Rating_out_of_5 = r.html.find('div._3LWZlK', first=True).text
    except:
        Rating_out_of_5 = ''
    try:
        Highlights = r.html.find('div._2418kt', first=True).text.replace('\n', ' ')
    except:
        Highlights = ''
     
    scrapedata = {
        'Product_name' : Product_name,
        'Product_Price' : Product_Price,
        'Rating' : Rating_out_of_5,
        'Highlights' : Highlights
                       
    }
      
    return scrapedata

searchTerm = input('Enter product name here:')
mainlist = []
for x in range(0, 2):
    links = page(x)
    for link in links:
        mainlist.append(get_productdata(link))
    print('Getting page:', x+1, '-', len(page(x)), 'products')
          
df = pd.DataFrame(mainlist)
df.to_excel(f'{searchTerm}' + '.xlsx', index=False)
print('Download completed')