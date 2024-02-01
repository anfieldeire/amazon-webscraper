import requests
from bs4 import BeautifulSoup as bs
import csv
import datetime
from datetime import date
import sqlite3
conn = sqlite3.connect('amazon_prices.db')
c = conn.cursor()

'''https://www.geeksforgeeks.org/how-to-compare-rows-and-columns-in-the-same-table-in-sql/'''


def connection():
    conn = sqlite3.connect('amazon_prices.db')
    print("connected")
    return conn

def read_csv():
    # Add check to check that the file has at least one row
  asins = []

  with open('amazon_asins.csv') as f:
      csv_reader = csv.reader(f)
      for row in csv_reader:
          asins.append(row[0])

  return(asins)


def product_info():

#    asins = read_csv()
    base_url = 'https://www.amazon.com/dp/'
    headers = {"accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate,"
    " br","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
               "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}

    products_all = [] # list containing all product - lists (product)

    for asin in asins:
        product_url = base_url + asin
        soup_url = requests.get(product_url, headers=headers)

        if (soup_url.status_code != 200):
            print(f"Error received. Status code{soup_url.status_code}")
    
        else:

            soup = bs(soup_url.text, 'html.parser')
            product = []
            product_dict = {}
            title = soup.find('span',  {'id': 'productTitle'}).text.strip()
            #date = datetime.datetime.today()
            today = date.today()
            price = soup.select_one('span.a-price').select_one('span.a-offscreen').text.strip('$')
            rating = soup.find_all('span', {"class": 'a-icon-alt'})[0].text.split()
            rating = (float(rating[0])) / (int(rating[3]))
            rating = (rating * 100)
            reviews = soup.find_all('span', {"id": 'acrCustomerReviewText'})[0].text.strip('ratings')
            product.append(asin)
            product_dict = {'asin': asin,'title': title,  'scrape_date': today,  'price': price, 'rating': rating, 'reviews': reviews}
            product.append(product_dict)
        products_all.append(product)

    return (products_all)

#product_info()

def load_data():

    conn = sqlite3.connect('amazon_prices.db')
#    c = conn.cursor()
    with conn:
        products_all = product_info()
        if products_all is not None:
            for product_list in products_all:
                print("product list 1 asin")
                print(product_list[1]['asin'])

                conn.execute('''INSERT INTO product_data VALUES(?,?,?,?,?,?)''', (
                product_list[1]['asin'], product_list[1]['title'], product_list[1]['scrape_date'], product_list[1]['price'],
                product_list[1]['rating'], product_list[1]['reviews']))

    #    conn.commit()
    print("data committed")


#load_data()


def price_check():
    ''' Run on today and compare todays data with yesterdays for a price drop '''

    conn = sqlite3.connect('amazon_prices.db')
    c = conn.cursor()

    price_drop = 10
    price_drop_perc = (1- (price_drop / 100))
    # print(price_drop_perc)
    # todays_date = date.today()
    # print(todays_date)
    todays_date = '2024-02-01'
    c.execute('''SELECT a.asin AS asin1, a.title AS title1, a.price AS price1, a.scrape_date as date1, b.asin AS asin2, b.title AS title2, b.price AS price2, b.scrape_date as date2,
            (a.price - b.price) AS difference
    from product_data a, product_data b
    WHERE a.price <> b.price AND b.scrape_date =:todays_date
    AND a.asin = b.asin AND b.price < a.price''', {'todays_date' : todays_date})
    result_list = c.fetchall()
    print("result list")
    print(result_list)
    return
    print(result_list)
    products_all = []

    product_dict = {}
    if result_list is not None:
        for product in result_list:
            item = [] # clear out item each time, so that only one list is added to the bigger list
            product = list(product)
            product_dict = {'asin': product[0], 'title': product[1], 'price_before': product[2], 'price_before_date': product[3], 'price_after': product[6], 'price_after_date': product[7] }
            item.append(product_dict)
            print("product")
            print(product)

            products_all.append(item)
        print("products all")
        print(products_all)
        item = []

    conn.close()

#price_check()


def update_data():
    ''' Search for a product by asin and update the price alert percentage '''
    conn = sqlite3.connect('amazon_prices.db')
    c = conn.cursor()

    input_asin = input("Please enter the product asin: ")
    c.execute("SELECT * from product_data WHERE asin=:asin",
    {'asin': input_asin})
    asin_data = c.fetchone()
    print(asin_data)

    #input_price = input("Please enter the desired price move percentage: ")

    #c.execute("UPDATE product_data SET price_move = price_move WHERE asin=asin ")

#update_data()


if __name__ == '__main__':
    asins = read_csv()
    if asins is not None:
        connection()
    product_info()



