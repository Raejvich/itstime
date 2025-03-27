# UFC Event Web Scraper

This project is a web scraper that extracts upcoming UFC events from **Tapology**, orchestrates the data pipeline using **Apache Airflow**, and loads the data into a **PostgreSQL** database. The web application serves the scraped data and dynamically converts event times from Eastern Time (ET) to the user's local time.

![Project GIF](static/images/readmegif.gif)

## Features

- Utilizes **Apache Airflow** for scheduling and orchestrating the scraping process from Tapology.
- Extracts and stores event details in a **PostgreSQL** database.
- Uses **Docker** for containerization and deployment on **Railway**.
- Serves event data via a **Flask** web application.
- JavaScript dynamically converts event times from ET to the user's local time.

## Technologies Used

- **Python**: For web scraping and data manipulation.
- **Apache Airflow**: To orchestrate and automate the web scraping workflow.
- **PostgreSQL**: To store and manage event data.
- **Flask**: For the web application backend.
- **JavaScript**: To convert event time from ET to the user's local time.
- **Docker**: To containerize the application for easy deployment.
- **Railway**: For cloud deployment and hosting.

This setup ensures automation, scalability, and seamless deployment of the web scraping and data presentation pipeline.

