import requests
import smtplib
import time
from re import sub
from decimal import Decimal
from bs4 import BeautifulSoup
headers = {
			"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
			}
URL = 'https://www.amazon.ca/****************' # Amazon product link

def main():
	page = requests.get(URL, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')
	price = soup.find(id="priceblock_ourprice").get_text()
	formattedPrice = Decimal(sub(r'[^\d.]', '', price))
	if(formattedPrice<15000):
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

while(True):
	main()
	time.sleep(60*60) #execute loop each hour