from anticaptchaofficial.recaptchav2proxyless import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import os


driver = webdriver.Chrome(ChromeDriverManager().install())

url = "https://www.google.com/recaptcha/api2/demo"
page = driver.get(url)

time.sleep(10)

sitekey = driver.find_element(By.XPATH, '//*[@id="recaptcha-demo"]').get_attribute('outerHTML')
sitekey_clean = sitekey.split('" data-callback')[0].split('data-sitekey="')[1]
print(sitekey_clean)

solver = recaptchaV2Proxyless()
solver.set_verbose(1)
solver.set_key(os.environ["anticaptcha_api_key"])
solver.set_website_url(url)
solver.set_website_key(sitekey_clean)

g_response = solver.solve_and_return_solution()
if g_response!= 0:
    print("g_response"+g_response)
else:
    print("task finished with error"+solver.error_code)

driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')

driver.execute_script("""document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", g_response)
driver.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')

driver.find_element(By.XPATH, '//*[@id="recaptcha-demo-submit"]').click()

time.sleep(20)