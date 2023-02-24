import pandas as pd
import plotly.express as px
import streamlit as st
import math
pd.set_option('display.max_columns', None)

# THIS FIRST STREAMLIT VERSION STOCK SCREENER


# set site config
st.set_page_config(page_title="Python Dashboard",
	page_icon=":bar_chart:",layout="wide")

country = st.sidebar.selectbox("Select the country:",["USA","POL","REST"])

	

# header
st.sidebar.header("Please Filter Here:")

caps= ['Nano Cap','Micro Cap', 'Small Cap', 'Mid Cap', 'Large Cap', "Mega Cap"]
def add_cap_size(row):
    if row["Market Cap (USD)"] <=50000000:
        val = caps[0]
    elif row["Market Cap (USD)"] <=300000000:
        val = caps[1]
    elif row["Market Cap (USD)"] <=2000000000:
        val = caps[2]
    elif row["Market Cap (USD)"] <=10000000000:
        val = caps[3]
    elif row["Market Cap (USD)"] <=200000000000:
        val = caps[4]
    else:
    	val = caps[5]
    return val

 # read data
path=f"data\\{country}.xlsx"


@st.cache_data
def get_data(path:str)->pd.DataFrame:

	df1=pd.read_excel(path, index_col=0, engine='openpyxl') 
	df1["Cap size"]= df1.apply(add_cap_size,axis=1)


	# print(df1.head(10))
	df1.fillna(0, inplace=True)
	return df1


df1 = get_data(path) 
higher_preferred=['Market Cap (USD)', 'EPS Average Estimated Annual Growth in Next 2 Years', 'Revenue Average Estimated Annual Growth in Next 2 Years', 'Book Value (Annual)', 'Upside for Next 12 Months', 'Price Target', 'Price Target Number Estimates',
			 'PE Ratio (Forward)', 'Altman Z Score (Annual)', 'Piotroski F Score (Annual)', 
			  'Retained Earnings (TTM)', 'Return on Assets (TTM)', 'Return on Equity (TTM)',
			   'Return on Invested Capital (TTM)',  'PS Ratio (Forward)', 'Revenue (TTM)', 'Revenue Estimates for Next 12 Months', 'Revenue Estimates for 2 Fiscal Years Ahead', 'EPS Basic (TTM)', 'EPS Estimates for Next Fiscal Year', 'EPS Number Estimates for 2 Fiscal Years Ahead', 'EPS Long Term (5 Years) Growth Estimates']

lower_preferred=['PE Ratio','Price to Book Value','Price','PS Ratio','Debt to Assets (Annual)','Total Debt (TTM)']


try:
	sector = st.sidebar.multiselect(
		"Select the sector:",
		options=df1["Sector"].unique()
		)
	if sector:
		industry = st.sidebar.multiselect(
		"Select the industry:",
		options=df1[df1["Sector"].isin(sector)]["Industry"].unique()
		)
	else:
		industry = st.sidebar.multiselect(
		"Select the industry:",
		options=df1["Industry"].unique()
		)
	
	
	cap_size = st.sidebar.multiselect(
		"Select a range of Market Cap",
		options=caps,
		default=['Mega Cap'],
		help ="**Nano Cap<50million \n <Micro Cap<300million <Small Cap< 2billion<Mid Cap< 10billion<Large Cap <200billion <Mega cap**\n"
		)

	
	filters =  st.sidebar.multiselect(
		"Select the columns filter:",
		options=df1.columns.tolist()[1:-1]
		)
	filter_checkbox = st.sidebar.checkbox('Show only filtered columns')
	name = st.sidebar.text_input(
		"Select the company name:",
		placeholder="apple"
		)

	
	
except Exception as e:
	pass

finally:
	if sector:
		df1=df1.query("Sector in @sector")
	if industry:
		df1=df1.query("Industry in @industry")
	if cap_size:
		df1=df1.query("`Cap size` in @cap_size")	
	if filters:
		for x in filters:
			if x in lower_preferred:
				x_filter = st.sidebar.text_input(
				x+"<...",
				placeholder="lower than"
				)
				if x_filter:
					df1=df1.query(f"`{x}` <= {x_filter}")
			elif x in higher_preferred:
				x_filter = st.sidebar.text_input(
				x+">...",
				placeholder="higher than"
				)
				if x_filter:
					df1=df1.query(f"`{x}` >= {x_filter}")
		if filter_checkbox:
			df2=df1.iloc[:,:1]
			df1=pd.concat([df2, df1.loc[:,filters]], axis=1)
	if name:
		df1=df1.query("`Company Name`.str.lower().str.contains(@name)")



st.dataframe(df1)