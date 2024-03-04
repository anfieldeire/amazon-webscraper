import requests
from bs4 import BeautifulSoup as bs
import csv
import datetime
from datetime import date, timedelta
import sqlite3
import os
from database import INSERT_PRODUCTS, PRICE_CHECK
from database import connection
from send_email import create_message, email_message



def read_csv():

    ''' Check the file is present in the current dir. Check that the file has data '''

    input_file = 'amazon_asins.csv'
    asins = []

    try:
        with open(input_file) as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if row == []: # check for empty row
                    raise ValueError('Empty File')
                else:
                    asins.append(row[0])

    except  FileNotFoundError as fnf_error:
        print(fnf_error)
    return(asins)

read_csv()

def scrape_data(asins):

    ''' Scrape product data from amazon using the asins '''

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


def load_data(products_all, conn):

    ''' load the scraped data into the database once daily '''

    with conn:

        if products_all is not None:
            for product_list in products_all:
                print("product list 1 asin")
                print(product_list[1]['asin'])

                conn.execute(INSERT_PRODUCTS, (
                product_list[1]['asin'], product_list[1]['title'], product_list[1]['scrape_date'], product_list[1]['price'],
                product_list[1]['rating'], product_list[1]['reviews']))

    print("data committed")


def price_check(conn):
    ''' Run on today and compare todays data with yesterdays for a price drop '''

    price_drop = 10
    price_drop_perc = (1- (price_drop / 100))
    todays_date = date.today()
    yest_date = todays_date - timedelta(1)
    c = conn.cursor()
    c.execute(PRICE_CHECK, {'todays_date': todays_date, 'yest_date': yest_date})

    result_list = c.fetchall()
    products_all = []
    product_dict = {}
    if result_list is not None:
        for product in result_list:
            item = [] # clear out item each time, so that only one list is added to the bigger list
            product = list(product)
            product_dict = {'asin': product[0], 'title': product[1], 'price_before': product[2], 'price_before_date': product[3], 'price_after': product[6], 'price_after_date': product[7] }
            item.append(product_dict)
            products_all.append(item)

    return products_all


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
    conn = connection()
    products_all = scrape_data(asins)
    load_data(products_all, conn)
    products_all = price_check(conn)
    body = create_message(products_all)
    email_message(products_all, body)



