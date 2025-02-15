from src.scrape.scrape_tapology import WebScraper
from src.database.database import DataBaseConnect

# Create web scraper object
scraper = WebScraper()
# get raw event data
scraper.get_event_data()
# get structured data
scraper.structure_data()

# iterate throug every event an insert into DB
for event in scraper.structured_event_data:
    pass
