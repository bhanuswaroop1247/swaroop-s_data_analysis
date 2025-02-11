# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:01:51 2025

@author: 91984
"""


import pandas as pd
from datetime import datetime
#Read the excel files

pizza_sales_df=pd.read_excel('pizza_sales.xlsx')
pizza_size_df=pd.read_csv('pizza_size.csv')
pizza_category_df = pd.read_csv('pizza_category.csv')

#Viewing top and bottom rows in a dataframe
pizza_sales_df.tail()
pizza_sales_df.head(10)

#Describing the data
pizza_sales_df.describe()
pizza_description=pizza_sales_df.describe()

# Have a look at non null counts per column
pizza_sales_df.info()

#Count the nu,ber of null values in each columns
null_count = pizza_sales_df.isnull().sum()

# Check for Duplicated rows
duplicted_rows = pizza_sales_df.duplicated().sum()
print(duplicted_rows)

#To select a column
quantity_column = pizza_sales_df['quantity']
selected_columns = pizza_sales_df[['order_id','quantity','unit_price']]

#Get the row with index label 3
row = pizza_sales_df.loc[3]

#Get two rows,index label 3 and 5
rows=pizza_sales_df.loc[[3,5]]


#get rows between index labels 3 and 5 and specific columns
subset = pizza_size_df.loc[3:5]

# Get rows between index labels 3 and 5 and specific columns
subset = pizza_sales_df.loc[3:5,['quantity','unit_price']]

# Set an Index as a column is a dataframe
pizza_sales_df.set_index('order_details_id',inplace=True)

#Resetting am Index
pizza_sales_df.reset_index(inplace=True)

#Truncate DataFrame before index 3
truncated_before = pizza_sales_df.truncate(before=3)

#Truncate data frame after index 5
truncated_after = pizza_sales_df.truncate(after=5)

#Truncating Columns
quantity_series = pizza_sales_df['quantity']

# Truncate series before index 3
truncated_series_before = quantity_series.truncate(before=3)

# Truncate series after index 5
truncated_series_after = quantity_series.truncate(after=5)

#Basic Filtering
filtered_rows = pizza_sales_df[pizza_sales_df['unit_price'] > 20]

# Filtering on Dates
#pizza_sales_df['order_date']=pizza_sales_df['order_date'].dt.date


# Convert 'order_date' column to datetime format
pizza_sales_df['order_date'] = pd.to_datetime(pizza_sales_df['order_date'])

# Now, extract only the date part
pizza_sales_df['order_date'] = pizza_sales_df['order_date'].dt.date

date_target = datetime.strptime('2015-12-15', '%Y-%m-%d').date()
filtered_rows_by_date = pizza_sales_df[pizza_sales_df['order_date']>date_target]

#Filtering on multiple conditions
#using the and conditions
bbq_chicken_rows= pizza_sales_df[(pizza_sales_df['unit_price'] > 15) & (pizza_sales_df['pizza_name']=='The Barbecue Chicken Pizza')]

# Using the or condition |
bbq_chicken_rows_or = pizza_sales_df[(pizza_sales_df['unit_price'] > 20) | (pizza_sales_df['pizza_name']=='The Barbecue Chicken Pizza')]

# Filter a specific range
high_sales = pizza_sales_df[(pizza_sales_df['unit_price']>15) & (pizza_sales_df['unit_price']<=20)] 

# Dropping Null values
pizza_sales_null_values_dropped = pizza_sales_df.dropna()

# Repalce nulls with a value
date_na_fill = datetime.strptime('2001-01-01', '%Y-%m-%d').date()
pizza_sales_null_replaced = pizza_sales_df.fillna(date_na_fill)

# Deletying Specific Rows and Columns in a DataFrame
filtered_rows_2 = pizza_sales_df.drop(2,axis=0)

# Deleting rows 5,7,9 
filtered_rows_5_7_9 = pizza_sales_df.drop([5,7,9], axis = 0)

# Delete a column by column name 
filtered_unit_price = pizza_sales_df.drop('unit_price',axis = 1)

# Delete mutiple columns
filtered_unit_price_and_order_id = pizza_sales_df.drop(['unit_price','order_id'],axis =1)

# Sorting a Data Frame in Pandas

#Sorting in ascending order
sorted_df= pizza_sales_df.sort_values('total_price')

#sorting in descending order
sorted_df = pizza_sales_df.sort_values('total_price',ascending = False)

# Sort by multiple columns
sorted_df = pizza_sales_df.sort_values(['pizza_category_id','total_price'],ascending = [True,False])

# group by pizza size id and get the count of sales(row count)
grouped_df_pizza_size = pizza_sales_df.groupby(['pizza_size_id']).count()

# Group by pizza sze id and get the sum
grouped_df_pizza_size_by_sum = pizza_sales_df.groupby(['pizza_size_id'])['total_price'].sum()

# group by pizza size id and sum tottal price and quantity
grouped_df_pizza_size_sales_qauntity = pizza_sales_df.groupby(['pizza_size_id'])[['total_price','quantity']].sum()

# looking at differeny aggregation functions
#sum()
#count()

grouped_df_agg = pizza_sales_df.groupby(['pizza_size_id'])[['total_price','quantity']].min()

# Using agg to perform different aggregations on different columns
aggregated_data = pizza_sales_df.groupby(['pizza_size_id']).agg({'quantity': 'sum','total_price':'mean'})

# mergeing pizza sales df and pizza sixe df
merged_df = pd.merge(pizza_sales_df,pizza_size_df,on='pizza_size_id')

# Add category information
merged_df = pd.merge(merged_df,pizza_category_df,on='pizza_category_id')

# Concatinate two data frames-appending rows to a dataframe-vertically
another_pizza_sales_df = pd.read_excel('another_pizza_sales.xlsx')
concatinate_vertically = pd.concat([pizza_sales_df,another_pizza_sales_df])
concatinate_vertically=concatinate_vertically.reset_index()

# Conacarinate two data frame - appending columns to a data frame - horizontally
pizza_sales_voucher_df = pd.read_excel('pizza_sales_voucher.xlsx')
concatenate_horizontally = pd.concat([pizza_sales_df, pizza_sales_voucher_df], axis=1)

#Converting to lower case
lower_text = pizza_sales_df['pizza_ingredients'].str.lower()
pizza_sales_df['pizza_ingredients']= pizza_sales_df['pizza_ingredients'].str.lower()

#Convert to uppercase
pizza_sales_df['pizza_ingredients']= pizza_sales_df['pizza_ingredients'].str.upper()

#Converting to title cased
pizza_sales_df['pizza_ingredients']= pizza_sales_df['pizza_ingredients'].str.title()

# Replace the text values
replaced_text = pizza_sales_df['pizza_ingredients'].str.replace('Feta Cheese','Mozzarella')
pizza_sales_df['pizza_ingredients'] = pizza_sales_df['pizza_ingredients'].str.replace('Feta Cheese','Mozarella')

# Removing extra whitespaces 
pizza_sales_df['pizza_name']=pizza_sales_df['pizza_name'].str.strip()

import seaborn as sns
import matplotlib.pyplot as plt

# Generating the Box Plot

sns.boxplot(x='category',y='total_price',data = merged_df)
plt.xlabel('Pizza Category')
plt.ylabel('Total Sales')
plt.title('Boxplot showing distribution of sales  by category')
plt.show()








































