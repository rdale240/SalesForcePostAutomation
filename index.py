from selenium import webdriver
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv
import os
import mysql.connector
import time


##REMAINING WORK:
    #Get/Set last IDs to ENV from DB
    #Add Program from DB to Program Drop Down - Finish adding <Select> <option> values
    #Select Submit Button / Send Click()


#Implement .env to protect database information
load_dotenv()



#load database information
HOST=os.getenv("HOST")
USER=os.getenv("USER")
PASS=os.getenv("PASS")
DB=os.getenv("DB")
PORT=os.getenv("PORT")
print(HOST,USER,PASS,PORT)

#respective databases
databases=["acctax","analytics","business","finance","gemba","hemba","intlbusiness","leadership","mba","mha","promba","sustainable"]

#Hashtable for Program Dropdown Values
programDropdown = {"MBA - Executive MBA in Health Sector Mgt. and Policy":"a0I1500000HSVMDEA5",
    "MBA - Global Executive MBA":"a0I1500000HSVMCEA5",
    "MBA - Global One":"a0I1C00000JcIB0UAN",
    "MBA - Professional MBA":"a0I1500000HSVMHEA5",
}

print(programDropdown["MBA - Professional MBA"])
time.sleep(5)
#connect to mySQL server to acquire data to post to salesforce
cnx = mysql.connector.connect(user=USER, password=PASS,
                              host=HOST,
                              database='umiami')

print(cnx)
#location of chromedriver.exe
chromedriverLocation = os.getenv(CHROMEDRIVERPATH)
#Open Chrome
driver = webdriver.Chrome(chromedriverLocation)

#Automating Flow
#Enter Every Database
for database in databases:
    #switch to choose corresponding salesforce URL
    if (database=="leadership") or (database=="finance") or (database=="form") or (database=="intlbusiness") or (database=="analytics") or (database=="mha"):
        url="http://go.miami.edu/specialized-masters"
    elif (database=="gemba"):
        url="http://go.miami.edu/ex-mba-americas"
    elif (database=="hemba"):
        url="http://go.miami.edu/ex-mba-health-sector"
    elif (database=="promba"):
        url="http://go.miami.edu/professional-mba"
    elif (database=="business") or (database=="mba"):
        url="http://go.miami.edu/full-time-mba"
    else:
        url="http://go.miami.edu/specialized-masters"
    #Open mySQL Cursor
    cursor=cnx.cursor()    
    #SQL Query
    query=("SELECT id, first_name, last_name, email, phone, utm_source, utm_medium, utm_campaign, program FROM "+database + " where ID > 600" ) # where ID > some ID related to DB
    #Execute SQL Query
    cursor.execute(query)
    #For all data returned from Query, execute Automation
    for(id,first_name,last_name,email,phone,utm_source,utm_medium,utm_campaign, program) in cursor:
        print(id,first_name,last_name,email,phone,utm_source,utm_medium,utm_campaign, program)
        #Go to Salesforce URL
        if(utm_source==None):
            utm_source=""
        if(utm_medium==None):
            utm_medium=""
        if(utm_campaign==None):
            utm_campaign=""
        driver.get(url+'/?utm_source='+utm_source+'&utm_medium='+utm_medium+'&utm_campaign='+utm_campaign) #URL must be custom for source
        ##########################

        #First Name Input
        fNameInput=driver.find_element_by_name('First_Name__c')
        first_name=''.join(e for e in first_name if e.isalnum())
        fNameInput.send_keys(first_name)

        #Last Name Input
        lNameInput=driver.find_element_by_name('Last_Name__c')
        last_name=''.join(e for e in last_name if e.isalnum())
        lNameInput.send_keys(last_name)
        #####################################

        #Email Input
        emailInput=driver.find_element_by_name('Email__c')
        emailInput.send_keys(email)
        #####################################

        #Phone Input
        phoneInput=driver.find_element_by_name('Home_Phone__c')
        phone=str(phone).replace("+","")
        phoneInput.send_keys(phone)
        ######################################
        time.sleep(3)
    #Close Cursor
    cursor.close()
#Close mySQL Connection after cycling through all DBs
cnx.close()
#################################################

#End of Program

# #Sample Data
# firstName='Hello World'
# firstName=''.join(e for e in firstName if e.isalnum())
# lastName='Dale%$#@'
# lastName=''.join(e for e in lastName if e.isalnum())
# email="someone@miami.edu"
# phone='5555555555' #no plus but can have parentheses
# country = "Malawi" #Must have first letter uppercase
# ################################






#Country Input (Not important)
#Useful for Program Dropdown
# countryInput=driver.find_element_by_name("Mailing_Country__c")
# countryInputSelector = Select(countryInput)
# countryInputSelector.select_by_value(country)
######################################

#driver.get('http://go.miami.edu/specialized-masters')


