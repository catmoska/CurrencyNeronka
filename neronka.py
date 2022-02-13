# неронка
print("подготовка")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from config import *
import matplotlib.pyplot as plt
import pandas as pd
import random
import csv
import numpy as np
import time
import cv2
import pyautogui
from tensorflow import keras
from tensorflow.keras.layers import Dense
from datetime import datetime
from numba import jit
from parsers import *

stop=False

def seveModel(model,indeks,srednia):
	print("seve.model")
	model.save(modelNeim[indeks])
	modelNeimm = modelNeim[indeks] + '.txt'
	if indeks == 0 or indeks == 1:
		modelNeimm = 'bitcoin.txt'
	f = open(modelNeimm,"w")
	f.write(str(srednia))

def seveTest(seveCSV):
	with open("test.csv","a") as f:
		writer = csv.writer(f)
		writer.writerow(seveCSV)

def nerevodV(r,sredni):
	return r / sredni

def nerevodO(r,sredni):
	return r * sredni

def timess(times,zaderzka=0.01,nroxod=0,seve=False):
	u=times-zaderzka-0.08*nroxod

	if u<0:
		print("ошибка времини: " + str(u))
		return

	if seve and u>0.3:
		time.sleep(u-0.3)
	else:
		time.sleep(u)

class contolModel:
	global stop

	# стартует вмести с класом
	def __init__(self,indeks=0):
		self.model = keras.Sequential()
		self.model = modelStruktura(self.model,indeks)
		self.modelNeim = modelNeim[indeks]
		self.indeks = indeks
		self.neroni = neroni[indeks]
		self.sredni = sredni[indeks]
		self.timee = timee
		self.ystrivaniaN = 0
		self.robotaet = False
		self.zagatovka =[]
		self.zagatovkaN =[]
		parsTrue(indeks)
		print("metod __init__ indeks: " + str(self.indeks))

	# 1 и 2 провирают фаили на устаривания
	def ystrivania1(self):
		ystrivaniaStart = Thread(target=self.ystrivania2)
		if not self.robotaet:
			ystrivaniaStart.start()

	def ystrivania2(self):
		self.robotaet = True
		self.ystrivaniaN == 1
		for i in range(10):
			time.sleep(0.5)
			if self.ystrivaniaN ==2 or self.ystrivaniaN ==0:
				self.robotaet = False
				return
		self.ystrivaniaN =0
		self.robotaet = False

	# заготавливает селий списак даних для неронки
	def zagatovsik(self):
		self.zagatovka=[]
		self.zagatovkaN = []
		self.ystrivaniaN =2

		for i in range(self.neroni):
			timess(timee)
			u = znacenia(self.indeks)
			self.zagatovka.append(u)
			self.zagatovka.insert(i, float(self.zagatovka[i]))
			print(str(u) + "    /    " + str(((i + 1) / self.neroni) * 100) + "%")
			if stop:
				pass

		self.sredni = (self.sredni+sum(self.zagatovka)) / (self.neroni+1)
		self.ystrivania1()
		print("metod zagatovsik indeks: " + str(self.indeks))

	# переваривает даний для неронки
	def dani(self,noviDani=None):
		if self.ystrivaniaN > 0:
			if noviDani == None:
				noviDani = znacenia(self.indeks)
			self.ystrivaniaN =2

			self.zagatovka.append(noviDani)

			liN = []
			for q in range(self.neroni):
				liN.append(self.zagatovka[q + 1])

			self.zagatovka = []
			for i in range(self.neroni):
				self.zagatovka.insert(i, float(liN[i]))

			# переобразования значений в просентное состояния
			self.zagatovkaN = []
			for i in range(self.neroni):
				self.zagatovkaN.append(nerevodV(self.zagatovka[i],self.sredni))

			# переобразавания фаила
			listttN = []
			for q in range(self.neroni - 2):
				listttN.append(self.zagatovkaN[q + 1])
			zagatovkaNu = self.zagatovkaN
			zagatovkaNu.append(self.nroxodMatematiciOtvet(True))

			# подготовка значений для неронки кроме последного
			self.training_inputs = np.array([[zagatovkaNu], [zagatovkaNu]])

			# подготовка последного нерона для подготовки
			self.tt = float(self.zagatovkaN[self.neroni - 1])
			self.training_outputs = np.array([self.tt, self.tt])

			self.ystrivania1()
			print("metod dani indeks: " + str(self.indeks))
			return [self.training_outputs, self.training_inputs,self.zagatovka,self.zagatovkaN, self.tt]
		print("metod dani indeks: " + str(self.indeks))

	# перезаписует даний
	def restr(self):
		self.ystrivaniaN =2
		self.zagatovsik()
		self.dani()
		self.ystrivania1()
		print("metod restr indeks: " + str(self.indeks))

	# видает резултат по даним в памяти
	def nroxodNeronkiOtvet(self,t =True):
		if t and self.ystrivaniaN > 0:
			self.ystrivaniaN = 2
			print("metod nroxodNeronkiOtvet indeks: " + str(self.indeks))
			self.ystrivania1()
			return self.model.predict(self.dani()[1])[0][0][0]
		elif self.ystrivaniaN > 0:
			return self.model.predict(self.training_inputs)[0][0][0]

	def nroxodMatematiciOtvet(self, t=False):
		matematicZagotovka = []
		for i in range(matematicNeroni[self.indeks]):
			matematicZagotovka.append(self.zagatovkaN[i])

		a = []
		for i in range(matematicNeroni[self.indeks]-1):
			a.append(matematicZagotovka[i] - matematicZagotovka[i + 1])

		# for i in range(matematicNeroni[self.indeks]-1):
		# 	a[i] = a[i]*((i+200)**2)

		if t:
			l = sum(a)
			if l == 0:
				return 0.5
			elif l > 0:
				return 1
			else:
				return 0

		return self.zagatovkaN[len(self.zagatovkaN)-1] + sum(a)
	
	# обучения модуля
	def obusenia(self,nroxodObusenia,Tixa=1):
		if self.ystrivaniaN==0 or not parserIndeks[self.indeks][1]:
			return

		print('')

		self.ystrivaniaN = 2

		timess(self.timee,0.1,nroxod,nroxodObusenia%20==0)

		self.dani()
		print("metod obusenia indeks: " + str(self.indeks))

		if Tixa != 0:
			Otvet1 = self.nroxodNeronkiOtvet(False)
			print("до   " + str(Otvet1) + "  OtvetN /  " + str(nerevodO(Otvet1,self.sredni)) + "  Otvet  /  " + str(
				self.zagatovka[self.neroni - 1]) + "  OtvetOgidaitca  /  " + str(Otvet1 / self.tt - 1) + "%  " + str(
				self.zagatovka[self.neroni - 1] - nerevodO(Otvet1,self.sredni)) + "  ошибка")

		# обучения нероронки
		self.model.fit(x=self.training_inputs, y=self.training_outputs, epochs=nroxod, validation_split=0.2, verbose=Tixa)

		if Tixa != 0:
			Otvet2 = self.nroxodNeronkiOtvet(False)
			print("после   " + str(Otvet2) + "  OtvetN /  " + str(nerevodO(Otvet2,self.sredni)) + "  Otvet  /  " + str(
				self.zagatovka[self.neroni - 1]) + "  OtvetOgidaitca  /  " + str(Otvet2 / self.tt - 1) + "%  " + str(
				self.zagatovka[self.neroni - 1] - nerevodO(Otvet2,self.sredni)) + "  ошибка")
			print(self.nroxodMatematiciOtvet(True))
			print("вмести   " + str(Otvet2 / Otvet1) + "  отношения  " + str(Otvet2 - Otvet1))

		# вивод даних
		if nroxodObusenia % 20 == 0:
			seveModel(self.model,self.indeks,self.sredni)

		print("проход:  " + str(nroxodObusenia))
		self.ystrivania1()

	# обучения модуля постояна
	def startObusenia(self,nroxod):
		print("start metod startObusenia indeks: " + str(self.indeks))
		if self.ystrivaniaN == 0:
			self.restr()
		self.ystrivaniaN = 2
		nroxodObusenia = 1

		if nroxod < 1:
			while True:
				self.obusenia(nroxodObusenia)
				nroxodObusenia += 1

				if not parserIndeks[self.indeks][1]:
					print('ошибка обучения закончилась')
					return
				if stop:
					print("metod startObusenia stop indeks: " + str(self.indeks))
					return
		else:
			for i in range(nroxod):
				self.obusenia(nroxodObusenia)
				nroxodObusenia +=1

				if not parserIndeks[self.indeks][1]:
					print('ошибка обучения закончилась')
					return
				if stop:
					print("metod startObusenia stop indeks: " + str(self.indeks))
					return
		self.ystrivania1()
		seveModel(self.model, self.indeks)
		print("metod startObusenia   " + str(self.indeks))

	# генирирует резултат спустя 'время'
	def generitModel(self,NaSkolko,Sxema = False):
		timeesik =self.timee
		if self.timee<=0 :
			timeesik = 1

		nroxod = round( NaSkolko / timeesik)
		nroxodSxema = []

		if self.ystrivaniaN == 0:
			self.restr()

		self.ystrivaniaN =2
		for rill in range(nroxod):
			Otvet = self.nroxodNeronkiOtvet(False)
			self.dani(Otvet)
			if Sxema:
				nroxodSxema.append(Otvet)
			if stop:
				print("metod generitModel stop indeks: " + str(self.indeks))
				return

		if Sxema:
			plt.plot(nroxodSxema)
			plt.grid(True)
			plt.show()

		self.ystrivaniaN = 0
		print("metod generitModel indeks: " + str(self.indeks))
		return nerevodO(Otvet,self.sredni)

	def generitModelMatematek(self,NaSkolko,Sxema = False):
		timeesik =self.timee
		if self.timee<=0 :
			timeesik = 1

		nroxod = round( NaSkolko / timeesik)
		nroxodSxema = []

		if self.ystrivaniaN == 0:
			self.restr()

		self.ystrivaniaN =2
		for rill in range(nroxod):
			Otvet = self.nroxodMatematiciOtvet(False)
			self.dani(nerevodO(Otvet,self.sredni))
			if Sxema:
				nroxodSxema.append(Otvet)
			if stop:
				print("metod generitModelMatematek stop  indeks: " + str(self.indeks))
				return

		if Sxema:
			plt.plot(nroxodSxema)
			plt.grid(True)
			plt.show()

		self.ystrivaniaN = 0
		print("metod generitModelMatematek indeks: " + str(self.indeks))
		return nerevodO(Otvet,self.sredni)

	# фоновое обучения (не рекомендую исползовать вного)
	def fonavaiObusenia(self,start = True):
		if self.ystrivaniaN > 0:
			Obusenia = contolModel(self.indeks)
			fonavaiObusenia = Thread(target=Obusenia.strtObusenia,args=(0))
			fonavaiObusenia.start()
		print("metod fonavaiObusenia indeks: " + str(self.indeks))

	# знасения парсера для testa
	def znaceniaDyblicat(self):
		print("metod znaceniaDyblicat indeks: " + str(self.indeks))
		return znacenia(self.indeks)

	def ocnovnoiSever(self):
		seveModel(self.model, self.indeks)

# тест модели бута как и весь етот код
def testModel(indeks):
	global stop
	if stop:
		pass
	stop = True

	test = contolModel(indeks,True)
	testDo = test.generitModel(60)
	time.sleep(60)
	testNosle = test.znaceniaDyblicat()
	print(str(testDo/testNosle)+"%  "+str(testDo-testNosle)+"  кофисиент ошибкй")


print("готов")