import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime


def request_html():
    """
    Requests HTML code and returns beautifulsoup objects
    """
    url = "https://www.tapology.com/fightcenter?group=ufc"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    else:
        logging.error("Failed to retrieve the page")


def get_event_dict():
    """
    Calls request_html() and extracts the event name, event time, main card fighters,
    and location. This is stored as json file
    """
    event_dict = dict()

    soup = request_html()
    # Find all event containers (parent divs that hold event names and times)
    event_containers = soup.find_all("div", attrs={"data-controller": "bout-toggler"})

    for event in event_containers:
        # Extract event name
        event_name_tag = event.find(
            "a", class_="border-b border-tap_3 border-dotted hover:border-solid"
        )
        event_name = event_name_tag.get_text(strip=True) if event_name_tag else "N/A"

        # Extract event time (Desktop version)
        event_time_tag = event.find("span", class_="hidden md:inline")
        event_time = event_time_tag.get_text(strip=True) if event_time_tag else "N/A"

        date_obj = convert_date(event_time)

        event_dict[
            event_name:{
                "date": date_obj,
                "fighter_1": None,
                "fighter_2": None,
                "location": None,
            }
        ]


def convert_date(event_time):
    """
    Converts date in string format to datetime object, can handle case when year is
    specified and when year is not specified(current year)
    """
    date_str = event_time.split(",", 1)[1].strip()
    try:
        # Try parsing the date with the year
        date_obj = datetime.strptime(date_str, "%B %d, %Y, %I:%M %p ET")
    except ValueError:
        # If parsing with year fails, assume no year and use the current year
        current_year = datetime.now().year
        date_obj = datetime.strptime(date_str, "%B %d, %I:%M %p ET")
        date_obj = date_obj.replace(year=current_year)

    return date_obj


if __name__ == "__main__":

    # get_event_dict()
    convert_date("Saturday, May 31, 2024, 6:00 PM ET")
