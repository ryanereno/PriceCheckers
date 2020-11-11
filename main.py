import smtplib
import requests
import time
import schedule
from tkinter import *
from bs4 import BeautifulSoup as soup

EMAIL_ADDRESS = 'NotifyingPrice@gmail.com'
EMAIL_PASSWORD = 'FuckChegg123'
RECIPIENT = ''
PRICE_MSG = 'The price for your item has lowered! Purchase Now! \n'
INITIAL_MSG = 'Thank you for signing up! We will track this items price \n'
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
           "Connection": "close", "Upgrade-Insecure-Requests": "1"}
price = None
my_url = ''


def main():
    # function for GUI to run
    GUI()

    # checking values to be correct
    print(price)
    print(my_url)
    print(RECIPIENT)

    # cant add a float to string to print it out
    # string_price = str(price)
    # just checking the price
    # print('The price is $' + string_price)


#    while True:
#        schedule.run_pending()
#        time.sleep(86401)


def sendPriceEmail():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS,
                    RECIPIENT,
                    PRICE_MSG + my_url)

    server.quit()


def sendInitialEmail():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS,
                    RECIPIENT,
                    INITIAL_MSG + my_url)

    server.quit()


def checkPrice(original_price):
    global price

    new_price = getPrice()

    if new_price < original_price:
        sendPriceEmail()
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

    return new_price


def GUI():
    master = Tk()

    # e1 is the input field for URL and e2 is for Email
    e1 = Entry(master)
    e1.grid(row=0, column=1)
    e1.insert(10, 'Newegg URL')

    e2 = Entry(master)
    e2.grid(row=1, column=1)
    e2.insert(20, 'Email')

    # get refers to the command used by the submit button
    # one the submit button is hit my_url and RECIPIENT are updated
    # and a confirmation email is sent
    def get():
        global my_url
        global RECIPIENT
        global price

        my_url = e1.get()
        RECIPIENT = e2.get()


        # make sure the user inputs a valid newegg URL and EMAIL
        try:
            price = getPrice()
            try:
                sendInitialEmail()

                master.quit()

            except:
                print("NOT A VALID EMAIL")  # implement this in gui later

        except:
            print("NOT A VALID URL")        # implement this in gui later

    Button(master, text="Submit", command=get).grid(row=3, column=1)

    mainloop()


main()
