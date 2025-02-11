# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 10:41:49 2025

@author: 91984
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

customer_data=pd.read_csv('customer_data.csv',sep=';')
loan_data=pd.read_excel('loandataset.xlsx')

#Display first few row of our data set
print(loan_data.head())
print(customer_data.head())

#Mergeing two data frame on ID
complete_data= pd.merge(loan_data, customer_data,left_on='customerid',right_on='id')

# Check for missing data
complete_data.isnull().sum()

#Remove rows with missing data
complete_data=complete_data.dropna()

# Check for missing data
complete_data.isnull().sum()

#Check for Duplicated Data
complete_data.duplicated().sum()

#Dropping Duplicates
complete_data=complete_data.drop_duplicates()

#Define a function to categorize purpose into broader categories

def categorize_purpose(purpose):
    if purpose in ['credit card','debt_consolidation']:
        return 'Financial'
    elif purpose in ['educational','small_business']:
        return 'Educatinal/Business'
    else:
        return 'Other'

categorize_purpose('credit card')

complete_data['purpose_category']=complete_data['purpose'].apply(categorize_purpose)

# Creating a conditional statement function
#Create a new function based on criteria
# if dti ration is more than 20 and the delinq.2years is grater than 2 and the revol.util>60 then the borrower is  

def asses_risk(row):
    if row['dti']>20 and row['delinq.2yrs'] >2 and row['revol.util']>60:
        return 'High Risk'
    else:
        return 'Low Risk'
    
complete_data['Risk']=complete_data.apply(asses_risk,axis=1)

#Create a function to categorize FICO scores

def categorize_fico(fico_score):
    if fico_score>=800 and fico_score<=850:
        return 'Excellent'
    elif fico_score>=740 and fico_score<800:
        return 'Very Good'
    elif fico_score >=670 and fico_score<740:
        return 'Good'
    elif fico_score>=580 and fico_score< 670:
        return 'Fair'
    else:
        return 'Poor'
    
    
    complete_data['fico_category']=complete_data['fico'].apply(categorize_fico)

#Identify customers with more than average inquiries and derogatory records with a function 

def identify_high_inq_derog(row):
    average_inq = complete_data['inq.last.6mths'].mean()
    average_derog = complete_data['pub.rec'].mean()
   
    if row['inq.last.6mths']> average_inq and  row['pub.rec'] > average_derog:
        return True
    else:
        return False
    
    
complete_data['High_Inquries_and_Public_Records']= complete_data.apply(identify_high_inq_derog,axis=1)


#Classes
class DataAnalysis:
    def __init__(self,df,column_name):
        self.df=df
        self.column_name=column_name
    def calculate_mean(self):
        return self.df[self.column_name].mean()
    def calculate_median(self):
        return self.df[self.column_name].median()
    
analysis = DataAnalysis(complete_data, 'fico')
mean_fico=analysis.calculate_mean()
median_fico=analysis.calculate_median()


# DAta Visualization 
# Seaborn palettes = 'deep','pastel','dark','muted','bright','colorblind'
#Set the Style of our visualization
sns.set_style('darkgrid')

# Bar Plot to show distribution of loans by purpose
plt.figure(figsize=(10,6))
sns.countplot(x='purpose',data = complete_data,palette='dark')
plt.title("Loan Purpose Distribution")
plt.xlabel('Purpose of loans')
plt.ylabel('Number of Loans')
plt.xticks(rotation=45)
plt.show()

# Create a scatter plot for  dti vs income
plt.figure(figsize=(10,6))
sns.scatterplot(x='log.annual.inc',y='dti',data=complete_data)
plt.title('Debr-to-Income vs Annual Icome')
plt.show()


#Distribution of FICO scores
plt.figure(figsize=(10,6))
sns.histplot(complete_data['fico'],bins=30,kde=True)
plt.title('Distribution of FICO')
plt.show()

# Box Plot to determine Risk vs Intrest Rate 
plt.figure(figsize=(10,6))
sns.boxplot(x='Risk',y='int.rate',data= complete_data)
plt.title('Intrest Rate vs Risk')
plt.show()

# Set the style for visualization
sns.set_style('darkgrid')

# Create subplots
fig, axes = plt.subplots(2, 2, figsize=(20, 20))

# Bar Plot to show distribution of loans by purpose
sns.countplot(ax=axes[0, 0], x='purpose', data=complete_data, palette='dark')
axes[0, 0].set_title("Loan Purpose Distribution")
axes[0, 0].set_xlabel('Purpose of loans')
axes[0, 0].set_ylabel('Number of Loans')
axes[0, 0].tick_params(axis='x', rotation=45)

# Scatter plot for dti vs income
sns.scatterplot(ax=axes[0, 1], x='log.annual.inc', y='dti', data=complete_data)
axes[0, 1].set_title('Debt-to-Income vs Annual Income')
axes[0, 1].set_xlabel('Log Annual Income')
axes[0, 1].set_ylabel('DTI')

# Distribution of FICO scores
sns.histplot(complete_data['fico'], bins=30, kde=True, ax=axes[1, 0])
axes[1, 0].set_title('Distribution of FICO')
axes[1, 0].set_xlabel('FICO Score')
axes[1, 0].set_ylabel('Frequency')

# Box Plot to determine Risk vs Interest Rate
sns.boxplot(ax=axes[1, 1], x='Risk', y='int.rate', data=complete_data)
axes[1, 1].set_title('Interest Rate vs Risk')
axes[1, 1].set_xlabel('Risk')
axes[1, 1].set_ylabel('Interest Rate')

# Adjust layout
plt.tight_layout()
plt.show()



































