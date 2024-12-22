from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.parse
import pandas as pd


chrome_options = webdriver.ChromeOptions()

#to avoid bot
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")

#For  Maximizing window
chrome_options.add_argument("--start-maximized")


driver = webdriver.Chrome(options=chrome_options)

# 10 bestseller
categories = [
    "Electronics",
"Fashion",
    "Home",
    "Books",
    "Beauty",
    "Sports",
    "Toys",
    "Grocery",
    "Automotive",
    "Health",
    "Pet Supplies"
]


all_products = []


for category in categories:
    # Properly encode the category
    encoded_category = urllib.parse.quote_plus(category)

    # Amazon url for particular category
    driver.get(
        f"https://www.amazon.in/s?k={encoded_category}&crid=Q0L6IWFI4HSJ&sprefix={encoded_category}%2Caps%2C231&ref=nb_sb_noss_2")


    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="p_n_pct-off-with-tax/2665401031"]/span/a'))
    )
    #to select 50% and more than 50% discount filter(radio button)
    discount = driver.find_element(By.XPATH, '//*[@id="p_n_pct-off-with-tax/2665401031"]/span/a')
    discount.click()
    time.sleep(5)

    # Product name
    h2_elements = driver.find_elements(By.XPATH, '//h2[@aria-label]')
    time.sleep(5)

    # Price
    price_elements = driver.find_elements(By.CLASS_NAME, 'a-price-whole')


    index = 0


    for h2 in h2_elements:
        try:

            product_name = h2.text
        except:
            product_name = "N/A"

        try:

            product_price = price_elements[index].text
        except:
            product_price = "N/A"

    product_data = {
            'Category': category,
            'Product Name': product_name,
            'Product Price': product_price,

        }


        all_products.append(product_data)


        index += 1


df = pd.DataFrame(all_products)


df.to_excel("amazon_product_data_with_category_and_rating.xlsx", index=False)
print("Succefully Scrapped data from 10 categories with more than 50% dicount and Prsented in EXcel sheet/Format")
# Close the browser
driver.quit()
