# ------------IMPORTING MODULES/LIBRARIES
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
# -------------------------------------------

# INITIALIZING THE WEB DRIVER AS DRIVER
driver = webdriver.Chrome(executable_path='C:/WebDrivers/chromedriver.exe')
# MAXIMIZING THE WINDOW
driver.maximize_window()
# ---------------------------------------------------------------IGNORE THIS--------------------------------------------
# email = 'your Email'
# password = 'your Password'
# login_url = "https://www.amazon.com/ap/signin?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A
# %2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2
# .0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns
# .pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https
# %3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26action%3Dsign-out%26path%3D%252Fgp%252Fyourstore%
# 252Fhome%26ref_%3Dnav_AccountFlyout_signout%26signIn%3D1%26useRedirectOnSuccess%3D1    "
# driver.get(login_url)
# email_box = driver.find_element_by_id('ap_email').send_keys(email)
# button_0 = driver.find_element_by_id('continue').click()
# password_box = driver.find_element_by_id('ap_password').send_keys(password)
# button_1 = driver.find_element_by_id('signInSubmit').click()
#
# time.sleep(100)
# ---------------------------------------------------------------IGNORE THE UPPER CODE----------------------------------
# GETTING THE URL
Product_url = 'https://www.amazon.com/s?k=Laptop&ref=nb_sb_noss_2/'
driver.get(Product_url)
# WAIT FOR THE ELEMENTS TO BE LOADED
driver.implicitly_wait(10)

# THE THINGS WE WILL SCRAPE WILL BW STORED IN A LIST(TEMPORARY)
products_url_list = []
final_urls = []
title_list = []
price_list = []
image_url_list = []
review_list = []
description_list = []
QnA_list = []

# DOING THE MAIN STUFF(SCRAPING THE LINKS WE WANT)
# PUT IT IN THE TRY EXCEPT FOR HANDLING THE ERRORS
try:
    # SLEEPING SO ALL THE ELEMENTS WILL BE LOADED
    time.sleep(5)
    # SCROLLING TO THE END OF THE PAGE
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # GETTING THE SOURCE CODE
    src = driver.page_source
    # PARSING IT WITH LXML
    soup = bs(src, 'lxml')
    # FINDING ALL THE URLS ON THE PAGE OF THE PRODUCTS TO BE SCRAPE
    products_url = soup.find_all('a', class_='a-link-normal a-text-normal')
    # GETTING THE EXACT LINK TO THE PRODUCT PAGE
    for product_link in products_url:
        link = product_link.get('href')
        products_url_list.append(link)

except:
    driver.quit()
    print('Unable to scrape links')

# YOU CAN IGNORE IF YOU DIDN'T UNDERSTAND THIS(NOT NECESSARY)
print(len(products_url_list))
for url in products_url_list:
    final_urls.append('https://www.amazon.com/' + url)
print(len(final_urls))

# DOING THE MAIN STUFF(SCRAPING THE THINGS WE WE WANT)
# AGAIN TRY EXCEPT FOR ERROR HANDLING
try:
    # PUTTING IT IN WHILE LOOP SO WE CAN SCRAPE ALL THE THINGS UNTIL NOTHING IS REMAINING TO BE SCRAPED
    while True:
        # ITERATING OVER THE LINK TO PRODUCT PAGE AND SCRAPING THE NECESSARY STUFF
        for link in final_urls:
            driver.get(link)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            product_src = driver.page_source
            page_soup = bs(product_src, 'lxml')
            title = page_soup.find('h1', id='title')
            title_text = title.text
            title_list.append(title_text.strip())
            print(title_list)
            price = page_soup.find('span', id='priceblock_ourprice')
            price_text = price.text
            price_list.append(price_text)
            print(price_list)
            img_url = page_soup.find('img', id='landingImage')
            url = img_url.get('src')
            image_url_list.append(url)
            print(image_url_list)
            review = page_soup.find('span', class_='a-icon-alt')
            review_text = review.text
            review_list.append(review_text)
            print(review_list)
            description = page_soup.find('div', id='productDescription')
            description_text = description.text
            description_list.append(description_text.strip())
            print(description_list)
            # STORING ALL THE DATA IN A CSV FILE USING PANDAS DATAFRAME
            data = {'Title': title_list,
                    'Price': price_list,
                    'Review': review_list,
                    'IMG_URL': image_url_list,
                    'Description': description_list}
            df = pd.DataFrame(data)
            df.to_csv('Products_Data.csv')
except:
    driver.quit()
    print('error')
# THAT'S ALL YOU HAVE SAW A CODE THAT CAN SCRAPE ALL THE REQUIRED THINGS TO BE SCRAPED OF A PRODUCT ON AMAZON-----------
