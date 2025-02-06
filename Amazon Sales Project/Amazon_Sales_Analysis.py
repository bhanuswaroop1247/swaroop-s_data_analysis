# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 18:12:06 2025

@author: 91984
"""

import pandas as pd

#Load the sales data from the excel file into a pandas DataDrame

sales_data=pd.read_excel('C:/Users/91984/Documents/Python for Data Analysis Udemy/Amazon Sales Project/sales_data.xlsx')

# =============================================================================
# Explorng the Data
# =============================================================================

#Get a Summary of Sales Date
sales_data.info() #Can also check data types
sales_data.describe()

#looking at columns
print(sales_data.columns)

#Having a look at the first few rows of the data
print(sales_data.head())

#Check the Data Types of the columns
print(sales_data.dtypes)

# =============================================================================
# Cleaning the Data
# =============================================================================

#Check for missing values in our sales data
sales_data.isnull().sum()


#Drop any rows that has any missing/nan values
sales_data_dropped=sales_data.dropna()


#Drop rows with missing amounts based on the amount column
sales_data_cleaned=sales_data.dropna(subset=["Amount"])

#Check for missing values in our sales data
print(sales_data_cleaned.isnull().sum())


# =============================================================================
# Slicing and filtering the data
# =============================================================================
category_data=sales_data[sales_data['Category']=='Top']
print(category_data)

#select a subset of our data based on the category column
high_amount_data=sales_data[sales_data['Amount']>1000]
print(high_amount_data)

#Select a subset of data based on the multiple conditions
filtered_data=sales_data[(sales_data['Category']=='Top')&(sales_data['Qty'])==3]
print(filtered_data)

# =============================================================================
# Aggregating data
# =============================================================================

#total sales by category
category_totals = sales_data.groupby('Category')['Amount'].sum()
print(category_totals)
category_totals= sales_data.groupby('Category',as_index=False)['Amount'].sum()
category_totals=category_totals.sort_values('Amount',ascending=False)

# Calculate the Average Amount by Category and Fulfillment

fulfilment_averages = sales_data.groupby(['Category','Fulfilment'],as_index=False)['Amount'].mean()
fulfilment_averages=fulfilment_averages.sort_values('Amount',ascending=False)

# Calculate the Average Amount by Category and Status

status_averages = sales_data.groupby(['Category','Status'],as_index=False)['Amount'].mean()
status_averages=fulfilment_averages.sort_values('Amount',ascending=False)

#Total Sales by Shipment and Fulfiment
total_sales_shipandfufil = sales_data.groupby(['Courier Status','Fulfilment'],as_index=False)['Amount'].sum()
total_sales_shipandfufil=total_sales_shipandfufil.sort_values('Amount',ascending=False)
total_sales_shipandfufil.rename(columns={'Courier Status': 'Shipment'},inplace=True)
# =============================================================================
# Exporting the data
# =============================================================================

status_averages.to_excel('average_sales_by_category_and_sales.xlsx',index=False)
total_sales_shipandfufil.to_excel('total_sales_by_ship_and_fulfilment.xlsx',index=False)






























