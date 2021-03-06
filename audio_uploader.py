#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

course_name = 'Harry Potter Chamber of Secrets Words'

input_file = "words.txt"
# Full path to your audio directory
audio_path = ''
# Your memrise id and password
memrise_id = ""
memrise_password = ""
# Memrise login page
login_url = "https://www.memrise.com/login/"


# Read words from given file
with open(input_file,"r") as f:
    words = f.read().splitlines()

# Load driver
driver = webdriver.Chrome('./web_drivers/chromedriver')

# Login
driver.get(login_url)
elem = driver.find_element_by_name('username')
elem.send_keys(memrise_id)
elem = driver.find_element_by_name('password')
elem.send_keys(memrise_password)
elem.send_keys(Keys.RETURN)

# Select course
elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, course_name))
    )
elem = driver.find_element_by_link_text(course_name)
elem.click()

# Go to edit course page
elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Edit Course'))
    )
elem = driver.find_element_by_link_text('Edit Course')
elem.click()

try:
	for word in words:
		elem = WebDriverWait(driver, 10).until(
		        EC.presence_of_element_located((By.XPATH, "//div[text()=\"" + word + "\"]"))
		    )

		elem = driver.find_element_by_xpath("//div[text()=\"" + word + "\"]")
		parent = elem.find_element_by_xpath("..")
		parent = parent.find_element_by_xpath("..")
		parent_tr = parent.find_element_by_xpath("..")
		upload_element = parent_tr.find_element_by_name('f')

		upload_element.send_keys(audio_path + word + '.mp3')
		print('[INFO] Uploaded audio file for the word {}'.format(word))
	print('[INFO] Uploaded all audio files')
except Exception as e:
	raise e

# driver.quit()
