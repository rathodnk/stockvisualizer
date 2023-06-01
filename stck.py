import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys

st.markdown("<h1 style='text-align: center'>Stock Visualization & Analysis</h1>", unsafe_allow_html = True)

ticker = st.sidebar.text_input("Ticker")
strt_d = st.sidebar.date_input("Start Date")
end_d = st.sidebar.date_input("End Date")

try:
    data = yf.download(ticker, start=strt_d, end=end_d)
    if data is not None and not data.empty:
        data['Change'] = data['Adj Close']/data['Adj Close'].shift(1) - 1
    else:
        st.warning(
            f"No data available for {ticker} between {strt_d} and {end_d}. Please select a different date range or ticker.")
        sys.exit()
except ValueError:
    st.warning(f"Please select a ticker.")
    sys.exit()
    
da2 = data.copy()
da2.dropna(inplace=True)

infm, dexan, vsl, anls, nws = st.tabs(
    ["INFO", "Data", "Visualization", "Analysis", 'Top News'])

with infm:
    tic = yf.Ticker(ticker)
    tick = tic.info
    st.markdown(f"<h2>{tick['longName']}</h2>", unsafe_allow_html= True)
    st.write(f"Country: {tick['country']}")
    st.write(f"Sector: {tick['sector']}")
    st.write(f"Industry: {tick['industry']}")
    st.write(f"Financial Currency: {tick['financialCurrency']}")
    st.write(f"Time Zone: {tick['timeZoneShortName']}")
    st.write(f"Market Cap: {tick['marketCap']}")
    st.markdown(f"{tick['website']}")

    # st.write(tick)


with dexan:
    st.markdown(f'<h2>{ticker} Data</h2>', unsafe_allow_html= True)
    st.write(data)

    desc, cor, rslt = st.tabs(["Description", "Correlation", "Result"])

    with desc:
        st.markdown("<h3>Data Description</h3>", unsafe_allow_html=True)
        st.write(data.describe())

    with cor:
        st.markdown('<h3>Data Correlation</h3>', unsafe_allow_html=True)
        st.write(data.corr())

    with rslt:
        st.markdown(f"<h3>Results for {ticker} between {strt_d} to {end_d}</h3>", unsafe_allow_html= True)

        da2_copy = data.copy()
        da2_copy.reset_index(inplace=True)

        try:
            d1 = {
                'Features': [
                    'open_max',
                    'open_min',
                    'high_max',
                    'high_min',
                    'low_max',
                    'low_min',
                    'close_max',
                    'close_min',
                    'adj_close_max',
                    'adj_close_min',
                    'change_max',
                    'change_min'
                ],
                'Values': [
                    da2_copy['Open'].max(),
                    da2_copy['Open'].min(),
                    da2_copy['High'].max(),
                    da2_copy['High'].min(),
                    da2_copy['Low'].max(),
                    da2_copy['Low'].min(),
                    da2_copy['Close'].max(),
                    da2_copy['Close'].min(),
                    da2_copy['Adj Close'].max(),
                    da2_copy['Adj Close'].min(),
                    da2_copy['Change'].max(),
                    da2_copy['Change'].min()
                ],
                'Date': [
                    da2_copy.loc[da2_copy['Open'].idxmax(), 'Date'],
                    da2_copy.loc[da2_copy['Open'].idxmin(), 'Date'],
                    da2_copy.loc[da2_copy['High'].idxmax(), 'Date'],
                    da2_copy.loc[da2_copy['High'].idxmin(), 'Date'],
                    da2_copy.loc[da2_copy['Low'].idxmax(), 'Date'],
                    da2_copy.loc[da2_copy['Low'].idxmin(), 'Date'],
                    da2_copy.loc[da2_copy['Close'].idxmax(), 'Date'],
                    da2_copy.loc[da2_copy['Close'].idxmin(), 'Date'],
                    da2_copy.loc[da2_copy['Adj Close'].idxmax(), 'Date'],
                    da2_copy.loc[da2_copy['Adj Close'].idxmin(), 'Date'],
                    da2_copy.loc[da2_copy['Change'].idxmax(), 'Date'],
                    da2_copy.loc[da2_copy['Change'].idxmin(), 'Date']
                ]
            }

            st.markdown('<h4>Resultant Table</h4>', unsafe_allow_html=True)
            st.write(pd.DataFrame(d1))

            retn = da2['Change'].mean()*da2['Change'].count()*100
            st.markdown(f"<h4><b>Total Return: {round(retn,2)}%</b></h4>", unsafe_allow_html=True)

            stdv = np.std(da2['Change'])*np.sqrt(da2['Change'].count())
            st.write(f"Standard Deviation: {round(stdv,4)}")

            rck = round(retn/(stdv*100), 4)
            st.write(f"Rick Return: {rck}")
        except KeyError:
            st.warning('')

with vsl:
    st.header(f"{ticker} Visualization")


    try:
        li = ['Open', 'High', 'Low', 'Close', 'Adj Close']

        sel = st.multiselect(label='Select', options=li, default='Adj Close')
        lnc = px.line(data, x=data.index, y=sel, title='Line Chart')
        st.plotly_chart(lnc)
    
    except ValueError:
        st.warning('')
        sys.exit()

    color_map = {'Negative': 'red', 'Positive': 'green'}
    catg = pd.cut(da2['Change'], bins=[-np.inf, 0, np.inf],
                    labels=['Negative', 'Positive'])
    brc = px.bar(
        da2, x=da2.index, y=da2['Change'], title='Bar Chart for Change', color=catg, color_discrete_map=color_map)
    st.plotly_chart(brc)

    st.write('Scatter Plot')
    c1, c2 = st.columns(2)
    with c1:
        xax = st.selectbox(label='X-axis', options=li, index=1)
    with c2:
        yax = st.selectbox(label='Y-axis', options=li, index=2)

    scp = px.scatter(data, x=xax, y=yax, title='Comparing')
    st.plotly_chart(scp)

    boc = px.box(data, y=['Open', 'High', 'Low', 'Close'], title='Box Chart')
    st.plotly_chart(boc)
    
    jbr = go.Figure(data = [
        go.Bar(name = 'MaxValue', x = ['Open', 'High', 'Low', 'Close', 'Adj Close'], y=[
            d1['Values'][0],
            d1['Values'][2],
            d1['Values'][4],
            d1['Values'][6],
            d1['Values'][8]]),
        go.Bar(name = 'MinValue', x = ['Open', 'High', 'Low', 'Close', 'Adj Close'], y=[
            d1['Values'][1],
            d1['Values'][3],
            d1['Values'][5],
            d1['Values'][7],
            d1['Values'][9]
        ])
    ])
    st.plotly_chart(jbr)
    
with anls:
    st.subheader("Technical Indicator Analysis")
    d2 = pd.DataFrame()
    l1 = d2.ta.indicators(as_list=True)
    lm = ['ema','stoch','aroon','bbands','rsi','aberration']
    techin = st.selectbox('Technical Indicator', options=l1, index=41)
    method = techin
    indicator = pd.DataFrame(getattr(ta, method)(
        open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], volume=data['Volume']))
    indicator['Close'] = data['Adj Close']

    fig = px.line(indicator)
    st.plotly_chart(fig)
    st.write(indicator)


###with fund_d:
    ###st.header('Fundamental Data')

    ###balance_sheet = tic.balance_sheet
    ###quarterly_balance_sheet = balance_sheet.iloc[:, :4]
    ###st.write(pd.DataFrame(quarterly_balance_sheet))


with nws:
    ticnews = tic.news
    i = 1
    for news in ticnews:
        st.write(f"#{i}. {news['title']}")
        st.markdown(f'{news["link"]}')
        st.write(f'\n')
        i = i + 1
