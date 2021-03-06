from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import datetime
import os
import mysql.connector
import time

##ASSUMPTIONS
    #Program of Interest is determined by mySQL Table/Certain Business Rules
    #Country is unimportant to SalesForce

##LEGACY WORK:
    #Get/Set last IDs to ENV from DB
        #UPDATE 2/7/19 - Server is Created, software needs to be installed on the virtual machine.
        #COMPLETE - Transitioned to timestamps to determine entries
    #Add Program from DB to Program Drop Down - Finish adding <Select> <option> values
        #UPDATE 2/7/19 - Program is determined by mySQL Table
        #UPDATE 2/8/19 - May informed to not access Business table because those links are forwarded to Business Director/ Online goes to online options
        #COMPLETE
    #Select Submit Button / Send Click()
        #COMPLETE


##REMAINING WORK:
    #COPY DATABASE ENTRIES IN CASE SYSTEM GOES DOWN
    #WRITE TRANSACTIONAL DATA TO SFPATEST DATABASE
        #COMPLETE
    #WAIT FOR CSS CHANGE WHEN ITEM IS SUBMITTED
        #UPDATE 2/28/19 Testing with MAY
            #NOTES:Send UOnline data to alternate table for storage
    #Criteria for Bad Lead:
        #Less than 10 digits in phone number
        #Last entry is identical


#Initialize Performance Data Records
numSubmissions = 0
f = open('record.txt', 'a')
start_time = time.time()
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(now,f)


#Implement .env to protect database information
load_dotenv()



#load database information
HOST=os.getenv("HOST")
USER=os.getenv("USER")
PASS=os.getenv("PASS")
DB=os.getenv("DB")
PORT=os.getenv("PORT")
STATEHOST=os.getenv("STATEHOST")
STATEUSER=os.getenv("STATEUSER")
STATEPASS=os.getenv("STATEPASS")
STATEPORT=os.getenv("STATEPORT")
#location of chromedriver.exe
chromedriverLocation = os.getenv("CHROMEDRIVERPATH")

#respective databases
databases=["finance","analytics","acctax","hemba","intlbusiness","leadership","mba","mha","promba","sustainable"]
    #business not entered to salesforce
    #removed "gemba" for testing purposes (phone is not a valid field)

#Hashtable for Program Dropdown Values
programDropdown = {"MBA - Executive MBA in Health Sector Mgt. and Policy":"a0I1500000HSVMDEA5",
    "MBA - Global Executive MBA":"a0I1500000HSVMCEA5", #Mapped
    "MBA - Global One":"a0I1C00000JcIB0UAN",
    "MBA - Professional MBA":"a0I1500000HSVMHEA5",#Mapped
    "MD/MBA - Medical Doctorate/Master in Business Administration":"a0I1500000HSVMNEA5",
    "MBA - Two-Year MBA":"a0I1500000HSVMEEA5",
    "MBA - One-Year MBA":"a0I1500000HSVMGEA5",
    "MBA - Accelerated MBA in Real Estate":"a0I1500000HSVMBEA5",
    "JD/MBA/LLM - JD/MBA/Master in Taxation":"a0I1500000HSVPKEA5",
    "JD/MBA/LLM - JD/MBA/Master in Real Property Development":"a0I1500000HSVPJEA5",
    "JD/MBA - Juris Doctorate/Master in Business Administration":"a0I1500000HSVMUEA5",
    "BARCH/MBA - Bachelor in Architecture/Master in Business Administration":"a0I1500000HSVM7EAP",
    "MS - Taxation":"a0I1500000HSVMMEA5", #Mapped
    "MS - Sustainable Business":"a0I1C00000JcIAvUAN", #Mapped
    "MS - Leadership":"a0I1500000HSVMLEA5", #Mapped
    "MS - International Business":"a0I1500000HSVMKEA5", #Mapped
    "MS - Finance":"a0I1500000HSVMJEA5",
    "MS - Business Analytics":"a0I1500000HSVMIEA5", #Mapped
    "MHA - Master in Health Administration":"a0I1500000HO3ZpEAL",
    "MACC/MST - Master in Accounting/Master in Tax":"a0I1500000HSVMVEA5",
    "MACC - Accounting":"a0I1500000HSVMAEA5",#Mapped
    "Certificate - Leadership":"a0I1500000HSVMOEA5",
}

programFromDB= {
    "intlbusiness":"MS - International Business",
    "hemba":"MBA - Executive MBA in Health Sector Mgt. and Policy",
    "gemba":"MBA - Global Executive MBA",
    "finance":"MS - Finance",
    "analytics":"MS - Business Analytics",
    "acctax":"decide",
    "sustainable": "MS - Sustainable Business",
    "promba":"MBA - Professional MBA",
    "mha":"MHA - Master in Health Administration",
    "mba":"MBA - Two-Year MBA",
    "leadership":"MS - Leadership"
}


#connect to mySQL server to update transactions
transCnx = mysql.connector.connect(user=STATEUSER, password=STATEPASS,
                              host=STATEHOST,
                              database='sfpatest',
                              )


#connect to mySQL server to acquire state
stateCnx = mysql.connector.connect(user=STATEUSER, password=STATEPASS,
                              host=STATEHOST,
                              database='sfpatest',
                              )

#connect to mySQL server to acquire data to post to salesforce
cnx = mysql.connector.connect(user=USER, password=PASS,
                              host=HOST,
                              database='umiami')

#Read State Database
stateCursor=stateCnx.cursor() 
stateQuery=("SELECT timestamp FROM state WHERE id=1")
#Execute SQL Query
stateCursor.execute(stateQuery)
for (timestamp) in stateCursor:
    print("time from db",timestamp[0])
    queryTime=timestamp[0].strftime("%Y-%m-%d %H:%M:%S")
stateCursor.close()
#*************************************

#Update State Database
stateUpdateCursor=stateCnx.cursor() 
stateUpdate=("UPDATE state SET timestamp="+ '"'+now+'" where ID=1')
#Execute SQL Query
#stateUpdateCursor.execute(stateUpdate)
#stateCnx.commit()
#************************************

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
    #query=("SELECT id, first_name, last_name, email, phone, utm_source, utm_medium, utm_campaign, program FROM "+database + " WHERE ID > 605 AND ID < 700" ) # where ID > some ID related to DB
    query=("SELECT id, first_name, last_name, email, phone, time_of_submission, utm_source, utm_medium, utm_campaign, program FROM "+database + " WHERE DATE(time_of_submission) > "+ 'DATE("'+queryTime+'")' + " AND TIME(time_of_submission) > "+'TIME("'+ queryTime+'")' )
    print(query)
    #Execute SQL Query
    cursor.execute(query)
    #For all data returned from Query, execute Automation
    for(id,first_name,last_name,email,phone, time_of_submission, utm_source,utm_medium,utm_campaign, program) in cursor:
        print(database, id,first_name,last_name,email,phone,utm_source,utm_medium,utm_campaign, program)
        if (program == "Online Master in Professional Accounting"):
            {
                #Do Nothing
                #load to send to UOnline
            }
        else:
            #Go to Salesforce URL
            if(utm_source==None):
                utm_source=""
            if(utm_medium==None):
                utm_medium=""
            if(utm_campaign==None):
                utm_campaign=""
            driver.get(url+'?utm_source='+utm_source+'&utm_medium='+utm_medium+'&utm_campaign='+utm_campaign) #URL must be custom for source
            ##########################

            #"More Information" Click
            moreInformation=driver.find_element_by_name("event-selection")
            moreInformation.click()

            #Program Input
            programInput=driver.find_element_by_name("Recruitment_Plan__c")
            programInputSelector = Select(programInput)
            #Based on Business Rules
            if (database == "acctax"):
                if (program == "Master in Accounting"):
                    programOptionTag = "MACC - Accounting"
                elif (program == "Master in Taxation"):
                    programOptionTag = "MS - Taxation"
                elif (program == "Undecided"):
                    programOptionTag = "MACC/MST - Master in Accounting/Master in Tax"
                programOption=programDropdown[programOptionTag]
            else:
                programOption = programDropdown[programFromDB[database]]
            #################
            programInputSelector.select_by_value(programOption) 
            #########################################

            #First Name Input
            fNameInput=driver.find_element_by_name('First_Name__c')
            first_name=''.join(e for e in first_name if e.isalnum())
            fNameInput.send_keys(first_name)

            #Last Name Input
            lNameInput=driver.find_element_by_name('Last_Name__c')
            last_name=''.join(e for e in last_name if e.isalnum())
            lNameInput.send_keys("xxServerTest" + last_name)
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

            time.sleep(5)
            
            #Submit Button Click
            submitButton=driver.find_element_by_name('Submit')
            submitButton.click()
            numSubmissions = numSubmissions + 1
            #TransactionDB
            transactionCursor=transCnx.cursor(buffered=True) 
            transactionQuery=('INSERT INTO transactions (`database`,`first_name`,`last_name`,`email`,`phone`,`utm_source`,`utm_medium`,`utm_campaign`,`program`,`timestamp`) VALUES("' + database + '", "' + first_name + '", "' + last_name + '", "' + email + '", "' + phone + '", "'+ utm_source + '", "' + utm_medium+ '", "' + utm_campaign +'", "' + program + '",CURRENT_TIME())')
            #Execute SQL Query
            transactionCursor.execute(transactionQuery)
            #commit to DB
            transCnx.commit()

            #Wait until Thank you Message confirms data submission
            element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "form-thank-you-message"))
            )
            print("Found Thank you message")
            driver.get("https://google.com")
            print(database, id, time_of_submission, programOption, program, first_name,last_name,email,phone, file=open("record.txt","a"))
            break
    #Close Cursor
    cursor.close()
    break
    #Close mySQL Connection after cycling through all DBs
cnx.close()
#################################################


#Close Chrome Browser
driver.close()
#################################################
end_time = time.time() - start_time
print(end_time, file=open("record.txt","a"))
print(numSubmissions," entries added to salesforce", file=open("record.txt","a"))
f.close()
#End of Program







#Country Input (Not important)
#Useful for Program Dropdown
# countryInput=driver.find_element_by_name("Mailing_Country__c")
# countryInputSelector = Select(countryInput)
# countryInputSelector.select_by_value(country)
######################################

#driver.get('http://go.miami.edu/specialized-masters')


