
# UFC Event Web Scraper

This project is a web scraper that extracts upcoming UFC events from **Tapology**, stores the data in a PostgreSQL database, and then serves the data through a web application. The web application converts the event times from Eastern Time (ET) to the user's local time.

## Features

- Web scrapes Tapology to retrieve upcoming UFC events.
- Stores event details in a PostgreSQL database.
- Serves events via a web application that displays the event data in HTML.
- JavaScript converts event time and date (ET) to the user's local time.

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/ufc-event-webscraper.git
cd ufc-event-webscraper
```

### 2. Set Up the Database

**Create the PostgreSQL database from the provided `schema.sql` file:**

1. **Log into PostgreSQL** (use your terminal or command line):
   ```bash
   psql -U your_username
   ```

2. **Create a new database:**
   ```sql
   CREATE DATABASE ufc_events;
   ```

3. **Run the schema to create tables** (in the `ufc_events` database):
   ```bash
   psql -U your_username -d ufc_events -f path/to/schema.sql
   ```

4. Replace `your_username` with your PostgreSQL username and `path/to/schema.sql` with the actual path to the `schema.sql` file from this repository.

### 3. Set Up Database Credentials

1. Navigate to `src/database/db_credentials.json` and edit the file to include your PostgreSQL database credentials:

   ```json
   {
     "host": "localhost",
     "port": 5432,
     "database": "ufc_events",
     "user": "your_username",
     "password": "your_password"
   }
   ```

### 4. Update the Database with Upcoming Events

Run the `scrape_tapology.py` script to scrape upcoming UFC events and update the database:

```bash
python src/scrape/scrape_tapology.py
```

This will fetch data from Tapology and store it in your database.

### 5. Run the Web Application

Start the web application with the following command:

```bash
python app.py
```

The web application will serve the upcoming UFC events and display them on the webpage. The event time will be displayed in the user's local time.

### 6. Access the Web Application

Once the application is running, you can access it in your browser by navigating to:

```
http://127.0.0.1:5000
```

### 7. (Optional) Re-scrape Data

If you need to update the database with the latest events, simply run the `scrape_tapology.py` script again:

```bash
python src/scrape/scrape_tapology.py
```

---

## Technologies Used

- **Python**: For web scraping and data manipulation.
- **PostgreSQL**: To store and manage the event data.
- **Flask**: For the web application server.
- **JavaScript**: To convert event time from ET to the user's local time.
