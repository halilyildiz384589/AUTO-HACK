# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 15:10:35 2023

@author: halil yildiz
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

veriler1 = pd.read_csv('dogleg.csv', decimal=',')
veriler2 = pd.read_csv('cd.csv', decimal=',')

print(veriler1)
print(veriler2)

#veriler1 için aşağıdaki değerleri hazırladım. Aslında gereksiz ve yazılımı yoran bir durum. Fakat açıklayıcı olması bakımından ihtiyaç olduğunu düşündüm

egim_value = veriler1.iloc[:,0:1].values#diziye dönüştürdüm
uzunluk = veriler1.iloc[:,1:2].values
yukseklik = veriler1.iloc[:,2:3].values
yaricap = veriler1.iloc[:,3:4].values

#veriler2 için aşağıdaki değerleri hazırladım.
model = veriler2.loc[:, 'model']
agirlik = veriler2.iloc[:,1:2].values 
katsayı_friction = veriler2.iloc[:,2:3].values
alan = veriler2.iloc[:,4].values
Cd = veriler2.iloc[:,5:6].values



# Değerleri saklayacak boş listeler oluşturalım - CSV dosyasına çevireceğiz
hiz_degerleri = []
kinetic_enerjiler = []
potansiyel_enerjiler = []
ruzgar_direnci_hesaplari = []
ruzgar_direnci_degerleri = []
fren_kuvvet_degerleri = []
delta_t_degerleri = []



#Öncelikle bu verilerden (sizinle paylaşacağımız word dosyası) kayma durumu ve buna göre hız hesaplaması ile ilgili küçük bir hesaplama blogu yazalım
#Araba kuvvet denklemlerini oluşturalım

#V1 = float(input("Arabanın başlangıç hızını giriniz (m/s): "))

#Random hız aralıkları oluşturalım
V1_degerleri = np.random.uniform(1, 350, 90)


for V1 in V1_degerleri:
    V2 = 0
    d = 100
    p_value = 1.225
    yer_cekimi_ivmesi = 9.81
    
    
    for i in range(len(agirlik)):

        #kinetik enerji
        kinetic_energy = (1/2)*agirlik[i]*((V1)**2 - (V2)**2) #V1 değerini çıktı olarak vereceğim ve V2 değerini hesaplatacağım. J
        print("Kinetik enerji(kJ): ",kinetic_energy/1000) #kilojoule çevir
        kinetic_enerjiler.append(kinetic_energy)
        
        #Potansiyel enerji
        potential_energy = agirlik[i]*yer_cekimi_ivmesi*uzunluk[i] #Joule değerinde hesapladık
        print("Potensiyel enerji(kJ): ", potential_energy/1000)
        potansiyel_enerjiler.append(potential_energy)
        
        #Rüzgar direnci hesabı - kritik bir hesap. Bu yapay zekanın en direnç hesabı diyebiliriz.
        Fd = (1/2)* float(Cd[i]) *p_value *float(alan[i]) * (V1**2) 
        print("Ruzgar direnci hesabı: ", Fd)
        ruzgar_direnci_hesaplari.append(Fd)

        #Rüzgar direnci enerjisi
        Re = Fd * d #d=100 m olarak belirlendi. Otomatik olarak veriden alınacak ama şu an bir veri olmadığından kendimiz beliriyoruz.
        print("Ruzgar direnci değeri: ", Re)
        ruzgar_direnci_degerleri.append(Re)
        
        #Frenin durdurmak için uyguladığı kuvvet 
        Fs = float(katsayı_friction[i]) *agirlik[i] *yer_cekimi_ivmesi
        print("Fren kuvvet degeri: ", Fs)
        fren_kuvvet_degerleri.append(Fs)
        
        #Dönüş süresi hesaplama   
        Delta_t = (kinetic_energy + potential_energy + Re ) / Fs
        print("Delta_t degeri: ", Delta_t)
        delta_t_degerleri.append(Delta_t)
        
        hiz_degerleri.append(V1)



# Listelerden bir DataFrame oluşturalım
data = {
    'Hiz': hiz_degerleri,
    'Kinetic_Energy': kinetic_enerjiler,
    'Potential_Energy': potansiyel_enerjiler,
    'Ruzgar_Direnci_Hesabi': ruzgar_direnci_hesaplari,
    'Ruzgar_Direnci_Degeri': ruzgar_direnci_degerleri,
    'Fren_Kuvvet_Degeri': fren_kuvvet_degerleri,
    'Delta_t_Degeri': delta_t_degerleri
}



df = pd.DataFrame(data)

# Verilerdeki parantezleri kaldıralım - Verileri uygun hale getirelim
# DataFrame içinde uygun formatlama işlemlerini yapalım
df['Kinetic_Energy'] = df['Kinetic_Energy'].astype(str).str.strip('[]').astype(float)
df['Potential_Energy'] = df['Potential_Energy'].astype(str).str.strip('[]').astype(float)
df['Fren_Kuvvet_Degeri'] = df['Fren_Kuvvet_Degeri'].astype(str).str.strip('[]').astype(float)
df['Delta_t_Degeri'] = df['Delta_t_Degeri'].astype(str).str.strip('[]').astype(float)


# DataFrame'i CSV dosyasına kaydetme
df.to_csv('degerler_hizlar_3.csv', index=False)

