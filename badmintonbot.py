#The following code is customised to the booking of badminton courts at Nanyang Technological University, Singapore.

from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from pyautogui import press
from twilio.rest import Client

def timeslotxpath(time,court):
    if court == 1:
        col = "10"
    else:
        col = "9"
    row = str(((time - 8) * 6) + 1 + court)
    timeslotxpath = '//*[@id="ui_body_container"]/table/tbody/tr/td[2]/form/table[2]/tbody/tr[' + row + ']/td[' + col + ']/input'
    return timeslotxpath

court_list = [1,2,3,4,5,6]
court = int(input("Court:"))
timeinput = int(input("Slot:"))
#Below two lines are credentials of the website account.
#Username = 
#Password = 
driver = webdriver.Chrome()
client = Client("AC06b675e849ca915a2413c176b436a2a1", "e397e3b8369b19f310da881532a530d2")
driver.get("https://sso.wis.ntu.edu.sg/webexe88/owa/sso_login1.asp?t=1&p2=https://wis.ntu.edu.sg/pls/webexe88/srce_smain_s.Notice_O&extra=&pg=")
username_input = driver.find_element_by_xpath("/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input")
username_input.send_keys(Username)
okbutton = driver.find_element_by_xpath('/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[4]/td/input[1]')
okbutton.click()
password_input = driver.find_element_by_xpath("/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/input")
password_input.send_keys(Password)
okbutton = driver.find_element_by_xpath('/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[5]/td/input[1]')
okbutton.click()
first_time = True
done = False
while True:
    facilitybutton = driver.find_element_by_xpath('//*[@id="ui_body_container"]/table/tbody/tr/td[2]/form/ul/li[4]/table[2]/tbody/tr[1]/td/input')
    facilitybutton.click()
    while first_time == True:
        time = datetime.now()
        time = time.strftime('%X')
        time = time.split(':')
        if time[1] == "00" and time[2] == "00a":
            driver.refresh()
            break
    while court_list != []:
        court_list.remove(court)
        try:
            if first_time == True:
                first_time = False
                slotbutton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, timeslotxpath(timeinput,court))))
            else:
                slotbutton = driver.find_element_by_xpath(timeslotxpath(timeinput,court))
            slotbutton.click()
            try:
                confirmbutton = driver.find_element_by_xpath('//*[@id="ui_body_container"]/table/tbody/tr/td[2]/form/input[18]')
                confirmbutton.click()
                done = True
                break
            except UnexpectedAlertPresentException:
                press('enter')
                cancelbutton = driver.find_element_by_xpath('//*[@id="ui_body_container"]/table/tbody/tr/td[2]/form/input[19]')
                cancelbutton.click()
                court = court_list[0]
                break
        except (NoSuchElementException,TimeoutException):
            if court_list != []:
                print(court_list)
                court = court_list[0]
    if done == True:
        print("Booking is successful.")
        client.messages.create(to="+6583320438", \
                       from_="+17852644138", \
                       body="Booking is successful.")
        break
    elif court_list == []:
        print("There are no vacant slots left.")
        client.messages.create(to="+6583320438", \
                       from_="+17852644138", \
                       body="There are no vacant slots left.")
        driver.quit()

            
                



