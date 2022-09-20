#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 13:42:11 2022

@author: pat
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

json_file = open('loan_data_json.json')
data = json.load(json_file)

with open('loan_data_json.json') as json_file:
    data = json.load(json_file)


#transform to datafram
loandata = pd.DataFrame(data)

loandata.describe()
loandata.info()

#finding unique values for the purpose column
loandata['purpose'].unique()

#descibe the 'fico' column
loandata['fico'].describe()

#debt to income ratio
loandata['dti'].describe()

#using exp to get annual income
income = np.exp(loandata['log.annual.inc'])
loandata['annualincome'] = income

#FICO score
fico = 250

if fico >= 300 and fico < 400:
    ficocat = 'Very Poor'
elif fico >= 400 and fico < 600:
    ficocat = 'Poor'
elif fico >= 600 and fico < 660:
    ficocat = 'Fair'
elif fico >= 660 and fico < 700:
    ficocat = 'Good'
elif fico >= 700:
    ficocat = 'Excellent'
else:
    ficocat = 'Unknown'
print(ficocat)    
    

#applying for loops to loan data and catrgorizing scores
length = len(loandata)
ficocat = []
for x in range(0,length):
    category = loandata['fico'][x]
    
    try:
        if category >= 300 and category < 400:
            cat = 'Very Poor'
        elif category >= 400 and category < 600:
            cat = 'Poor'
        elif category >= 600 and category < 660:
            cat = 'Fair'
        elif category >= 600 and category < 700:
            cat = 'Good'
        elif category >= 700:
            cat = 'Excellent'
        else:
            cat = 'Unknown'
    except:
        cat = 'Unknown'
    ficocat.append(cat)
# making it a series
ficocat = pd.Series(ficocat)

#Adding to table
loandata['fico.category'] = ficocat
    

#df.loc as conditional statements
#for interest rates, a new column is wanted. rate > 0.12 then high, else low
loandata.loc[loandata['int.rate'] > 0.12, 'int.rate.level'] = 'High'
loandata.loc[loandata['int.rate'] <= 0.12, 'int.rate.level'] = 'Low'
    
    
#number of loans/rows by fico.category and creating bar charts
catplot = loandata.groupby(['fico.category']).size()  
catplot.plot.bar(color = 'green', width = 0.1)
plt.show() 

   
purposeplot = loandata.groupby(['purpose']).size()
purposeplot.plot.bar(color = 'red', width = 0.2)
plt.show()

#scatter plot of debt to income ratio
xpoint = loandata['dti']
ypoint = loandata['annualincome']
plt.scatter(xpoint,ypoint, color = '#4caf50')
plt.show()

#writing to csv
loandata.to_csv('loan_cleaned.csv', index = True)

