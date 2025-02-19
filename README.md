# Conflict of Nations Stats Scraper

This project scrapes game statistics from **Conflict of Nations** using Selenium and processes the data for
visualization.

## Features

- Automated data scraping with Selenium
- Data processing and handling
- Basic visualization of game statistics

## Requirements

- Python 3.x
- Google Chrome
- ChromeDriver (included in `chromedriver-win64/` or can be downloaded from the internet)
- Required Python libraries (listed in `requirements.txt`)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/petko-todorov/con-stats.git
   cd con-stats
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env` file (if required). The `.env` file should contain your **username** and
   **password** for the game:
   ```env
   USERNAME=your_username
   PASSWORD=your_password
   ```
   **Important:** Do not share or commit your `.env` file to version control for security reasons.

## Usage

Run the main script to start scraping:

```sh
python main.py
```

## File Structure

- `main.py` - Entry point for the scraper
- `scraper.py` - Handles web scraping
- `info_from_web.py` - Retrieves additional data
- `visualizer.py` - Generates visualizations from the collected data
- `data_handler.py` - Processes and manages data
- `data/stats.csv` - Stores scraped data (if the folder is empty, it will be automatically created and populated with
  data upon first run)
- `chromedriver-win64/` - ChromeDriver for Selenium (can also be downloaded from the internet)
- `.env` - Stores login credentials (not to be shared)

