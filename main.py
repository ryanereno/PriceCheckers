import smtplib
import requests
from bs4 import BeautifulSoup as soup

EMAIL_ADDRESS = 'NotifyingPrice@gmail.com'
EMAIL_PASSWORD = 'FuckChegg123'
RECIPIENT = ''
MSG = ''


server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
server.sendmail(EMAIL_ADDRESS,
                RECIPIENT,
                MSG)

server.quit()


headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

my_url = 'http://rb.gy/kjkteb'

resp = requests.get(my_url, headers = headers)


ps = soup(resp.content, 'lxml')

container = ps.findAll("span", {"id": "price_inside_buybox"})

temp = container[0].text

actual = float(temp[2:len(temp)])


requested = float(input())

if requested == actual:
    print("Yurt")

else:
    print("Nah G")