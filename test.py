import pandas as pd
import ta
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

#Header
st.write("""
# Simple Stock Price App
""")

#List of stocks
stock = ['ADA-USD','AAPL','FB','AMZN','ARKF','ORA.PA','BAYN.DE','MSFT','ARKK','T','VB','ACA.PA','SLV','VONG','ARKG','PM','BNGO','PFE','DAI.DE','REET']
#Selector of stock
choice_stock = st.sidebar.selectbox('Which stock do you want to select?', stock)
choice_ma = st.sidebar.slider('Pick a moving average in days',0,365,value=20)
choice_std = st.sidebar.slider('Pick a standard deviation',0,3, value = 2)

#TA part
chosen = yf.Ticker("{}".format(choice_stock)).history(period="12mo").reset_index()[["Date","Close"]]

bl = ta.volatility.BollingerBands(close=chosen["Close"], window=choice_ma, window_dev=choice_std)

chosen["hbl"] = bl.bollinger_hband()
chosen["mabl"] = bl.bollinger_mavg()
chosen["lbl"] =  bl.bollinger_lband()

#Graphing part
fig = px.line(x= chosen["Date"], y=[chosen["Close"],chosen["mabl"],chosen["hbl"],chosen["lbl"]],width=900, height=500)
fig.update_layout(title_text="Bollinger bands for {}".format(choice_stock),xaxis_title="Date",yaxis_title="Price")

st.plotly_chart(fig)