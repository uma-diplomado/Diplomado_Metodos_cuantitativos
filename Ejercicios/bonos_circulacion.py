# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 09:02:46 2019

@author: MB50294
"""
import requests
import os
import xlrd 
import pandas as pd
import datetime  

proxy = 'http://MB50294:ener2020@150.216.245.17:80'
os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

fecha = datetime.datetime.strptime("01012015", "%d%m%Y")
l=[]

num_fechas = (datetime.datetime.today()-fecha).days
for i in range(num_fechas):
    print(i)
    fecha = fecha+datetime.timedelta(1)
    fecha_str= fecha.strftime("%d%m%Y")
    req = 'https://www.banxico.org.mx/valores/servletformato?fechaini=' + fecha_str + '&fechafin='+fecha_str+'&ins=TODOS&fechavto=&BMXC_claseIns=GUB&tipocons=1&BMXC_lang=es_MX'
    resp = requests.get(req)
    xlfile = xlrd.open_workbook(file_contents = resp.content)
    
    xl = pd.ExcelFile(xlfile)
    dfs = {fecha_str: xl.parse(sheet) for sheet in xl.sheet_names}
    l.append(dfs)
    fecha = datetime.datetime.strptime(fecha_str, "%d%m%Y")
