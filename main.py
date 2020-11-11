import smtplib
import requests
import time
import schedule
from bs4 import BeautifulSoup as soup

EMAIL_ADDRESS = 'NotifyingPrice@gmail.com'
EMAIL_PASSWORD = 'FuckChegg123'
RECIPIENT = ''
MSG = 'The price for your item has lowered! Purchase Now! \n'
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
           "Connection": "close", "Upgrade-Insecure-Requests": "1"}
price = None
my_url = ''


def main():
    # this lets python know that price will be referring to the global one defined above
    global price
    global my_url

    my_url = 'https://rb.gy/j8eslh'

    price = getPrice()

    # cant add a float to string to print it out
    # string_price = str(price)
    # just checking the price
    # print('The price is $' + string_price)


#    while True:
#        schedule.run_pending()
#        time.sleep(86401)


def sendEmail():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS,
                    RECIPIENT,
                    MSG + my_url)

    server.quit()


def checkPrice(original_price):
    global price

    new_price = getPrice()

    if new_price < original_price:
        sendEmail()
        price = new_price

    elif new_price > original_price:
        price = new_price


def getPrice():
    resp = requests.get(my_url, headers=HEADERS)

    ps = soup(resp.content, 'lxml')

    # the whole number of the price is in a strong tag
    strong_num = ps.findAll("strong")

    # the decimal is in a sup tag
    small_num = ps.findAll("sup")

    new_price = float(strong_num[1].text + small_num[0].text)
    print(new_price)

    return new_price


main()
