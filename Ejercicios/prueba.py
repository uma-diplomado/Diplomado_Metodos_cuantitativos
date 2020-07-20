import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

r = requests.get('https://www.banxico.org.mx/valores/PresentaDetallePosicionGub.faces?BMXC_instrumento=2&BMXC_lang=es_MX')

data = BeautifulSoup(r.text,'lxml')

trs_par = data.find_all('tr',{'class':'renglonPar'})
trs_non = data.find_all('tr',{'class':'renglonNon'})

l = []
for i in range(len(trs_par)):    
    l.append(trs_non[i].text.split('\n'))
    l.append(trs_par[i].text.split('\n'))
    

df = pd.DataFrame(l)
df.drop([0,16],axis = 1,inplace = True)

columnas = data.find_all('th',{'class':'titulos_tabla'})
df.columns = [i.text for i in columnas]
df.to_excel('datos.xlsx')
print('Terminado')
