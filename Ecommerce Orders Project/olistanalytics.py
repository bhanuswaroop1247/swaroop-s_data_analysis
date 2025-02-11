# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 10:23:15 2025

@author: 91984
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the working Directory
os.chdir('C:\\Users\\91984\\Documents\\Python for Data Analysis Udemy\\Ecommerce Orders Project')
print(os.getcwd())


# =============================================================================
# Loading files
# =============================================================================

# Load the orders data
orders_data = pd.read_excel('C:/Users/91984/Documents/Python for Data Analysis Udemy/Ecommerce Orders Project/orders.xlsx')

#load Payments data
#if it is a csv file us pd.read_csv(file path)
payments_data=pd.read_excel('C:/Users/91984/Documents/Python for Data Analysis Udemy/Ecommerce Orders Project/order_payment.xlsx')

# load the customers data

customers_data=pd.read_excel('C:/Users/91984/Documents/Python for Data Analysis Udemy/Ecommerce Orders Project/customers.xlsx')
# =============================================================================
# Describing the data
# =============================================================================
orders_data.info()
payments_data.info()
customers_data.info()

# Handling the missing data

#check for missing data in orders data

orders_data.isnull().sum()
payments_data.isnull().sum()
customers_data.isnull().sum()

# Filling in the missing values in the ordes data with a default values
orders_data2=orders_data.fillna('N/A')
#check if there are null values in null values in oreders data 2
orders_data2.isnull().sum()

#Drop rows with missing values in payments data
payments_data=payments_data.dropna()

#check if there are null values in null values in oreders data 2
payments_data.isnull().sum()

# =============================================================================
# Removing duplicte data
# =============================================================================

# Check for duplictes in our orders data
orders_data.duplicated().sum()

# Remove duplicates from orders data
orders_data=orders_data.drop_duplicates()

#duplictes in th e payments data
payments_data.duplicated().sum()

# Remove duplicates from payments data
payments_data=payments_data.drop_duplicates()


# =============================================================================
# Filtering the data
# =============================================================================

#Select the subset of the orders data basedx on the order status
invoiced_orders_data= orders_data[orders_data['order_status'] == 'invoiced']
# Reset the index
invoiced_orders_data=invoiced_orders_data.reset_index(drop=True)

#Select a subset of the payments data where payment type = Credit Card and payment value>1000
credit_card_payments_data = payments_data[
    (payments_data['payment_type']=='credit_card') & 
    (payments_data['payment_value']>1000)
    ]

#Select a subset of customers based on the customer state = SP
customers_data_state=customers_data[customers_data['customer_state']=='SP']

# =============================================================================
# Merge and join data frames
# =============================================================================

#Merege Oerders data with payments data on order_id column
merged_data= pd.merge(orders_data,payments_data,on='order_id')

#Join the merged data with our customers data on the customer_id column
joined_data = pd.merge(merged_data,customers_data,on='customer_id')


# =============================================================================
# Data Visualization
# =============================================================================
#Create a field called month_year from order_purchase_timestamp

joined_data['month_year'] = joined_data['order_purchase_timestamp'].dt.to_period('M')
joined_data['week_year'] = joined_data['order_purchase_timestamp'].dt.to_period('W')
joined_data['year'] = joined_data['order_purchase_timestamp'].dt.to_period('Y')

grouped_data=joined_data.groupby('month_year')['payment_value'].sum()
grouped_data=grouped_data.reset_index()
#Convert Month_year from period to string
grouped_data['month_year']=grouped_data['month_year'].astype(str)
#Creating  a plot

plt.plot(grouped_data['month_year'],grouped_data['payment_value'],color='red',marker='o')
plt.ticklabel_format(useOffset=False,style='plain',axis='y')
plt.show()
plt.xlabel('Month and Year')
plt.ylabel('Payment Value')
plt.title('Payment Value by month and year')
plt.xticks(rotation=90,fontsize=10)
plt.yticks(fontsize=8)



#Sactter Plot

#Create the Data Frame
scatter_df=joined_data.groupby('customer_unique_id').agg({'payment_value' : 'sum','payment_installments' : 'sum'})

plt.scatter(scatter_df['payment_value'], scatter_df['payment_installments'])
plt.xlabel('Payment value')
plt.ylabel('Payment Installments')
plt.title('Payment Value vs Installments by customers')
plt.show()

#Using seaborn to create a scatterf plot

sns.set_theme(style='darkgrid') #whitegrid,darkgrid,white
sns.scatterplot(data=scatter_df,x='payment_value',y='payment_installments')
plt.xlabel('Payment value')
plt.ylabel('Payment Installments')
plt.title('Payment Value vs Installments by customers')
plt.show()


#Creating a Bar Chart
bar_chart_df=joined_data.groupby(['payment_type','month_year'])['payment_value'].sum()
bar_chart_df=bar_chart_df.reset_index()

pivot_data=bar_chart_df.pivot(index='month_year',columns='payment_type',values='payment_value')

pivot_data.plot(kind='bar',stacked='True')
plt.ticklabel_format(useOffset=False,style='plain',axis='y')
plt.xlabel('Month of Payment')
plt.ylabel('Payment Value')
plt.title('Payment per Payment Type by Month')
plt.show()


#Creating Box Plot
payment_values=joined_data['payment_value']
payment_types=joined_data['payment_type']

# Creating a seoarate box plot per oayment type
plt.boxplot([ payment_values[payment_types=='credit card'],
            payment_values[payment_types== 'boleto'],
            payment_values[payment_types== 'voucher'],
            payment_values[payment_types== 'debit_card']],
            labels=['Credit card','Boleto','voucher','Debit Card'])
plt.xlabel('Payment Type')
plt.ylabel('Payment value')
plt.title('Box Plot showing Payment value ranges by payments type')
plt.show()



# Creating a subplot (3 plots in one)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))

# Box plot
ax1.boxplot([
    payment_values[payment_types == 'credit card'],
    payment_values[payment_types == 'boleto'],
    payment_values[payment_types == 'voucher'],
    payment_values[payment_types == 'debit_card']
], labels=['Credit card', 'Boleto', 'Voucher', 'Debit Card'])

ax1.set_xlabel('Payment Type')
ax1.set_ylabel('Payment Value')
ax1.set_title('Box Plot showing Payment Value Ranges by Payment Type')

# Stacked bar chart (corrected)
pivot_data.plot(kind='bar', stacked=True, ax=ax2)  # Specify ax=ax2

ax2.ticklabel_format(useOffset=False, style='plain', axis='y')
ax2.set_xlabel('Month of Payment')
ax2.set_ylabel('Payment Value')
ax2.set_title('Payment per Payment Type by Month')

plt.tight_layout()  # Adjust layout to prevent overlap


# Ax3 which is Scatter plot
ax3.scatter(scatter_df['payment_value'], scatter_df['payment_installments'])
ax3.set_xlabel('Payment value')
ax3.set_ylabel('Payment Installments')
ax3.set_title('Payment Value vs Installments by customers')
fig.tight_layout()


plt.savefig('E-Commerce_Orders_Analysis.png')
plt.show()











































































































