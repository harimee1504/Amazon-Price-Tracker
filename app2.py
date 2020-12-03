import re
import time
import smtplib
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from email.message import EmailMessage
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

global titlst, pricelst
titlst, pricelst = [], []


def titlename(URL):
    if len(titlst) != 0:
        return titlst[0]
    else:
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'lxml')
        title = soup.find(id="productTitle")
        for d in soup.findAll('div', attrs={'class': 'a-section a-spacing-none'}):
            name = d.find(
                'span', attrs={'class': 'a-size-large product-title-word-break'})
            if name != None:
                res = name.get_text()
                titlst.append(res.strip())
        if title != None:
            res = title.get_text()
            titlst.append(res.strip())
        return titlename(URL)


def pricename(URL):
    if len(pricelst) != 0:
        return pricelst[0]
    else:
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'lxml')
        price = soup.find(id="priceblock_dealprice")
        for d in soup.findAll('div', attrs={'class': 'a-section a-spacing-small'}):
            name = d.find(
                'span', attrs={'class': 'a-size-medium a-color-price priceBlockBuyingPriceString'})
            if name != None:
                res = name.get_text()
                pricelst.append(res.strip())
        if price != None:
            res = price.get_text()
            pricelst.append(res.strip())
        return pricename(URL)


@app.route("/")
def index():
    return render_template("amazon.html")


@app.route('/amazonTracker', methods=['GET', 'POST'])
def amazon():
    if request.method == 'POST':

        URL = request.form.get("url")
        title = titlename(URL)
        price = pricename(URL)
        global titlst, pricelst
        titlst, pricelst = [], []
        return str(title+'\n'+price)
