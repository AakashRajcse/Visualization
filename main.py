import  pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title = 'Adidas Sales',
                  page_icon = "C:/Users/hp/Downloads/Adidas-1.csv",
                  layout = 'wide')

st.title("Adidas Sales Dashboard")

# load the data
df = pd.read_csv("Adidas-1.csv")

df['Invoice Date'] = pd.to_datetime(df['Invoice Date'])
#df = df.sort_values(by = 'Invoice Date')
#st.dataframe(df)

#Filter users
retailer_fil = st.sidebar.multiselect('Retailer', df['Retailer'].unique(), df['Retailer'].unique())
region_fil = st.sidebar.multiselect('Region', df['Region'].unique(), df['Region'].unique())
state_fil = st.sidebar.multiselect('State', df['State'].unique(), df['State'].unique())
city_fil = st.sidebar.multiselect('City', df['City'].unique(), df['City'].unique())
product_fil = st.sidebar.multiselect('Product', df['Product'].unique(), df['Product'].unique())
df= df.loc[(df['Retailer'].isin(retailer_fil)) & (df['Region'].isin(region_fil)) & (df['State'].isin(state_fil)) & (df['City'].isin(city_fil)) & (df['Product'].isin(product_fil))]
st.dataframe(df)

#Key Metrics
with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", df["Retailer"].count())
    col2.metric("Total Units", df["Units Sold"].sum())
    col3.metric("Total Profit", df["Operating Profit"].sum().round().astype(int))
    col4.metric("Average Margin", df["Operating Margin"].mean().round(1))

#Repeat Customer Analysis
col1, col2 = st.columns(2)
with col1:
    retailer_count = df["Retailer"].value_counts().reset_index()
    # st.dataframe(retailer_count)
    fig = px.pie(data_frame=retailer_count, names='Retailer', values='count')
    st.plotly_chart(fig)

#Product wise total Profit
with col2:
    product_profit = df.groupby("Product")["Operating Profit"].sum().reset_index().sort_values("Operating Profit", ascending=False)
    #st.dataframe(product_profit)
    product_profit = product_profit.round()
    fig = px.bar(data_frame=product_profit, x="Product", y = "Operating Profit", text="Operating Profit")
    st.plotly_chart(fig)


col1, col2 = st.columns(2)
with col2:
    date_profit = df.groupby("Product")['Operating Profit'].mean().reset_index()
    st.dataframe(date_profit)

with col2:
    fig = px.line(data_frame=date_profit, x='Invoice Date', y = 'Operating Profit')
    st.plotly_chart(fig)


