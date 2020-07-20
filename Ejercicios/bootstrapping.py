import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


#Convención Actual 360
def delta(t1,t2):
    return((t2-t1).days/360)

class DISC_Curve:
    def __init__(self,_spot_date,_zeros,_mat):
        self.spot_date=_spot_date
        self.zeros=_zeros
        self.mat=_mat
        self.tenors= [delta(spot_date,i) for i in _mat]
        self.libors=[((1/pv)-1)/t for (pv,t) in zip(_zeros,self.tenors)]
        
    def get_zero(self,maturity):
        t=delta(self.spot_date,maturity)
        l=np.interp(t,self.tenors,self.libors)
        return(1/(1+l*t))
    
    def get_libor(self,maturity):
        t=delta(self.spot_date,maturity)
        return(np.interp(t,self.tenors,self.libors))
    
    def set_node(self,zero, mat_date):
        self.zeros.append(zero)
        self.mat.append(mat_date)
        tenor=delta(self.spot_date,mat_date)
        self.tenors.append(tenor)
        self.libors.append(((1/zero)-1)/tenor)
    
    def get_fwd(self,reset_date,maturity_date):
        return(((self.get_zero(reset_date)/self.get_zero(maturity_date))-1)/delta(reset_date,maturity_date))
        
if __name__ == '__main__':

    #Load data
    mkt_data=pd.read_csv('prueba.csv')
    
    pmts=pd.read_csv('pagos instrumentos.csv')
    
    spot_date=pd.to_datetime('03/10/2012',format='%d/%m/%Y')
    
    mkt_data['Maturity Dates']=pd.to_datetime(mkt_data['Maturity Dates'],format='%d/%m/%Y')
    
    pmts.Tenor=pd.to_datetime(pmts.Tenor,format='%d/%m/%Y')

    LIBORS=mkt_data.loc[mkt_data.Source=="LIBOR"]
    
    FUTURES=mkt_data.loc[mkt_data.Source=="Futures"]
    
    SWAPS=mkt_data.loc[mkt_data.Source=="Swap"]

    MAT=[i for i in LIBORS['Maturity Dates']]
    
    #Obtener los factores de descuento a partir de las cotizaciones de tasas ZC
    DF=[1/(1+delta(spot_date,i)*j/100) for (i,j) in zip(LIBORS['Maturity Dates'],LIBORS['Market Quotes'])]

    disc_factor=DISC_Curve(spot_date,DF,MAT)

    S=list(pmts.Tenor.loc[pmts.Instrument=='FUT'])
    
    #Obtener los factores de descuento a partir de precios de futuros
    for i in range(len(S)-1):
        t=delta(S[i],S[i+1])
        df=disc_factor.get_zero(S[i])/(1+(1-list(FUTURES['Market Quotes'])[i]/100)*t)
        disc_factor.set_node(df,S[i+1])

    #Cotizaciones de tasas swap
    U=list(pmts.Tenor.loc[pmts.Instrument=='SWAP'])

    swap_mkt_tenor=[delta(spot_date,i) for i in list(SWAPS['Maturity Dates'])]
    
    #Una forma para resolver este problema es interpolar las tasas swap y obtener una 
    #Tasa swap para cada periodo de pago de cupón
    sw=[]    
    for i in range(len(U)):
        sw.append(np.interp(delta(spot_date,U[i]),
                  swap_mkt_tenor,
                  list(SWAPS['Market Quotes']))/100)

    U.insert(0,spot_date)
    
    sw.insert(0,0)

    factor=0
    for n in range(2,len(U)):    
        factor+=disc_factor.get_zero(U[n-1])*delta(U[n-2],U[n-1])
        df=(1-sw[n]*factor)/(1+sw[n]*delta(U[n-1],U[n]))
        disc_factor.set_node(df,U[n])
        
    plt.plot(disc_factor.mat,disc_factor.zeros,'b.-')
    plt.show()