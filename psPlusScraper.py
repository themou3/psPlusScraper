from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
import time
import csv

def cookie_consent(driver):
    try:
        cookie_accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="_evidon-accept-button"]')))
        cookie_accept_button.click()
        time.sleep(1)
        del(cookie_accept_button)
    except Exception as e:
        print("Cookie banner not found or could not be clicked:", e)

def create_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f'products_{timestamp}.csv'

def create_csv_writer(filename):
    fieldnames = ['Product Name', 'Link', 'Type']
    csvfile = open(filename, mode='w', newline='', encoding='utf-8')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    return writer, csvfile


def main():
    # Initialisation
    page = 0
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.get("https://store.playstation.com/en-us/category/30e3fe35-8f2d-4496-95bc-844f56952e3c/")
    elements_xpath = '//span[@class="psw-truncate-text-1 psw-c-t-ps-plus" and (contains(text(), "Premium") or contains(text(), "Extra"))]' 
    next_button_xpath = '//button[@data-qa="ems-sdk-grid#ems-sdk-top-paginator-root#next"]' 

    # Cookie consent
    cookie_consent(driver)

    #File creation
    filename = create_filename()
    csv_writer, csvfile = create_csv_writer(filename)

    while True:

        page += 1
        print(page)

        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, elements_xpath)))
            WebDriverWait(driver, 4).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            elements = driver.find_elements(By.XPATH, elements_xpath)
        except Exception:
            print("There is no games.")
            elements = 0
        
        if elements:
            for element in elements:
                try:
                    link_element = element.find_element(By.XPATH, './/ancestor::a')  # find tag <a>
                    link = link_element.get_attribute("href")  # find href

                    product_name_element = link_element.find_element(By.XPATH, './div/section/span') # find Product Name
                    product_name = product_name_element.text if product_name_element else "Unknown Product"

                    product_type_element = link_element.find_element(By.XPATH, './div/section/div[1]/div/span') # find Type
                    product_type = product_type_element.text
                    print(f"Found link: {link} | Product Name: {product_name} | Type: {product_type}")

                    csv_writer.writerow({'Link': link, 'Product Name': product_name, 'Type': product_type}) # write it down
                    
                    # Part of code for clicking can't be done because of https://bugzilla.mozilla.org/show_bug.cgi?id=1638673
                    # User must be logged in and this cannot be done with Selenium
                    # Same with chromium-based browsers 

                except Exception as e:
                    print("Link not found or could not be accessed:", e)
                    continue

        # Go next page
        try:
            del(elements)
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, next_button_xpath)))
            next_button = driver.find_element(By.XPATH, next_button_xpath)
            
            if next_button.get_attribute("disabled") is not None:
                print("No more pages to explore")
                break # Quit if no more pages
            else:
                print("The button is active. Proceeding to click.")
                next_button.click()
        except Exception:
            print("Uknnown eror")
            break
    
    csvfile.close()
    driver.quit()

if __name__ == "__main__":
    main()
