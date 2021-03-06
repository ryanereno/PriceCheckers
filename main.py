import smtplib
import requests
import csv
import time
import schedule
from tkinter import *
from bs4 import BeautifulSoup as soup

#insert email address and password for bot
EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''
RECIPIENT = ''
PRICE_MSG = 'The price for your item has lowered to $! Purchase Now! \n'
INITIAL_MSG = 'Thank you for signing up! We will track this items price \n'
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
           "Connection": "close", "Upgrade-Insecure-Requests": "1"}
price = None
my_url = ''

ALL_LINKS = []
ALL_PRICES = []
ALL_EMAILS = []
data = open("checker_database.csv", "a+")


def main():
    # function for GUI to run
    GUI()

    # checking values to be correct
    #print(price)
    #print(my_url)
    #print(RECIPIENT)


    # tracking links,emails,and prices to file
    # writeToFile()
    # cant add a float to string to print it out
    # string_price = str(price)
    # just checking the price
    # print('The price is $' + string_price)


#    while True:
#        schedule.run_pending()
#        time.sleep(86401)


def sendPriceEmail(email):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS,
                    email,
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
    index = 0

    for x in ALL_LINKS:
        new_price = getPrice(x)

        if new_price < ALL_PRICES[index]:
            sendPriceEmail(ALL_EMAILS[index])
            ALL_PRICES[index] = new_price
            index += 1

        elif new_price > original_price:
            ALL_PRICES[index] = new_price


def getPrice(url):
    resp = requests.get(url, headers=HEADERS)

    ps = soup(resp.content, 'lxml')

    # the whole number of the price is in a strong tag
    strong_num = ps.findAll("strong")

    # the decimal is in a sup tag
    small_num = ps.findAll("sup")

    new_price = float(strong_num[1].text + small_num[0].text)

    return new_price


def writeToFile():
    global data
    data.write(my_url + ',' + str(price) + "," + RECIPIENT + "\n")
    data.close()


def readFile():
    global ALL_LINKS
    global ALL_PRICES
    global ALL_EMAILS

    tracker = 0

    with open('checker_database.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            ALL_LINKS.insert(tracker, row[0])
            ALL_PRICES.insert(tracker, float(row[1]))
            ALL_EMAILS.insert(tracker, row[2])
            tracker += 1

    data.close()


def GUI():
    master = Tk()

    # window size
    master.geometry('600x70')

    # e1 is the input field for URL and e2 is for Email
    e1 = Entry(master, width=100)
    e1.grid(row=0, column=1)
    e1.insert(10, 'Newegg URL')

    e2 = Entry(master, width=100)
    e2.grid(row=1, column=1)
    e2.insert(20, 'Email')

    # get refers to the command used by the submit button
    # once the submit button is hit my_url and RECIPIENT are updated
    # and a confirmation email is sent
    def get():
        global my_url
        global RECIPIENT
        global price

        my_url = e1.get()
        RECIPIENT = e2.get()

        # make sure the user inputs a valid newegg URL and EMAIL
        try:
            price = getPrice(my_url)
            try:
                sendInitialEmail()

                master.quit()

            except:
                errorMSG = 'NOT A VALID EMAIL'
                popupMsg(errorMSG)

        except:
            errorMSG = "NOT A VALID URL"
            popupMsg(errorMSG)

    # submit button
    Button(master, text="Submit", command=get, width=50).grid(row=3, column=1)

    mainloop()


def popupMsg(msg):
    popup = Tk()
    popup.wm_title("!")
    label = Label(popup, text=msg, foreground="red", font='Helvetica 20 bold')
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


main()
