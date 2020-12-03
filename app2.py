import re
import time
import smtplib
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from email.message import EmailMessage
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

global lst
lst = []


def titname(URL):
    if len(lst) != 0:
        return lst[0]
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
                lst.append(res.strip())
        if title != None:
            res = title.get_text()
            lst.append(res.strip())
        return titname(URL)


@app.route("/")
def index():
    return render_template("amazon.html")


@app.route('/amazonTracker', methods=['GET', 'POST'])
def amazon():
    if request.method == 'POST':

        URL = request.form.get("url")
        title = titname(URL)
        global lst
        lst = []
        return str(title)
