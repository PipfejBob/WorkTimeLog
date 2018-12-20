# letölt: selenium
# letölt: geckodriver for chrome -> http://chromedriver.chromium.org/downloads

import time, getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def up(Work):
	# proxy beállítás kell-e?
	
	# böngésző megnyitása
	browser = webdriver.Chrome()
	# munkanapló bejelentkezős oldal:
	browser.get('http://192.168.1.64:8080/')

	# username kitöltése
	browser.find_element_by_name('username').send_keys("pipfejbob")

	# password kitöltése
	pw = getpass.getpass()
	browser.find_element_by_name('password').send_keys(pw)

	# bejelentkezés nyomógomb megkeresése, klikk rá
	browser.find_element_by_name('login').click()

	# munkafelvételi lap megnyitása (a projekt id alapján!)
	wp = '' + Work.Diszpo_ID
	browser.get(wp)

	# mezők kitöltése:
	# - munkaidő kezdete: str(Work.Time_Start)
	# - munkaidő vége: str(Work.Time_WorkStop)
	# - munkaleírás: Work.Work_On + ': ' + Work.Work_Desc

	time.sleep(10) # sleep for 5 seconds so you can see the results
	browser.quit()