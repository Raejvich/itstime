from src.scrape.scrape_tapology import WebScraper
from src.database.database import DataBaseConnect

# Create web scraper object
scraper = WebScraper()
# get raw event data
scraper.get_event_data()
# get structured data
scraper.structure_data()

admin = DataBaseConnect("itstime_db", "admin", "pw_admin")
# connect to DB
admin.connect()
# iterate throug every event an insert into DB
for event in scraper.structured_event_data:
    id = admin.insert_event(
        event_name=event.event_name,
        event_date=event.event_date,
        event_location=event.event_location,
    )
    for order, fight in enumerate(event.event_fights):
        admin.insert_fight(
            event_id=id, fighter_1=fight[0], fighter_2=fight[1], fight_order=order
        )
