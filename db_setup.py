import sqlite3

conn = sqlite3.connect('amazon_prices.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS product_data (
        asin string NOT NULL,
        title text,
        scrape_date date, 
        price float,
        rating string,
        reviews string, 
        PRIMARY KEY(asin, scrape_date)
    )""")
conn.commit()
conn.close
