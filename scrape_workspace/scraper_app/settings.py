# simply a global vaiables, much like Django settings.py

BOT_NAME = 'livingsocial'

SPIDER_MODULES = ['scraper_app.spiders']

DATABASE = {
    'drivername': 'postgres', 
    'host': 'localhost',
    'port': '5432',
    'username': 'nharsch',
    'database': 'scrape'
}


