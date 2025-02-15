import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime


class WebScraper:
    def __init__(self):
        self.url = "https://www.tapology.com/fightcenter?group=ufc"
        self.event_data = []
        self.event_time = None
        self.event_name = None

    def request_html(self):
        """
        Requests HTML code and returns beautifulsoup objects
        """
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        else:
            logging.error("Failed to retrieve the page")

    def get_event_data(self):
        """
        Calls request_html() and extracts the event name, event time, main card fighters,
        and location. This is stored as json file
        """
        soup = self.request_html()
        # Find all event containers (parent divs that hold event names and times)
        event_containers = soup.find_all(
            "div", attrs={"data-controller": "bout-toggler"}
        )

        for event in event_containers:
            # Extract event name
            event_name_tag = event.find(
                "a", class_="border-b border-tap_3 border-dotted hover:border-solid"
            )
            self.event_name = (
                event_name_tag.get_text(strip=True) if event_name_tag else "N/A"
            )

            # Initialize a list to hold the event times
            event_raw = []
            event_raw.append(self.event_name)
            # Find all the span elements with the given class
            span_tags = event.find_all("span", class_="hidden md:inline")

            # Loop through span tags and collect them
            for span_tag in span_tags:
                event_raw.append(span_tag.get_text(strip=True))

            # Store all collected event times, if any
            self.event_times = event_raw if event_raw else "N/A"

            self.event_data.append(event_raw)

    def convert_date(self):
        """
        Converts date in string format to datetime object, can handle case when year is
        specified and when year is not specified(current year)
        """
        date_str = self.event_time.split(",", 1)[1].strip()
        try:
            # Try parsing the date with the year
            date_obj = datetime.strptime(date_str, "%B %d, %Y, %I:%M %p ET")
        except ValueError:
            # If parsing with year fails, assume no year and use the current year
            current_year = datetime.now().year
            date_obj = datetime.strptime(date_str, "%B %d, %I:%M %p ET")
            date_obj = date_obj.replace(year=current_year)
        self.event_time = date_obj


if __name__ == "__main__":
    fight_data = WebScraper()
    fight_data.get_event_data()
    print(fight_data.event_data)
