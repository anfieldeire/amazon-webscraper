
Webscraper for amazon product price information with sqlite
 - A program that reads a csv file containing amazon product numbers (asins) and uses that to search for products on amazon
 - It extracts product information and loads that into a sql lite database
 - The program is intended to run once a day, and compares todays price to the previous days price. (DB primary key is both asin and scrape date, so this can only run once daily - unless the scrape date is changed manually in the DB)
 - If there is a decrease it will trigger an email alert to the configured email with product and price information
 - The csv file is one column with no header, containing asin numbers on each row

Versions
- pip version: 23.3.2
- python version: 3.12
  
Virtual Environment Instructions
 - Create the virtual environment: virtualenv amazon-webscraper
 - Activate: Navigate to the scripts directory and run the activate file to activate the virtual environment
 - Install package dependencies: python -m pip install -r requirements.txt

Email
 - Setup an email account and enable it to send email
 - Create an environment variable on your machine that contains the email password
 - Run the program. Check for a plain text email

Program Outline
 - db_setup.py - creates the sqlite db
 - database.py - contains the queries
 - main.py - the main program. 
 - send_email.py - creates and sends the email message
  
