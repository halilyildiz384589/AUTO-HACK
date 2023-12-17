# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 17:48:52 2023

@author: halil yildiz
"""

#1.kutuphaneler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# veri yukleme - verilerden oluşturduğumuz değerleri çekiyoruz
veriler = pd.read_csv('degerler_hizlar_3.csv')

# Verileri özellikler ve etiketler olarak ayırıyoruz 
X = veriler[['Hiz']]
y = veriler['Delta_t_Degeri']


# Verileri eğitim ve test setlerine bölüyoruz
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=42)

# Standart scaler  ile ölçeklendirme yapıyoruz
sc_X = StandardScaler()
sc_y = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
y_train = sc_y.fit_transform(y_train.values.reshape(-1, 1))
y_train = y_train.ravel() #tek boyutlu hale getiriyoruz

# SVR modelini oluşturuyor ve eğitiyoruz
svr = SVR(kernel='rbf')
svr.fit(X_train, y_train) #svr modelimizi eğitiyoruz

# Test sonuçlarını y_pred değişkeninde tuttum.
y_pred = svr.predict(X_test)
y_pred = sc_y.inverse_transform(y_pred.reshape(-1, 1)) # Tahminleri yeniden şekillendirme

# Performans ölçümlerini yapalım.

from sklearn.metrics import r2_score

r2 = r2_score(y_test, sc_y.inverse_transform(y_pred))
print("R2 Skoru:", r2)


#Tahminler
#SVR kullanarak farklı hız değerlerine göre durma süresi hesabı yapalım

# 111 m/s hız değeri için bir özellik vektörü oluşturalım
x=115
hiz_degeri = np.array([[x]])  # Özellik vektörü oluşturduk

# Hız değeri için ölçeklendirme yapalım
scaled_hiz = sc_X.transform(hiz_degeri)

# Model ile tahmin yapalım
tahmin_delta_t = svr.predict(scaled_hiz)
gercek_deger = sc_y.inverse_transform(tahmin_delta_t.reshape(-1, 1))

print(x, " m/s hızı için tahmin edilen delta_t değeri:", gercek_deger[0][0])



