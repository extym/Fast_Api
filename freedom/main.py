from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pqdm
#'https://finlandvisa.fi/register'  #



url = 'https://github.com/'
service = Service(executable_path='/usr/local/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  #for open window chrome
browser = webdriver.Chrome(service=service, options=options)
browser.get(url)