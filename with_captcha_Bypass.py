from selenium import webdriver
import requests
import time

API_KEY='2captcha api key'
data_sitekey='6LcGZjIaAAAAAIQ6iL31H6IIfGRnEmgWBYUkZOgi'

loginid='enter email'
passwd='your password'

driver =webdriver.Chrome('chromedriver.exe')
driver.get('https://labs.vocareum.com/home/login.php?/util/vcauth.php')

user_input = driver.find_element_by_id('inputEmail')
user_input.send_keys(loginid)

passwd_input = driver.find_element_by_id('inputPassword')
passwd_input.send_keys(passwd)

login_button = driver.find_element_by_xpath("//button[contains(text(),'Continue')]")
login_button.click()

time.sleep(30)

curr_url=driver.current_url

print(curr_url)

if curr_url!="https://labs.vocareum.com/main/main.php?m=dashboard":
    url1="https://labs.vocareum.com/home/login.php?/util/vcauth.php"
    u1=f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&googlekey={data_sitekey}&pageurl={url1}&json=1&invisible=1"
    r1=requests.get(u1)
    print(r1.json())
    rid=r1.json().get("request")
    u2=f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={int(rid)}&json=1"
    time.sleep(5)
    while True:
        r2 = requests.get(u2)
        print(r2.json())
        if r2.json().get("status") == 1:
            form_tokon=r2.json().get("request")
            break
    time.sleep(5)
    driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"'% form_tokon)
    time.sleep(3)
    driver.execute_script('onSubmit("%s")'%form_tokon)
    print("Submitted")
    time.sleep(3)
    driver.get("https://labs.vocareum.com/main/main.php?m=editor&nav=1&asnid=14334&stepid=14335")
    driver.get("https://labs.vocareum.com//util/vcput.php?a=getaws&nores=0&stepid=14335&mode=s&type=0&vockey=")
    

else:
    ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    driver.get("https://labs.vocareum.com/main/main.php?m=editor&nav=1&asnid=14334&stepid=14335")
    driver.get("https://labs.vocareum.com//util/vcput.php?a=getaws&nores=0&stepid=14335&mode=s&type=0&vockey=")
    headers = {'User-Agent':ua, 'Accept-Language': 'en-GB,en;q=0.5'}
    url5="https://labs.vocareum.com//util/vcput.php?a=getaws&nores=0&stepid=14335&mode=s&type=0&vockey=s.cookies['logintoken']"
    aws = requests.get(url5, headers=headers, stream=True)
    text=aws.text.split('\n')[1:4]
    print(text)