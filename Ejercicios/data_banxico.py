# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:47:25 2020

@author: Claudio Cuevas
"""
import requests
import pandas as pd
import functools

def request_banxico(token, instrumentos,fecha_inicio,fecha_final):
    '''
    Creates a Request to the Banxico Economic Information System (SIE).
    Arguments:
        token:  necessary for autentication in the platform, it is possible to 
                generate one on the following link:
                https://www.banxico.org.mx/SieAPIRest/service/v1/
        ibnstruments: list of instrument codes necessary.
                      example: intrument CETES 28d, instrument code: SF282.
                      see https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries#
        fecha_inicio: start date for time series, format 'Y-m-d'
        fecha_final: end date for time series, format 'Y-m-d'
    '''
    for ins in instrumentos:                
    print(ins)
    peticion = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/' + \
                         ins + '/datos/' + fecha_inicio + '/' + \
                         fecha_final + '?token=' + token
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