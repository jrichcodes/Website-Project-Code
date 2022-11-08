from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time

def shopping(Foods): 

    #inital setup to connect to chrome and open website
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    #chrome_options.add_argument("--start-maximized");

    PATH = "C:\Downloads\chromedriver2.exe"
    driver = webdriver.Chrome(PATH, options=chrome_options)
    driver.get("https://www.target.com")
    driver.implicitly_wait(15)


    #typing in search bar for different foods
    item = "ham"
    search = driver.find_element(By.XPATH, "//*[@id='search']")
    search.send_keys(item)
    driver.find_element(By.CLASS_NAME, "styles__SearchButton-sc-srf2ow-7").click()
    driver.implicitly_wait(5)

    #choosing pick-up
    pick_up_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pageBodyContainer"]/div[1]/div/div[4]/div/div/div[1]/div/div/div/div[1]/button[1]')))
    pick_up_button.click()
    driver.implicitly_wait(3)

    #first item
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[data-test='orderPickupButton']"))).click()
    driver.implicitly_wait(3)
    driver.find_element(By.CSS_SELECTOR, 'button[aria-label="close"]').click()
    driver.implicitly_wait(3)

    for i in Foods:
        search = driver.find_element(By.XPATH, "//*[@id='search']")
        
        #clearing the search bar
        search.click()
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        
        #typing in food and searching
        search.send_keys(i)
        driver.find_element(By.CLASS_NAME, "styles__SearchButton-sc-srf2ow-7").click()
        time.sleep(5)
        
        #clicking on the first aviable item
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[data-test='orderPickupButton']"))).click()
        driver.implicitly_wait(3)
        driver.find_element(By.CSS_SELECTOR, 'button[aria-label="close"]').click()
        driver.implicitly_wait(3)

    time.sleep(10)
    driver.quit()

    #To Do: add in quanity funcitonality and chooses not sponsored products
    #notes for later use in case I get stuck again 
    #ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
    #item = WebDriverWait(driver, 10,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.CLASS_NAME, 'styles__ProductCardVariantDefaultWrapper-sc-bcz5ql-4 bUjSUe')))
    #item.click()
    #driver.find_element(By.CLASS_NAME,'styles__StyledProductCardBody-sc-bcz5ql-0').click()
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div[data-test="web/ProductCard/body"]'))).click()