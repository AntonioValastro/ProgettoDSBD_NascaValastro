import matplotlib.pyplot as plt 
import numpy as np, pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing



df = pd.read_csv("./post.csv", sep=";", header=0, parse_dates=[1], index_col=[1])
tsr = df.resample(rule="0.25T").mean()

print(tsr.info())
print(tsr.describe())
print(tsr)

tsr_rol = tsr.rolling(window=5).mean()
tsr_rol = tsr_rol.shift(-5)
tsr_rol = tsr_rol[:-5]
#print(tsr_rol.info())
train_data = tsr_rol[:75]
train_data2 = tsr_rol[:76]
test_data = tsr_rol[75:78]

tsr_sea_dec = seasonal_decompose(train_data, model='add', period=28)
tsr_sea_dec.plot()


# Original Series

tsmodel = ExponentialSmoothing(train_data, trend='add', seasonal='add', seasonal_periods=28).fit()
prediction = tsmodel.forecast(3)
plt.figure(figsize=(24,10), dpi=100)
plt.ylabel('Values',fontsize=14)
plt.xlabel('Time',fontsize=14)
plt.plot(train_data2,"-", label="Train Data", color="blue")
plt.plot(test_data,"--", label="Test Data", color="green")
plt.plot(prediction,"-", label="Prediction", color="red")
plt.title("Test Prediction")
plt.legend(title='Legend', fontsize=12)

# Future Series
tsmodel = ExponentialSmoothing(tsr_rol, trend='add', seasonal='add', seasonal_periods=28).fit()
prediction = tsmodel.forecast(3)
plt.figure(figsize=(24,10), dpi=100)
plt.ylabel('Values',fontsize=14)
plt.xlabel('Time',fontsize=14)
plt.plot(tsr_rol,"-", label="Train Data", color="blue")
plt.plot(prediction,"-", label="Prediction", color="red")
plt.title("Future Prediction")
plt.legend(title='Legend', fontsize=12)
plt.show()