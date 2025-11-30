import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
import seaborn as sns
from pmdarima import auto_arima

plt.style.use('dark_background')


df = pd.read_csv('C:\\Users\\vashi\\OneDrive\\Desktop\\Nat_Gas.csv', parse_dates=['Dates'],date_format="%Y-%m-%d")
df['Dates'] =pd.to_datetime(df['Dates'],format='%m/%d/%y')
df = df.sort_values('Dates').reset_index(drop=True)
print(df.head())
#===============================================================================================
#Stationarity checks
#===============================================================================================
def adf_test(series):
    result = adfuller(series)
    print(f"ADF p-value : {result[1]:.6f}")
    if result[1]<0.05:
        print("Stationary")
    else:
        print("Non-Stationary")

print("\n ADF Test on raw data:")
adf_test(df['Prices'])

df['SMA'] = df['Prices'].rolling(5).mean()

plt.figure(figsize=(10,4))
plt.plot(df['Dates'],df['Prices'], label ='Price')
plt.plot(df['Dates'],df['SMA'],label='5-Day SMA')
plt.legend();plt.grid(True, linestyle='-',alpha=0.5)
plt.title('Natural Gas Prices')
plt.show()

df['Log'] = np.log(df['Prices'])

plt.figure(figsize=(10,4))
plt.plot(df['Dates'],df['Log'])
plt.title('Log Prices')
plt.grid(True, linestyle='-',alpha=0.5)
plt.show()

plot_acf(df['Prices'])
plt.show()
plot_pacf(df['Prices'])
plt.show()

#===========================================================================================================
#Differencing
#============================================================================================================

df['Diff'] =df['Prices'].diff()
df_diff = df.dropna()

print("\n ADF Test on differenced data: ")
adf_test(df_diff['Diff'])

plt.figure(figsize=(10,4))
plt.plot( df_diff['Dates'],df_diff['Diff'])
plt.title("Differenced Series")
plt.grid(True, linestyle='-',alpha=0.5)
plt.show()


plot_acf(df_diff['Diff'])
plt.show()
plot_pacf(df_diff['Diff'])
plt.show()
#===============================================================================================================
#Fit SARIMAX
#====================================================================================================

print("\n Running Auto-ARIMA...")
model = auto_arima(
    df['Prices'],
    d=1,
    D=1,
    m=12,
    seasonal=True,
    start_p=0, max_p=5,
    start_q=0, max_q=5,
    start_P=0, max_P=5,
    start_Q=0, max_Q=5,
    trace =True,
    stepwise=True,
    suppress_warnings=True,
    error_action='ignore'
)
print("\n Auto-ARIMA SUMMARY:")
print(model.summary())
order = model.order
seasonal_order =model.seasonal_order

sarimax_model =SARIMAX(
    df['Prices'],
    order= order,
    seasonal_order=seasonal_order,
    enforce_stationarity=False,
    enforce_invertibility=False
).fit()

print("\n SARIMAX SUMMARY:")
print(sarimax_model.summary())

#===============================================================================================================
#Forecasting
#===============================================================================================================

n_forecast =12
forecast= sarimax_model.get_forecast(steps = n_forecast)
mean_forecast = forecast.predicted_mean
ci = forecast.conf_int()

future_dates=pd.date_range(df['Dates'].iloc[-1], periods=n_forecast+1,freq='M')[1:]

plt.figure(figsize=(12,5))
plt.plot(df['Dates'],df['Prices'], label ='Historical')
plt.plot(future_dates,mean_forecast,label='Forecast')
plt.fill_between(
    future_dates,
    ci.iloc[:,0],
    ci.iloc[:,1],
    alpha =0.3,
    label= 'Confidence Interval'
)
plt.legend();plt.grid(True, linestyle='--',alpha=0.5)
plt.title("12-Month Forecast - Natural Gas Prices")
plt.show()