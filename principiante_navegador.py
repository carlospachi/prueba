import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ejemplo(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Edge(executable_path=r"D://Carlos//phyton//empezando//binance//msedgedriver.exe")
	
		

	def test_usando_explicit(self):
		driver = self.driver 
		driver.get("http://www.hispashare.club/")
		
		
		try:
		    element = WebDriverWait(driver, 10).until(
		        EC.presence_of_element_located((By.NAME, "order"))
		        )
		    print("Que bien trabajamos")
		except Exception as e:
			print("Cagadilla, ",e)
		#driver.close()
		
	def tearDown(self):
		driver = self.driver
		driver.close()	
			


if __name__=="__main__":
	unittest.main()





