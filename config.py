import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from tensorflow import keras
from tensorflow.keras.layers import Dense

neroni = [1024,240,50]                     # озидания пунктов и неронов
matematicNeroni = [100,30,50]
nroxod = 2                                  # количество повторений
sredni = [54510.99,54510.99,54510.99]       # средная значения етого обекта
k = 1                                       # кофисиент разброса
timee = 1                                   # время озидания обнавления
timerZadergok = 0.1
zagruzka =True
x1,y1,x2,y2 = 530,298,629,325

modelNeim = ["bitcoin1024","bitcoin240","test"]

def modelStruktura(model,indeks=0):
    global neroni,sredni,modelNeim

    neronii = neroni[indeks]
    modelNeimm = modelNeim[indeks] + '.txt'
    if indeks==0 or indeks==1:
        modelNeimm = 'bitcoin.txt'

    if indeks == 0:
        model.add(Dense(units=neronii, activation='sigmoid'))
        model.add(Dense(units=neronii * 4, activation='sigmoid'))
        model.add(Dense(units=neronii * 2, activation='selu'))
        model.add(Dense(units=neronii / 2, activation='sigmoid'))
        model.add(Dense(units=100, activation='sigmoid'))
        model.add(Dense(units=1, activation='linear'))
        sredni[0] = float(open(modelNeimm).read())
    elif indeks == 1:
        model.add(Dense(units=neronii, activation='sigmoid'))
        model.add(Dense(units=neronii * 6, activation='sigmoid'))
        model.add(Dense(units=neronii * 3, activation='selu'))
        model.add(Dense(units=neronii/2, activation = 'sigmoid'))
        model.add(Dense(units=100, activation='sigmoid'))
        model.add(Dense(units=1, activation='linear'))
        sredni[1] = float(open(modelNeimm).read())
    else:
        model.add(Dense(units=neronii, activation='sigmoid'))
        model.add(Dense(units=neronii * 4, activation='sigmoid'))
        model.add(Dense(units=neronii * 2, activation='selu'))
        #model.add(Dense(units=neronii / 2, activation='sigmoid'))
        model.add(Dense(units=100, activation='sigmoid'))
        model.add(Dense(units=1, activation='linear'))
        sredni[2] = float(open("sredniaExt.txt").read())

    if zagruzka:
        try:
            model = keras.models.load_model(modelNeim[indeks])
        except OSError:
            model.compile(loss='mse', optimizer="sgd", metrics=["accuracy"])
    else:
        model.compile(loss='mse', optimizer="sgd", metrics=["accuracy"])

    return model