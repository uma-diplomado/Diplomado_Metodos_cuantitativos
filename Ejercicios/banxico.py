# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 11:35:28 2019

@author: MB50294
"""

import requests
import os
import pandas as pd
import functools
from bs4 import BeautifulSoup

def comma_to_float(x):
    return float(x.replace(',', ''))

proxy = 'http://MB50294:febr2020@150.216.245.17:80'
os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

req = requests.get('http://www.anterior.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=7&accion=consultarCuadro&idCuadro=CF478&locale=es#')
soup = BeautifulSoup(req.text, "lxml")
token =  'c7d71fa11b9e18e8905289e4a36fb75f3f298d7bce99156d3b00c4a274b15046'
inicio = '2011-05-01'
final = '2019-12-20'
instrumentos = []
resultado = []
for sub_heading in soup.find_all('input'):
    if 'name' in sub_heading.attrs.keys():
        if sub_heading['name'] == "series":
            instrumentos.append(sub_heading['value'])

for ins in instrumentos:                
    print(ins)
    peticion = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/' + \
                         ins + '/datos/'+inicio+'/'+final+'?token=' + token
    response = requests.get(peticion)

    datos = response.json()['bmx']['series']
    
    for i in datos:
        temp = pd.DataFrame(i['datos'])
        temp.set_index('fecha',inplace = True)
        temp.index = pd.to_datetime(temp.index,dayfirst=True)
        temp.columns = [i['titulo']]
        resultado.append(temp)
        
dfList = functools.reduce(lambda x, y: pd.merge(x, y, 
                                                left_index=True, 
                                                right_index=True,
                                                how ='outer'),resultado)

dfList = dfList.applymap(comma_to_float)

