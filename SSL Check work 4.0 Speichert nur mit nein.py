import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust sleep time as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print("Finished scrolling")

def open_url_and_accept_cookies(url):
    options = Options()
    # options.add_argument('--headless')  # Uncomment this line if you want to run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    link_limit = 1000  # Maximum number of links to collect
    link_count = 0  # Initialize link counter
    link_data = []  # List to store links and SSL status

    try:
        driver.get(url)
        print("Navigated to URL")

        # Wait for the cookie consent button to appear and click it
        try:
            consent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="L2AGLb"]'))
            )
            consent_button.click()
            print("Clicked 'Accept All' button for cookies")
        except Exception as e:
            print("Cookie consent button not found or clickable: ", e)
        
        # Scroll down the page initially
        scroll_down(driver)

        while link_count < link_limit:
            # Find and click the "Pfeil nach oben" button if exists
            try:
                arrow_up_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.kQdGHd span.OTvAmd.z1asCe.QFl0Ff'))
                )
                arrow_up_button.click()
                print("Clicked 'Pfeil nach oben' button")
            except Exception as e:
                print("Could not find or click 'Pfeil nach oben' button: ", e)
                break
            
            # Scroll down again to load more content
            scroll_down(driver)

            # Find all links on the page
            links = driver.find_elements(By.TAG_NAME, 'a')

            for link in links:
                href = link.get_attribute('href')
                if href and not href.startswith('https://'):
                    link_count += 1
                    if link_count > link_limit:
                        break
                    link_data.append((href, "No"))  # Mark SSL status as "No"
                    print(f"Collected link {link_count}: {href}")

            if link_count > link_limit:
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

        # Create a DataFrame from link_data
        df = pd.DataFrame(link_data, columns=['Link', 'SSL'])

        # Write DataFrame to Excel
        excel_filename = 'links_without_ssl_status Nagelstudio.xlsx'
        df.to_excel(excel_filename, index=False)
        print(f"Data has been written to {excel_filename}")

if __name__ == "__main__":
    url = input("URL Pleas ")
    open_url_and_accept_cookies(url)
