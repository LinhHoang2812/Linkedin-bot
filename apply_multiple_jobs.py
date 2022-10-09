import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
EMAIL = os.environ["EMAIL"]
PASS_WORD = os.environ["PASS"]

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
driver.get("https://www.linkedin.com/my-items/saved-jobs/")

cookies = driver.find_element(By.XPATH,'//*[@id="artdeco-global-alert-container"]/div/section/div/div[2]/button[1]')
cookies.click()



signin_textlink = driver.find_element(By.LINK_TEXT,"Sign in")
signin_textlink.click()

email = driver.find_element(By.ID,"username")
email.send_keys(EMAIL)

password = driver.find_element(By.ID,"password")
password.send_keys(PASS_WORD)

signin_butt = driver.find_element(By.CLASS_NAME,"from__button--floating")
signin_butt.click()


time.sleep(5)

all_jobs = driver.find_elements(By.CSS_SELECTOR,".t-16 a")

for job in all_jobs:
    #get link to the job
    second_tab_link = job.get_attribute("href")

    #open job in second tab
    driver.execute_script("window.open('about:blank','secondtab');")
    driver.switch_to.window("secondtab")
    driver.get(second_tab_link)
    time.sleep(2)

    #if the job still available for apply
    try:
        jobs_apply_button = driver.find_element(By.CSS_SELECTOR, '.jobs-apply-button--top-card button')
        jobs_apply_button.click()

        phone = driver.find_element(By.CSS_SELECTOR, ".display-flex input")
        if phone.text == "":
            phone.send_keys("3887247409")

        submit = driver.find_element(By.CSS_SELECTOR,".pv4 button")
        if submit.text == "Submit application":
            submit.click()
            print("successfully applied")
            x = driver.find_element(By.CSS_SELECTOR,".artdeco-modal artdeco-modal--layer-default  button")
            x.click()

        else:
            x = driver.find_element(By.CSS_SELECTOR, ".jobs-easy-apply-modal button")
            x.click()
            time.sleep(2)

            discard = driver.find_elements(By.CSS_SELECTOR, ".artdeco-modal__actionbar button")[0]
            discard.click()

            print("complicated job application. Skip")




    # job is not anymore available
    except NoSuchElementException:
        print("job no longer accepts application")
    finally:
        time.sleep(5)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])







