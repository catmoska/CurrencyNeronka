import fake_useragent
import requests
# from bs4 import BeautifulSoup
import time
from threading import *
from config import *
import pyscreenshot as ImageGrab
import pytesseract
import numpy as np
import cv2
import random

timer = 0.8 + random.randint(-5,5)/100
# очен плахая идея
pars = True

# подклучения тесиракт оср
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# регистрасия
sesion = requests.Session()
def registr():
	global sesion
	urlRegistr = 'https://libertex.fxclub.org/spa/auth/login'
	userAgent = fake_useragent.UserAgent().random
	HEADERSRegistr = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36", "accept": '*/*', 'user-agent':userAgent}
	data = {'login':'vitalka200520052018@gmail.com','password':'20182018ящщящщ'}

	respont = sesion.post(urlRegistr,data =data,headers=HEADERSRegistr)
registr()

# даний для парсинга
URL = 'https://libertex.fxclub.org/spa/instruments'
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36","accept":'*/*'}
parserIndeks= {
	0:[54510.99,False,1,0],
	1:[54510.99,False,1,0],
	2:[54510.99,False,1,0]
}

# парсинг
def get_html(URL,indeks=0):
	global nrokses,sesion
	getZanros = sesion.get(URL,headers=HEADERS)
	if getZanros.status_code == 200:
		data = getZanros.json()
		# print(data['instruments'][parserIndeks[indeks][2]]['symbol'])
		return float(data['instruments'][parserIndeks[indeks][2]]['ask'])
	else:
		parserIndeks[indeks][3] += 1
		if parserIndeks[indeks][3] == 5:
			parserIndeks[indeks][1] = False
		print("ошибка соидинения")
		return parserIndeks[indeks][0]

def parsirnt(indeks = 0):
	global URL
	parserIndeks[indeks][0] = get_html(URL,indeks)

# обновляит сканирования
def parsWair():
	global timer
	nroxod =0
	while True:
		nroxod += 1
		for i in range(len(parserIndeks)):
			if parserIndeks[i][1]:
				parsirnt(i)
		time.sleep(timer)

# записует какий модели сканировать
def parsTrue(indeks):
	parserIndeks[indeks][1] = True

# видает знасения програме и за одно видает лист
def znacenia(indeks):
	return parserIndeks[indeks][0]

startParser = Thread(target=parsWair)
startParser.start()
