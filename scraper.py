from fileinput import filename
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASEURL = "https://www.thewhiskyexchange.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
FILEDIR = "./"
FILENAME = "whisky_products"

k = requests.get('https://www.thewhiskyexchange.com/c/35/japanese-whisky').text
soup = BeautifulSoup(k,'html.parser')
productlist = soup.find_all("li",{"class":"product-grid__item"})
# print(productlist)

start_time = time.time()
productlinks = []
for product in productlist:
        link = product.find("a",{"class":"product-card"}).get('href')                 
        productlinks.append(BASEURL + link)
        # print(productlinks)
        # break
print("Get product URLs completed.")

productlinks = []
for x in range(1,6):  
    k = requests.get('https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={}&psize=24&sort=pasc'.format(x)).text  
    soup=BeautifulSoup(k,'html.parser')  
    productlist = soup.find_all("li",{"class":"product-grid__item"})
 
    for product in productlist:
        link = product.find("a",{"class":"product-card"}).get('href')
        productlinks.append(BASEURL + link)
print("Get product elements completed.")

data=[]
for link in productlinks:
    f = requests.get(link, headers=HEADERS).text
    hun = BeautifulSoup(f,'html.parser')

    try:
        price = hun.find("p",{"class":"product-action__price"}).text.replace('\n',"")
    except:
        price = None

    try:
        about = hun.find("div",{"class":"product-main__description"}).text.replace('\n',"")
    except:
        about = None

    # try:
    #     rating = hun.find("div",{"class":"review-overview"}).text.replace('\n',"")
    # except:
    #     rating = None

    try:
        rating = hun.find("span", class_="review-overview__rating").text.strip()
    except:
        rating = None

    try:
        review_count = hun.find("span", class_="review-overview__count").text
        review_count = review_count.encode('ascii', errors='ignore').decode("utf-8").split("Re", 1)[0].replace("(","").strip()
    except:
        review_count = None

    try:
        name = hun.find("h1",{"class":"product-main__name"}).text.replace('\n',"")
    except:
        name = None

    try:
        made_style = hun.find("ul", class_="product-main__meta")
        made_style = list(made_style.descendants)[1].text.strip()
    except:
        made_style = None

    try:
        img_url = hun.find("img", class_="product-main__image")["src"]
    except:
        img_url = None

    whisky = {
        "name":name,
        "made style":made_style,
        "price":price,
        "rating":rating,
        "Number of reviews":review_count,
        "about":about,
        "image_url":img_url,
        }
    data.append(whisky)
    # print(data)
    # break

print("Get product details completed.")
print("Scraping is finished in %s seconds." % (time.time()-start_time))

df = pd.DataFrame(data)
print(df.head())

df.to_excel("%s.xlsx" % (FILEDIR + FILENAME))
df.to_csv("%s.csv" % (FILEDIR + FILENAME), index=False)
print("Data is already saved to xlsx and csv format.")




