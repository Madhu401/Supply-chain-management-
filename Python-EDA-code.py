## OPTIMIZATION IN SUPPLY CHAIN MANAGEMENT ##

import pandas as pd
import numpy as np
from scipy import stats 
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import create_engine
import pymysql
import mysql.connector 

dir (pd)

# Load the dataset
Pallets_Data = pd.read_excel (r"C:\Users\sudha\OneDrive\Desktop\Pallet Masked Full Data.xlsx")
Pallets_Data
# Total rows = 80962
# Total columns = 9

# Display top 10 records
Pallets_Data.head(10)

# Connect to MYSQL Database

#  MySQL server details
host = "127.0.0.1"
user = "root"
password = "Madhu@330"
database = "pallets"

# Establish a connection to the MySQL server
connection = mysql.connector.connect(host=host,user=user,password=password,database=database)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Example: Execute a simple query
cursor.execute("SELECT * FROM `pallet_masked_fulldata`")
result = cursor.fetchall()
columns = [i[0] for i in cursor.description]
df = pd.DataFrame(result, columns=columns)
print(df)

# Total rows = 80962
# Total columns = 9

# Close the cursor and connection
cursor.close()
connection.close()

# Dataframe shape and data type #
Pallets_Data.shape

# Total rows = 80962
# Total columns = 9

Pallets_Data.dtypes
# Date                datetime64[ns]
# CustName                     int64
# City                        object
# Region                      object
# State                       object
# Product Code                object
# Transaction Type            object
# QTY                          int64
# WHName                       int64

# FIRST MOMENT BUSINESS DECISION : Measures of central Tendency #

# MEAN
Pallets_Data.QTY.mean()
# Mean of Quantity = 42.96

# MEDIAN 
Pallets_Data.QTY.median()
# Median of QTY = 100

# MODE 
Pallets_Data.Date.mode()
# Mode of Date = 2022-07-11

Pallets_Data.CustName.mode()
# Mode of CustName = 11
                 
Pallets_Data.City.mode()  
# Mode of City = Ahmedabad

Pallets_Data.Region.mode() 
# Mode of Region = North
                     
Pallets_Data.State.mode()
# Mode of State  = Maharashtra
                     
Pallets_Data['Product Code'].mode() 
# Mode of Product Code = A010000035
               
Pallets_Data['Transaction Type'].mode()
# Mode of Transaction Type = Allot
            
Pallets_Data.QTY.mode()  
# Mode of QTY = 100
                        
Pallets_Data.WHName.mode()
# Mode of WHName = 1009                    


# SECOND MOMENT BUSINESS DECISION : Dispersion #

# VARIANCE #
Pallets_Data.QTY.var()
# Variance of QTY = 45242.06274117576

# STANDARD DEVIATION #

Pallets_Data.QTY.std()
# Standard deviation of QTY = 212.70181649712293

Pallets_Data.QTY.max() - Pallets_Data.QTY.min()
# Range of QTY =  1140

# THIRD MOMENT BUSINESS DECISION (Skewness) #
Pallets_Data.QTY.skew()
#Skewness of  QTY = -0.2139977431626821

# FOURTH MOMENT BUSINESS DECISION (Kurtosis) #
Pallets_Data.QTY.kurt()
#Quantity = -0.9177810283949985


# Handling Missing values #
Missing_values = Pallets_Data.isna().sum().sort_values(ascending = False)
print(Missing_values)
# NO NULL VALUES


# Handling Duplicates #
# Count duplicates
Duplicates = Pallets_Data.duplicated()
Duplicates
sum(Duplicates)

# No.of Duplicates = 16938

# Remove Duplicates #

Pallets_Data = Pallets_Data.drop_duplicates()
Duplicates = Pallets_Data.duplicated()
sum(Duplicates)
print(Pallets_Data)
# AFTER  REMOVING DUPLICATES TOTAL ROWS = 64024

# Outliers Treatment #
# QTY
Q1 = Pallets_Data['QTY'].quantile(0.25)
Q3 = Pallets_Data['QTY'].quantile(0.75)
IQR = Q3-Q1
Pallets_Data = Pallets_Data[(Pallets_Data['QTY']>= Q1 - 1.5*IQR) & (Pallets_Data['QTY']<= Q3 + 1.5*IQR)]
print(Pallets_Data)
plt.boxplot(Pallets_Data.QTY)

# THERE ARE NO OUTLIERS


# GRAPHICAL REPRESENTATION #

## HISTOGRAM ##

plt.hist(Pallets_Data.QTY, color = 'purple', bins = 15, alpha = 1)
# It is used to represent the Distribution of the numerical variables
# It is an estimate of the probability distibution
# There arae no gaps between the bars of the histogram
# Here, It represents the frequency of QTY
# Insight: Identify the most frequent quantity ranges of pallets in the dataset.


## LINE PLOT ##

# set the figure size:
plt.figure(figsize = (10,10))
plt.plot(Pallets_Data['Date'], Pallets_Data['QTY'], color='r', marker='*', linestyle='--')
Date = np.arange(1,13)
# Add labels and title
plt.xlabel('Date')
plt.ylabel('Quantity')
plt.title('Quantity Over Time')
# Add a grid with green color and solid linestyle
plt.grid(color='g', linestyle='--')
# displaying the plot
plt.show
# A line plot allows you to observe trends in pallet quantities over time. Is the quantity increasing, decreasing, or remaining relatively stable?
# Insights: Identify overall trends in demand or production that can help with forecasting and planning.
## IT IS A SIMPLE POINT THAT DISPLAYS THE RELATIONSHIP BETWEEN TWO VARIABLES ##
## Here, it displays the relationship between Date and Quantity ##

## BOX PLOT ##
plt.boxplot(Pallets_Data.QTY)

# Insights: Recognize extreme values that may contribute to inventory volatility or indicate unusual events.
# It is used to visualize the distribution of the numeric variable
# Used to detect the outliers(extreme values) in the data
# Here, there are no outliers

## SCATTER PLOT ##

plt.scatter(x = Pallets_Data.QTY, y = Pallets_Data["Product Code"])
plt.scatter(x = Pallets_Data.QTY, y = Pallets_Data["WHName"])
plt.scatter(x = Pallets_Data.QTY, y = Pallets_Data["CustName"])
plt.scatter(x = Pallets_Data.QTY, y = Pallets_Data["Date"])

# Insights: Observe changes in the relationship between variables and adapt strategies accordingly.
# Insights: Detect unusual or extreme values that may impact inventory management
# There is no correlation 
# It is used to display the relationship between two Numerical variables
# Used to represent the extent of correlation between two variables
# Used to detect extreme points in the data

## BAR PLOT ## 

sns.barplot(data = Pallets_Data, x = 'CustName', y = 'QTY')
plt.show()
# Insights: Identify which customers are major contributors to the overall quantity, allowing for targeted customer management strategies.
sns.barplot(data = Pallets_Data, x = 'Transaction Type', y = 'QTY')
plt.show()
# Insights: Understand the balance between incoming and outgoing pallets and identify any trends or irregularities.
sns.barplot(data = Pallets_Data, x = 'Product Code', y = 'QTY')
plt.show()
# Insights: Identify which products contribute the most to the overall quantity, helping in inventory management and demand forecasting.
sns.barplot(data = Pallets_Data, x = 'WHName', y = 'QTY')
plt.show()
# Insights: Identify high-performing or low-performing warehouses, helping in optimizing inventory storage and distribution.
sns.barplot(data = Pallets_Data, x = 'Transaction Type', y = 'WHName')
plt.show()
# Insights: Understand how different transaction types impact individual warehouses.


# DISTRIBUTION PLOT #
 
sns.distplot(Pallets_Data.QTY, color = 'red')
# Insights: Gain a clear understanding of how pallet quantities are distributed across different values.
# It displays the distribution of the data
# Here,the distribution of skewness of QTY is Negative Skewness
# The Peakedness of Kurtosis of QTY is Platykurtic

## DENSITY PLOT ##
sns.kdeplot(Pallets_Data.QTY, color = 'red')
# The distribution of QTY data is not near to normal distribution
# Its like the distribution plot


## VIOLIN PLOT ##
sns.violinplot(data = Pallets_Data,x = "Region", y = "QTY", palette = ['red','green','pink','purple'] )
# Insights: Identify regions of the quantity spectrum with higher concentrations of pallets, which can inform inventory management strategies.
# It is the similar to a Boxplot, the Displays the kernel Density estimator for the underlying distribution
# It shows the distributionn of the quantitative data across categorical variables such that those distribution can be compared
# Here, we can identify the distribution of QTY data across Region variable

sns.violinplot(data = Pallets_Data,x = "Transaction Type", y = "QTY", palette = ['red','green'])
sns.violinplot(data = Pallets_Data,x = "Product Code", y = "QTY", palette = ['red','green'])
sns.violinplot(data = Pallets_Data,x = "WHName", y = "QTY", palette = ['red','green'])
# Insights: Identify variations in distribution patterns across categories and understand factors contributing to volatility.
# Violin plots can be used to compare the distribution of pallet quantities across different categories (e.g., Product Code, Transaction Type, Warehouse Name).

## STRIP PLOT ##
sns.stripplot(data = Pallets_Data,x = "Region", y = "QTY")
sns.stripplot(data = Pallets_Data,x = "WHName", y = "QTY")
sns.stripplot(data = Pallets_Data,x = "Transaction Type", y = "QTY")
# Insights: Identify the specific data points (e.g., regions, transaction types) and their corresponding quantities.
# It is so similar to scatter plot
# one axis represents the categorical variable and another axis value of the correspanding categories

# Create a stem-and-leaf plot #
import stemgraphic as sg
stem_and_leaf_plot = sg.stem_graphic(Pallets_Data.QTY)
# Display the plot
print(stem_and_leaf_plot)
# Insights: Identify clusters or gaps in the data, revealing patterns that may be important for decision-making.
# The stem-and-leaf plot is a simple way to represent the distribution of a dataset. 
# The stems represent the leading digits, and the leaves represent the trailing digits. 
# The plot provides a visual representation of the data's distribution, and it's particularly useful for small datasets.

# Create a Time series plot #
plt.figure(figsize=(13, 6))
plt.plot(df.index, df['QTY'], label='Time Series Data', marker='o', linestyle='-', color='blue')
# Add labels and title
plt.xlabel('Date')
plt.ylabel('QTY')
plt.title('Time Series Plot')
# Add a legend
plt.legend()
# Display the plot
plt.show()
# Insights: Determine if there are long-term trends that contribute to inventory volatility.
# Insights: Align inventory targets with actual demand patterns to reduce overstocking and understocking.
# When creating time series plots, it's important to choose appropriate visualization techniques and consider factors like the granularity of the time intervals, 
# the duration of the time series, and the specific insights you aim to gain from the visual representation. 
# Time series plots provide a clear and intuitive way to interpret temporal patterns and trends in data.

# Create excel sheet with cleaned Data
Pallets_Data = pd.DataFrame(Pallets_Data)
Pallet_Cleaned_Data = Pharmacy_data.to_excel("C:\\Users\\sudha\\OneDrive\\Desktop\\Pallet Cleaned data.xlsx")
Pallet_Cleaned_Data
                          ## AUTO EDA ##

# (D-Tale) # 
import dtale as dt
dt.show(Pallets_Data)
Pallet = dt.show(Pallets_Data)
Pallet.open_browser()
# 	In our data we have 64024 records with 9 variables but it adds one index column and showing 10 variables with the 64024 records

# Sweetviz #
import sweetviz as sv
sv.analyze(Pallets_Data)
Pallet_report = sv.analyze(Pallets_Data)
Pallet_report.show_html('sweetviz_report.html')
# They generate various statistical analyses and visualizations to help users understand the patterns, distributions, and relationships within their data.

#Autoviz #

from autoviz.AutoViz_Class import AutoViz_Class
AV = AutoViz_Class()
%matplotlib inline
Pallet_AV = AV.AutoViz((r'C:\Users\sudha\OneDrive\Desktop\Pallet Cleaned data.xlsx'))
# Visualize the availability of Quantity of pallets in ware houses.
# Use visualizations to understand stock levels, reorder points, and supply chain dynamics.

# PANDAS PROFILING #
# pip install --upgrade typing
# pip install ydata_profiling
import sys
import webbrowser
from ydata_profiling import ProfileReport
Pallet_Profile = ProfileReport(Pallets_Data, title = "Panda Profiling Report")
Pallet_Profile.to_notebook_iframe()
webbrowser.open("Panda Profiling Report.html")
# It creates an HTML report that includes information about the distribution of data, missing values, correlations, and more.
# QTY is highly overall correlated with Transaction Type.	
# Region is highly overall correlated with State	.
# State is highly overall correlated with Region.

# DATA PREP #
import dataprep
from dataprep.eda import create_report
df = pd.read_excel(r'C:\Users\sudha\OneDrive\Desktop\Pallet Cleaned data.xlsx')
create_report(Pallets_Data)

# we can create all the possible visualizations for the data using just a single line of code.
# To get a detailed plot for a single column with all its statistics to understand the column better.

