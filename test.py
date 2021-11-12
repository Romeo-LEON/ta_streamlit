import pandas as pd
import ta
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit as st

#Header
st.write("""
# Simple Stock Price App 🦆
""")

#List of stocks
stock = ['ADA-USD','AAPL','FB','AMZN','ARKF','ORA.PA','BAYN.DE','MSFT','ARKK','T','VB','ACA.PA','SLV','VONG','ARKG','PM','BNGO','PFE','DAI.DE','REET']
#Selector of stock
choice_stock = st.sidebar.selectbox('Which stock do you want to select?', stock)
choice_ma = st.sidebar.slider('Pick a moving average in days',0,365,value=20)
choice_std = st.sidebar.slider('Pick a standard deviation',0,3, value = 2)

###TA part

#Define ticker
chosen = yf.Ticker("{}".format(choice_stock)).history(period="max").reset_index()[["Date","Close"]]

#Create BollingerBands
bl = ta.volatility.BollingerBands(close=chosen["Close"], window=choice_ma, window_dev=choice_std)

chosen["hbl"] = bl.bollinger_hband()
chosen["mabl"] = bl.bollinger_mavg()
chosen["lbl"] =  bl.bollinger_lband()

#Define returns
chosen['Return'] = 100 * (chosen['Close'].pct_change())

#Define buy / sell signals
buy = []
sell = []

for i in range(len(chosen['Close'])):
    if chosen['Close'][i] > chosen['hbl'][i]:
        buy.append(np.nan)
        sell.append(chosen['Close'][i])
    elif chosen['Close'][i] < chosen['lbl'][i]:
        buy.append(chosen['Close'][i])
        sell.append(np.nan)
    else:
        buy.append(np.nan)
        sell.append(np.nan)

chosen['buy'] = buy
chosen['sell'] = sell

#Graphs the close and moving average
fig = px.line(x= chosen["Date"], y=[chosen["Close"],chosen["mabl"]],width=900, height=600)
fig.update_layout(title_text="Bollinger bands for {}".format(choice_stock),xaxis_title="Date",yaxis_title="Price")

#Graph upper Bound
fig.add_trace(go.Scatter(x = chosen['Date'],
                         y = chosen['hbl'],
                         line_color = 'gray',
                         line = {'dash': 'dash'},
                         name = 'upper band',
                         opacity = 0.5),
              row = 1, col = 1)

# Lower Bound fill in between with parameter 'fill': 'tonexty'
fig.add_trace(go.Scatter(x = chosen['Date'],
                         y = chosen['lbl'],
                         line_color = 'gray',
                         line = {'dash': 'dash'},
                         fill = 'tonexty',
                         name = 'lower band',
                         opacity = 0.5),
              row = 1, col = 1)

#Add trading signals
fig.add_trace(go.Scatter(x = chosen['Date'],
                         y = chosen['buy'],
                         line_color = '#49FF00',
                         mode ='markers',
                         marker_symbol = 'triangle-up',
                         opacity = 1,
                         name = 'buy'))

fig.add_trace(go.Scatter(x = chosen['Date'],
                         y = chosen['sell'],
                         line_color = '#FF9300',
                         mode ='markers',
                         marker_symbol = 'triangle-down',
                         opacity = 1,
                         name = 'sell'))


#Update variable names
newnames = {
   'wide_variable_0': 'Value',
   'wide_variable_1': '{} days MA'.format(choice_ma),
   'upper band': 'Upper band',
   'lower band': 'Lower band',
   'buy': 'Buy',
   'sell': 'Sell'
}
fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
   legendgroup = newnames[t.name]
))

#Update trading signal size
fig.update_traces(marker_size = 8)

# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)


st.plotly_chart(fig)

daily_volatility = chosen['Return'].std()

volatility =  round(np.sqrt(21) * daily_volatility,2)

st.write(""" 
### Monthly volatility of {} is {}%""".format(choice_stock,volatility))

fig2 = px.line(x= chosen["Date"], y=chosen["Return"],width=900, height=600)
fig2.update_layout(title_text="Daily return of {}".format(choice_stock),xaxis_title="Date",yaxis_title="Change in %")

fig2.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

st.plotly_chart(fig2)
