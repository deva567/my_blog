# from selenium import webdriver


# driver=webdriver.Chrome()
# driver.get('https://kite.trade/connect/login?api_key=knezpu1290s0fgkn&v=3')



from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
# options = Options()
# options.headless = True
# options.add_argument("--window-size=1920,1200")
path=r"C:\Users\venna\AppData\Local\Programs\Python\Python38-32\Scripts\chromedriver.exe"

driver = webdriver.Chrome(executable_path=path)
driver.implicitly_wait(30)
driver.maximize_window()

driver.get("https://kite.trade/connect/login?api_key=knezpu1290s0fgkn&v=3")

username=driver.find_element_by_xpath("//*[@id='userid']")
username.clear()
username.send_keys('AO7882')



pwd=driver.find_element_by_xpath("//input[@id='password']")
pwd.clear()
pwd.send_keys('Vd@4vennam')

submit=driver.find_element_by_xpath("//button[@type='submit']").click()

pin=driver.find_element_by_xpath("//input[@id='pin']")
pin.clear()
pin.send_keys('481996')

submit1=driver.find_element_by_xpath("//button[@type='submit']").click()

time.sleep(30)
driver.close()


