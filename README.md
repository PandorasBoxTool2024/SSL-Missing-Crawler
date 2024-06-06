# SSL Check Work 4.0

This Python script uses Selenium to navigate to a specified URL, scroll down the page, and collect information.

## Dependencies

- Python
- Selenium
- pandas
- time

## How to Run

1. Install the required Python packages with `pip install -r requirements.txt` (you need to create this file and list the dependencies there).
2. Run the script with `python SSL_Check_work_4.0.py`.

## Functions

- `scroll_down(driver)`: Scrolls down a page that the driver is currently on until it cannot scroll anymore.
- `open_url_and_accept_cookies(url)`: Opens a specified URL and navigates through the page.

## Configuration

You can adjust the maximum number of links to collect by changing the `link_limit` variable in the `open_url_and_accept_cookies` function.

## Note

The script is currently set to run in a visible browser mode. If you want to run it in headless mode, uncomment the line `options.add_argument('--headless')` in the `open_url_and_accept_cookies` function.
