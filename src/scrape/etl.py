from src.scrape.scrape_tapology import WebScraper
from src.database.database import DataBaseConnect
import json

# Create web scraper object
scraper = WebScraper()
# get raw event data
scraper.get_event_data()
# get structured data
scraper.structure_data()

with open("src/database/db_credentials.json", "r") as file:
    db_credentials = json.load(file)

admin = DataBaseConnect(
    db_credentials["database"],
    db_credentials["username"],
    db_credentials["password"],
)
# connect to DB
admin.connect()
# delete current events
admin.delete_events()
# iterate through every event an insert into DB
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
# commit deletion and insert at the same time
admin.conn.commit()
admin.close()
