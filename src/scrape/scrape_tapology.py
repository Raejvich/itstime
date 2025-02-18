import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime


class WebScraper:
    def __init__(self):
        self.url = "https://www.tapology.com/fightcenter?group=ufc"
        self.event_data = []
        self.structured_event_data = []
        self.event_date = None
        self.event_name = None
        self.event_location = None
        self.fights = []
        self.fighters = []

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

            self.event_data.append(event_raw)

    def convert_date(self):
        """
        Converts date in string format to datetime object, can handle case when year is
        specified and when year is not specified(current year)
        """
        date_str = self.event_date.split(",", 1)[1].strip()
        try:
            # Try parsing the date with the year
            date_obj = datetime.strptime(date_str, "%B %d, %Y, %I:%M %p ET")
        except ValueError:
            # If parsing with year fails, assume no year and use the current year
            current_year = datetime.now().year
            date_obj = datetime.strptime(date_str, "%B %d, %I:%M %p ET")
            date_obj = date_obj.replace(year=current_year)
        self.event_date = date_obj

    def get_fights(self, event):
        self.fights = []
        self.fighters = []
        for entry in event:
            if "vs." in entry:
                entry = entry.split("vs.")  # Split at 'vs'
                entry = [fighter.strip() for fighter in entry]
                self.fights.append(entry)
        self.fighters = [fighter for fight in self.fights for fighter in fight]

    def structure_data(self):
        """
        Example structure:
        [event_obj_1, event_obj_2 ]
            "event_name" : "UFC 312"
            "event_date" : datetime(2020-01-01 18:00)
            "event_location" : "Mexico City"
            "event_fights" : ["fighter 1 vs. figter 2", "fighter 3 vs. fighter 4", etc.]
            "event_fighters" : ["fighter 1", "fighter 2", "fighter 3", etc]
        """
        for event in self.event_data:
            # name is stored in self.event_name or self.event_data[-][0]
            self.event_name = event[0]
            # date is stored in self.event_data[-][1], self.convert_date() to get correct format
            self.event_date = event[1]
            self.convert_date()
            # location stored self.event_data[-][2]
            self.event_location = event[2]
            # fights use vs. as identifier, make function for cleaning
            self.get_fights(event[1:])
            self.structured_event_data.append(
                Event(
                    self.event_name,
                    self.event_date,
                    self.event_location,
                    self.fights,
                    self.fighters,
                )
            )


class Event:
    def __init__(
        self,
        event_name: str,
        event_date: datetime,
        event_location: str,
        event_fights: list,
        event_fighters: list,
    ):
        self.event_name = event_name
        self.event_date = event_date
        self.event_location = event_location
        self.event_fights = event_fights
        self.event_fighters = event_fighters

    def __repr__(self):
        return (
            f"Event(\n"
            f"  event_name={self.event_name!r},\n"
            f"  event_time={self.event_date!r},\n"
            f"  event_location={self.event_location!r},\n"
            f"  event_fights={self.event_fights!r},\n"
            f"  event_fighters={self.event_fighters!r}\n"
            f")"
        )


if __name__ == "__main__":
    fight_data = WebScraper()
    fight_data.get_event_data()
    fight_data.structure_data()

    print(fight_data.structured_event_data[-1])
