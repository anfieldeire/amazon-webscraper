import sqlite3

INSERT_PRODUCTS = "INSERT INTO product_data VALUES(?,?,?,?,?,?);"

PRICE_CHECK = """SELECT a.asin AS asin1, a.title AS title1, a.price AS price1, a.scrape_date as date1, b.asin AS asin2, b.title AS title2, b.price AS price2, b.scrape_date as date2,
(a.price - b.price) AS difference from product_data a, product_data b
WHERE a.price <> b.price AND b.scrape_date =:todays_date AND a.asin = b.asin AND b.price < a.price"""
