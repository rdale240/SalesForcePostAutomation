from selenium import webdriver
from selenium.webdriver.support.ui import Select

#Sample Data
chromedriverLocation = 'C:\\Users\\Richard\\chromedriver.exe'
firstName='Hello World'
firstName=''.join(e for e in firstName if e.isalnum())
lastName='Dale%$#@'
lastName=''.join(e for e in lastName if e.isalnum())
email="someone@miami.edu"
phone='5555555555' #no plus but can have parentheses
country = "Malawi" #Must have first letter uppercase
################################

#Open Chrome
driver = webdriver.Chrome(chromedriverLocation)
driver.get('http://go.miami.edu/specialized-masters') #URL must be custom for source
##########################

#First Name Input
fNameInput=driver.find_element_by_name('First_Name__c')
fNameInput.send_keys(firstName)

#Last Name Input
lNameInput=driver.find_element_by_name('Last_Name__c')
lNameInput.send_keys(lastName)
#####################################

#Email Input
emailInput=driver.find_element_by_name('Email__c')
emailInput.send_keys(email)
#####################################

#Phone Input
phoneInput=driver.find_element_by_name('Home_Phone__c')
phoneInput.send_keys(phone)
######################################

#Country Input (Not important)
#Useful for Program Dropdown
countryInput=driver.find_element_by_name("Mailing_Country__c")
countryInputSelector = Select(countryInput)
countryInputSelector.select_by_value(country)
######################################



