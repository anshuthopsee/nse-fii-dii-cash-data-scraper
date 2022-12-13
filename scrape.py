from selenium import webdriver
from datetime import date, datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

PATH = "C:\\Program Files (x86)\\chromedriver.exe"
service = Service(PATH)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

def get_data():
    driver = None
    elements = None
    values_list = []
    data_keys = ["dii_cash_buy", "dii_cash_sell", "dii_cash_net", "fii_cash_buy", "fii_cash_sell", "fii_cash_net"]
    data = {}
 
    #Keeps trying until the webpage displays the data correctly.
    def recursive_func():
        nonlocal driver
        
        #Closes the previous instance of the driver, when the function gets called recursively.
        if driver:
            driver.quit()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://www.nseindia.com/reports/fii-dii")

        def find_elements(driver):
            nonlocal elements
            elements = driver.find_elements(By.TAG_NAME, "td")
            
            #If number of elements is > 1, that means data is available, hence returns True. Or returns False, if not the case.
            if len(elements) > 1:
                return True
            else:
                return False

        wait = WebDriverWait(driver, 3)
        try:
            wait.until(find_elements)
            
        #Execption is raised, when data is not shown on the page, so a retry is required.
        except:
            recursive_func()

    recursive_func()

    for item in elements:
        value = item.text.replace(",", "")
        values_list.append(value)

    date_displayed = values_list[1]
    date_today = date.today().strftime("%d-%b-%Y")

    #Checks if today's date and the date of available data are the same
    if date_today == date_displayed:
        
        #Removes data lables
        for i in [0, 0, 3, 3]:
            values_list.pop(i)

        for i in range(0, len(values_list)):
            data[data_keys[i]] = float(values_list[i])
        
        driver.quit()
        return data

    else:
        driver.quit()
        print(f"Data for {date_today} is not yet available. Try again later.")

data = get_data()
