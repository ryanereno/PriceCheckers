import smtplib
import requests
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


def main():
    # this lets python know that price will be referring to the global one defined above
    global price

    my_url = 'http://rb.gy/legkuo'

    price = getPrice(my_url)

    checkPrice(price, my_url)


def sendEmail(my_url):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS,
                    RECIPIENT,
                    MSG + my_url)

    server.quit()


def checkPrice(original_price, my_url):
    global price

    new_price = getPrice(my_url)

    if new_price < original_price:
        sendEmail(my_url)
        price = new_price

    elif new_price > original_price:
        price = new_price


def getPrice(my_url):
    resp = requests.get(my_url, headers=HEADERS)

    ps = soup(resp.content, 'lxml')

    container = ps.findAll("span", {"id": "price_inside_buybox"})
    temp_price = container[0].text

    new_price = float(temp_price[2:len(temp_price)])

    return new_price


main()
