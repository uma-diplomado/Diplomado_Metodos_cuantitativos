import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
df = pd.read_csv('https://www.quandl.com/api/v3/datasets/USTREASURY/YIELD.csv?api_key=1qqA2P4yyiY5bPaauktM',
                    index_col='Date')

df.index = pd.to_datetime(df.index)
df.drop('2 MO',axis = 1,inplace =True)
df = df.loc[df.index > '2016-01-01'].dropna()

covariance = np.cov(df, rowvar = False)

df.plot(title = 'Treasury Yield Curve Rates')

plt.show()

eigen_values, eigen_vectors= np.linalg.eig(covariance)

plt.plot(eigen_vectors[:,0:3])
plt.show()

means = np.array(df.mean(axis = 0))

X = df.sub(means)

Y = np.dot(X , eigen_vectors)
Y2 = Y.copy()
Y2[:,1] = Y2[:,1]*(-1)
pd.DataFrame(Y2[:,:3],index = df.index,columns=['PC 1','PC 2','PC 3']).plot()
plt.show()
Y_reduced = Y[:,:3]

A_reduced = eigen_vectors[:,:3]

A_reduced_transposed = A_reduced.transpose()

X1 = np.dot(Y_reduced, A_reduced_transposed)

dy = X1 + means
names =['approx '+i for i in df.columns]
estim = pd.DataFrame(dy,index = df.index,columns= names)
estim.plot()
plt.show()
