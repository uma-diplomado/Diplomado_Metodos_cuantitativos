# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 11:35:36 2019

@author: MB50294
"""

import requests
from bs4 import BeautifulSoup
 
req = requests.get('http://www.anterior.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=7&accion=consultarCuadro&idCuadro=CF478&locale=es#')
soup = BeautifulSoup(req.text, "lxml")

for sub_heading in soup.find_all('input'):
    if 'name' in sub_heading.attrs.keys():
        if sub_heading['name'] == "series":
            print(sub_heading['value'])
    