import re
import time
import smtplib
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from email.message import EmailMessage
from flask import Flask, render_template, redirect, request

app = Flask(__name__)


def sendmail(name, receiver, tit, url1, r):
    Email_PASSWORD = "JO8NC5NAaa"
    Email_ADDRESS = "hariwebpage@gmail.com"
    url = re.split('//', url1)
    url = url[-1]
    msg = EmailMessage()
    msg['From'] = Email_ADDRESS
    msg['To'] = receiver
    if r == 'zero':
        msg['Subject'] = 'Amazon Price Track-Price Fell Down'
        mg = "Your Product:\n\n "+tit + \
            "\n\nIt's Price Fell Down below your Desired Price - Check it out:\n\n" + \
            url
    else:
        msg['Subject'] = 'Amazon Price Track-Price Still Above'
        mg = "Your Product:\n\n"+tit + \
            "\n\nIt's Price is still above your Desired Price - Check it out:\n\n" + \
            url
    msg.set_content(mg)

    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(Email_ADDRESS, Email_PASSWORD)
    smtp.send_message(msg)
    smtp.quit()


@app.route("/")
def index():
    return render_template("amazon.html")


@app.route('/amazonTracker', methods=['GET', 'POST'])
def amazon():
    if request.method == 'POST':

        URL = request.form.get("url")
        name = request.form.get("fname")
        email = request.form.get("email")
        DesiredPrice = request.form.get("price")
        ua = UserAgent()
        headers = {
            'User-Agent': ua.chrome}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find(id='productTitle').get_text()
        title = title.strip()
        price = soup.find(id="priceblock_ourprice")
        if price == None:
            price = soup.find(id="priceblock_dealprice")
        price = price.get_text()
        price = float(''.join(price[2:-3].split(',')))

        if price <= float(DesiredPrice):
            flag = 'zero'
        else:
            flag = 'one'
        ims = soup.findAll('img')
        img_list = []
        for i in ims:
            try:
                if i['alt'] == title.strip():
                    img_list.append(i['src'])
            except:
                pass
        rating = str(soup.find('span', {"class": "a-icon-alt"}).get_text())
        sendmail(name, email, title, URL, flag)
        return render_template('details.html', title=title, price=str(price)[:-2], dprice=DesiredPrice, url=URL, img_url=img_list[-1], rating=rating)
