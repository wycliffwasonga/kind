import subprocess
from sys import platform
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.firefox import GeckoDriverManager

if platform == "win32":
    import win32com.client as comclt

KIND_URL = "https://kind.krx.co.kr/disclosure/details.do?method=searchDetailsMain#viewer"
COMPANY_INPUT_SELECTOR = "form#searchForm .search-group .form-search .company input#AKCKwd"
FROM_DATE_INPUT_SELECTOR = "form#searchForm .search-group .form-search input#fromDate"
TO_DATE_INPUT_SELECTOR = ".form-search input#toDate"
SEARCH_BUTTON_SELECTOR = "form#searchForm .search-group a.search-btn"
SEARCH_RESULT_ROW_SELECTOR = "article#main-contents section.scrarea table.list tbody tr"

DATE_INPUT_FORMAT = "%Y%m%d"

def show_only_frame(driver, frame):
    driver.switch_to.frame(frame)
    
    time.sleep(2)
    
    body = WebDriverWait(driver, 30).until(lambda d: d.find_element(By.CSS_SELECTOR, "body"))
    
    ActionChains(driver).context_click(body).perform()
    
    time.sleep(1)
    
    if platform == "darwin":
        cmd = '''
        tell application "System Events"
          repeat 3 times
            key code 126
          end repeat
          key code 124
          keystroke return
        end tell
        '''
        p = subprocess.run(['osascript', '-e', cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        #print(p.stderr.decode('utf-8'))
        #print(p.stdout.decode('utf-8'))
    elif platform == "win32":
        wsh = comclt.Dispatch("WScript.Shell")
        
        wsh.SendKeys("{UP}")
        wsh.SendKeys("{UP}")
        wsh.SendKeys("{UP}")
        wsh.SendKeys("{RIGHT}")
        wsh.SendKeys("{ENTER}")

def search(company_symbol, start_date, end_date):
    if platform == "linux" or platform == "linux2":
        raise Exception("Linux is not currently supported")
        
    options = Options()
    options.headless = True
    
    search_results = []
    
    try:
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
        driver.get(KIND_URL)
        
        actionChains = ActionChains(driver)
        wait = WebDriverWait(driver, 30)
        main_window = driver.current_window_handle
        
        company_input   = wait.until(lambda d: d.find_element(By.CSS_SELECTOR, COMPANY_INPUT_SELECTOR))
        from_date_input = wait.until(lambda d: d.find_element(By.CSS_SELECTOR, FROM_DATE_INPUT_SELECTOR))
        to_date_input   = wait.until(lambda d: d.find_element(By.CSS_SELECTOR, TO_DATE_INPUT_SELECTOR))
        search_button   = wait.until(lambda d: d.find_element(By.CSS_SELECTOR, SEARCH_BUTTON_SELECTOR))

        company_input.clear()
        company_input.send_keys(company_symbol)
        from_date_input.clear()
        from_date_input.send_keys(start_date.strftime(DATE_INPUT_FORMAT))
        to_date_input.clear()
        to_date_input.send_keys(end_date.strftime(DATE_INPUT_FORMAT))

        driver.execute_script("arguments[0].click()", search_button)
        
        time.sleep(3)
        
        search_result_rows = wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, SEARCH_RESULT_ROW_SELECTOR))

        i = 1
        while i < len(search_result_rows):
            date_cell = WebDriverWait(driver, 30).until(lambda d: d.find_element(By.CSS_SELECTOR, f"article#main-contents section.scrarea table.list tbody tr:nth-child({i}) td:nth-child(2)"))
            link = WebDriverWait(driver, 30).until(lambda d: d.find_element(By.CSS_SELECTOR, f"article#main-contents section.scrarea table.list tbody tr:nth-child({i}) td:nth-child(4) a"))
            
            search_result = {
                "date": date_cell.text,
                "title": link.text
                }
            
            driver.execute_script("arguments[0].click()", link)

            wait.until(EC.number_of_windows_to_be(2))
            driver.switch_to.window(driver.window_handles[1])
            
            doc_view_frame = wait.until(lambda d: d.find_element(By.CSS_SELECTOR, "iframe#docViewFrm"))
            
            show_only_frame(driver, doc_view_frame)
            
            search_result["url"] = driver.execute_script("return window.document.URL")
            
            driver.close()
            wait.until(EC.number_of_windows_to_be(1))

            driver.switch_to.window(main_window)
            
            i = i + 1
                
            search_results.append(search_result)
    except:
        raise Exception("Error occurred while getting the search results")
    finally:
        if driver != None:
            driver.quit()
    
    return search_results
