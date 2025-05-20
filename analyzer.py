import pandas as pd
import numpy as np
import datetime
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from pyarrow.interchange.from_dataframe import column_to_array
from sklearn.preprocessing import StandardScaler
st.title("Stock Market Analyzer")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Read and display the file
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    data['Date'] = pd.to_datetime(data['Date'])

    data=data.dropna()
    data.set_index('Date', inplace=True)
    data['year']=data.index.year
    st.write("Preview of uploaded data:")
    st.dataframe(data.head())
    selected_column= st.selectbox("Select column", list(data.columns))

    date_range=st.date_input("Select start date",data.index.min())
    date_range=pd.to_datetime(date_range)
    today=st.date_input('select end date',datetime.date.today())
    today=pd.to_datetime(today)
    range_data=data[(data.index>=date_range) & (data.index<=today)]

    fig1,ax1=plt.subplots()
    ax1=sns.histplot(data=range_data, x=selected_column,kde=True,color='pink')
    fig2,ax2=plt.subplots()
    ax2=sns.lineplot(data=range_data,x=range_data.index,y=range_data[selected_column])
    fig3,ax3=plt.subplots()
    ax3=sns.boxplot(data=range_data,x=range_data[selected_column],color="green")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.pyplot(fig1)
        st.write("Distribution of"+" "+str(selected_column))
    with col2:
        st.pyplot(fig2)
        st.write("Treand of"+" "+str(selected_column))
    with col3:
        st.pyplot(fig3)
        st.write("Box plot"+" "+str(selected_column))

    st.write('Advanced Analysis')
    advanced_option=st.selectbox("Select advanced Analysis Options",("Moving Avreage",'Anomaly Detection','Volatality & Daliy Return Analysis'))
    if advanced_option=="Moving Avreage":
        st.number_input('select window size',min_value=20,max_value=365,placeholder="Enter window size",value=20,icon="🔥")
        fig4,ax4=plt.subplots()
        ax4 = sns.lineplot(data=range_data, x=range_data.index, y=range_data[selected_column])
        ax4=sns.lineplot(data=range_data,x=range_data.index,y=range_data[selected_column].rolling(window=20).mean(),color="red")

        st.pyplot(fig4)
    elif advanced_option=="Anomaly Detection":
        range_data['std']=(range_data[selected_column]-range_data[selected_column].mean())/(range_data[selected_column].std())
        treshhold1=2
        treshhold2=-2
        range_data['color'] = ''

        for i in range(len(range_data['std'])):
            if range_data['std'][i]>=treshhold1:
                range_data['color'][i]='above Anomaly'
            elif range_data['std'][i]<=treshhold2:
                range_data['color'][i]='lower Anomaly'
        fig5,ax5=plt.subplots()
        ax5=sns.lineplot(data=range_data, x=range_data.index, y='std')
        ax5=sns.scatterplot(x=range_data.index,y='std',hue='color',palette={'above Anomaly':'red', 'lower Anomaly':'yellow'},data=range_data)
        st.pyplot(fig5)
    elif advanced_option=="Volatality & Daliy Return Analysis":
        column=st.selectbox("Select column",('Adj Close',"Close"))
        range_data['Daliy return']=range_data[column].pct_change().dropna()
        fig6,ax6=plt.subplots()
        ax6=sns.lineplot(data=range_data, x=range_data.index, y='Daliy return')
        st.pyplot(fig6)
        daily_volatality=(range_data['Daliy return'].std())*100
        volatality=(range_data['Daliy return'].std()*np.sqrt(252))*100
        if daily_volatality>2:
           st.header(daily_volatality)

           st.markdown("<h3 style='color:red'>High Volatality </h3>", unsafe_allow_html=True)
        else:
            st.header(daily_volatality)
            st.markdown("<h3 style='color:green'>Moderate Volatality </h3>", unsafe_allow_html=True)
        if volatality>20:
            st.header(volatality)
            st.markdown("<h3 style='color:red'>High Annual Volatality </h3>", unsafe_allow_html=True)
        else:
            st.header(volatality)
            st.markdown("<h3 style='color:green'>Moderate Volatality </h3>", unsafe_allow_html=True)



else:
    st.warning("Please upload a CSV file to proceed.")

