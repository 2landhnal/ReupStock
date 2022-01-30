import csv
import flask
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from csv import reader
from flask_sqlalchemy import SQLAlchemy
from random import choice
import os

colors = [
   'background-color: #FA8BFF; background-image: linear-gradient(19deg, #FA8BFF 0%, #2BD2FF 52%, #2BFF88 90%); color:white;',
   'background-color: #21D4FD; background-image: linear-gradient(19deg, #21D4FD 0%, #B721FF 100%); color:white;',
   'background-color: #FEE140; background-image: linear-gradient(19deg, #FEE140 0%, #FA709A 100%); color:white;',
   'background-color: #FEE140; background-image: linear-gradient(19deg, #FEE140 0%, #FA709A 100%); color:white;',
   'background-color: #4158D0; background-image: linear-gradient(19deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%); color:white;',
   'background-color: #F4D03F; background-image: linear-gradient(19deg, #F4D03F 0%, #16A085 100%); color:white',
   'background-color: #74EBD5; background-image: linear-gradient(19deg, #74EBD5 0%, #9FACE6 100%); color:white',
   'background-image: linear-gradient( 19deg,  rgba(61,245,167,1) 11.2%, rgba(9,111,224,1) 91.1% ); color:white',
   'background-image: linear-gradient( 19deg,  rgba(245,116,185,1) 14.7%, rgba(89,97,223,1) 88.7% ); color:white',
   'background-image: linear-gradient( 19deg,  rgba(71,139,214,1) 23.3%, rgba(37,216,211,1) 84.7% ); color:white',
   'background-image: linear-gradient( 19deg,  rgba(201,37,107,1) 15.4%, rgba(116,16,124,1) 74.7% ); color:white',
   'background-image: linear-gradient( 19deg,  rgba(115,18,81,1) 10.6%, rgba(28,28,28,1) 118% ); color:white',
   'background-image: linear-gradient( 19deg,  rgba(31,212,248,1) 11%, rgba(218,15,183,1) 74.9% ); color:white',
   'background-image: linear-gradient( 19deg,  rgba(24,138,141,1) 11.2%, rgba(96,221,142,1) 91.1% ); color:white',
]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL1', 'sqlite:///data.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'aa8sda8saha8su9daasHABIAa89s8YS8a'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)


class Companies(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   sym = db.Column(db.String(250), nullable=False)
   name = db.Column(db.String(250), nullable=False)
   ope = db.Column(db.String(250), nullable=False)
   high = db.Column(db.String(250), nullable=False)
   low = db.Column(db.String(250), nullable=False)
   date = db.Column(db.String(250), nullable=False)
   color = db.Column(db.String(250), nullable=False)

db.create_all()

def create():
   with open('static/data.csv', 'r') as read_obj:
      rows = reader(read_obj)
      rows = list(rows)

   symbol_list = [row[0] for row in rows[1:]]
   symbolist = ','.join(symbol_list)

   params = {
      'access_key': '107492fb008338b63d428f38120cd892',
      'limit': len(symbol_list),
      'symbols': symbolist,
   }

   url = 'http://api.marketstack.com/v1/intraday'
   response = requests.get(url, params=params)
   full = response.json()
   print(full)
   data = full['data']
   for i in range(len(data)):
      company = data[i]
      ope = str(company['open']) + '$'
      high = str(company['high']) + '$'
      low = str(company['low']) + '$'
      date = company['date']
      sym = company['symbol']
      comp = Companies(
         name = rows[i+1][1],
         ope = ope,
         high = high,
         low = low,
         date = date[:10],
         sym = sym,
         color = choice(colors)
      )
      db.session.add(comp)
      db.session.commit()

def update():
   with open('static/data.csv', 'r') as read_obj:
      rows = reader(read_obj)
      rows = list(rows)

   symbol_list = [row[0] for row in rows[1:]]
   symbolist = ','.join(symbol_list)

   params = {
      'access_key': '107492fb008338b63d428f38120cd892',
      'limit': len(symbol_list),
      'symbols': symbolist,
   }

   url = 'http://api.marketstack.com/v1/intraday'
   response = requests.get(url, params=params)
   data = response.json()
   data = data['data']
   for i in range(len(data)):
      company = data[i]

      ope = str(company['open']) + '$'
      high = str(company['high']) + '$'
      low = str(company['low']) + '$'
      date = company['date']
      name = rows[i+1][1]

      comp = Companies.query.get(i+1)

      print(f'{name} {ope} {high} {low} {date}')

      comp.name = name
      comp.ope = ope
      comp.high = high
      comp.low = low
      comp.date = date[:10]
      db.session.commit()

create()
# update()

@app.route('/', methods=['POST', 'GET'])
def home():
   coms = Companies.query.all()
   if request.method == 'POST':
      print('POST')
      try:
         update()
         coms = Companies.query.all()
         return redirect(url_for('home'))
      except:
         return redirect(url_for('home'))
   return render_template('index.html', coms=coms)

if __name__ == '__main__':
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)

### Sample ###
# with open('static/data.csv', 'r') as read_obj:
#    rows = reader(read_obj)
#    rows = list(rows)
#
# symbol_list = [row[0] for row in rows[1:]]
# symbolist = ','.join(symbol_list)
# print(symbolist)
# params = {
#    'access_key': '4d04caee7cb6d0d46bfe21c8f6d5a055',
#    'limit': len(symbol_list),
#    'symbols': symbolist,
# }
# url = 'http://api.marketstack.com/v1/intraday'
# response = requests.get(url, params=params)
# data = response.json()
# print(data)

### Get Companies Name and ID ###
# response = requests.get('http://api.marketstack.com/v1/tickers', params=params)
# text = response.json()
# data = text['data']
# for com in data:
#    id = com['symbol']
#    name = com['name']
#    new_row = [id, name]
#    coms.append(new_row)
#
# heading = ['Symbols', 'Company Name']
# with open('data.csv', 'a', newline='') as file:
#    writor = csv.writer(file)
#    writor.writerow(heading)
#    for com in coms:
#       new_row = [com[0], com[1]]
#       writor.writerow(new_row)

