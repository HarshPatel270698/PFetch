import requests
import smtplib
import time
from re import sub
from decimal import Decimal
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

prices=[]
dates=[]
times=[]

headers = {
			"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
			}
URL = 'https://www.amazon.ca/****************' # Amazon product link

def main():
	now = datetime.now()
	page = requests.get(URL, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')
	price = soup.find(id="priceblock_ourprice").get_text()
	formattedPrice = Decimal(sub(r'[^\d.]', '', price))
	today_date = now.strftime("%B %d, %Y")
	current_time = now.strftime("%H:%M:%S")
	prices.append(formattedPrice)
	dates.append(today_date)
	times.append(current_time)
	if(formattedPrice<1500): #insert your specific amount instead of 1500
		send_email()

def send_email():
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('email@gmail.com', '**********') #your email and password
	subject = 'Time to Buy'
	body = 'Link to buy product : ' + URL
	msg = f"Subject: {subject}\n\n\n{body}"
	server.sendmail(
		'email@gmail.com', #your email
		'email@gmail.com', #receiver email
		msg
	)
	print('EMAIL SENT')
	server.quit()
	insert_into_CSV()
	quit()
	

def insert_into_CSV():
	df = pd.DataFrame({'Price' : prices, 'Date' : dates, 'Time' : times }) 
	df.to_csv('Price_Track_History.csv', index=False, encoding='utf-8')
	print('<----------------------------CSV Exported---------------------------->')
	quit()

while(True):
	i=0
	while(i<24):
		main()
		time.sleep(60*60) #execute loop each hour for a day
		i+=1
	insert_into_CSV()
