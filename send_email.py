import os
from email.message import EmailMessage
import ssl
import smtplib


email_sender = 'email@gmail.com'
email_pass = os.environ.get("PYTHON_EMAIL")
email_receiver = 'email@gmail.com'
subject = 'Price Drop Alert'




def create_message(products_all):
    body = 'Price Drop In The Following Products:\n'
    print(products_all)

    for product in products_all:
        body = body + "\n"

        asin = [dictionary["asin"] for dictionary in product]
        asin = str(asin).strip("[' ']")
        title =  [dictionary["title"] for dictionary in product]
        title = str(title).strip("[' ']")
        price_before = [dictionary["price_before"] for dictionary in product]
        price_before = str(price_before).strip("[' ']")
        price_after = [dictionary["price_after"] for dictionary in product]
        price_after = str(price_after).strip("[' ']")
        product_text = f'Product asin: {asin}. \nTitle: {title}.\nPrevious Price: {price_before}, price now: {price_after}\n'

        body = body + product_text
    return body



def email_message(products_all, body):

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    em.set_content(body)


    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_pass)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

#email_message()