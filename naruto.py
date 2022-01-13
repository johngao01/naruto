import time
import pymysql
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
host = 'localhost'
port = 3306
mysql_database = 'naruto'
db_user = 'root'
password = '123456'
db = pymysql.connect(
    host=host,
    port=port,
    db=mysql_database,
    user=db_user,
    password=password)
cursor = db.cursor()
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.get('https://list.youku.com/show/id_zcc001f06962411de83b1.html')
content = browser.find_element(
    By.XPATH, '/html/body/div[2]/div/div[2]/div/div[1]/ul/li[2]')
content.click()
time.sleep(5)
for i in range(1, 73):
    browser.find_element(By.XPATH, f'//*[@id="point"]/ul/li[{i}]').click()
    time.sleep(3)
    items = browser.find_element(
        By.ID, 'point').find_elements(
        By.CLASS_NAME, 'p-item ')
    print(len(items))
    index = 1
    for j in range(-10, 0, 1):
        a = str((i - 1) * 10 + index)
        duration = items[j].find_element(By.CSS_SELECTOR,
                                         "[class='p-time'").find_element(By.TAG_NAME,
                                                                         'span').text
        title = items[j].find_element(By.CSS_SELECTOR, "[class='item-title c555']").find_element(By.TAG_NAME,
                                                                                                 'a').get_attribute('title')
        intro = items[j].find_element(
            By.CSS_SELECTOR,
            "[class='item-intro c999']").text

        url = items[j].find_element(By.CSS_SELECTOR, "[class='item-title c555']").find_element(By.TAG_NAME,
                                                                                               'a').get_attribute('href')
        print(a, title)
        info = [a, title, intro, duration, url]
        sql = 'insert into naruto values ({data})'.format(data=str(info)[1:-1])
        # print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
        index += 1
    time.sleep(5)
