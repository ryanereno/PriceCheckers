import smtplib
import requests
from bs4 import BeautifulSoup as soup

EMAIL_ADDRESS = 'NotifyingPrice@gmail.com'
EMAIL_PASSWORD = 'FuckChegg123'
RECIPIENT = 'ryanaereno@gmail.com'
MSG = 'The price for your item has reached your desired price! Purchase Now! \n'

def main():
    #telling amazon that im a real browser
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    my_url = 'http://rb.gy/kjkteb'

    resp = requests.get(my_url, headers = headers)

    ps = soup(resp.content, 'lxml')

    container = ps.findAll("span", {"id": "price_inside_buybox"})
    temp_price = container[0].text

    actual_price = float(temp_price[2:len(temp_price)])
    print(actual_price)

    my_price = float(input())

    checkPrice(my_price, actual_price, my_url)

def sendEmail(my_url):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS,
                    RECIPIENT,
                    MSG + my_url)

    server.quit()

def checkPrice(my_price, actual_price, my_url):
    if my_price <= actual_price:
        sendEmail(my_url)

    else:
        print("Nah G")


main()