CREATE DATABASE PALLETS;
Use PALLETS;
SELECT * FROM pallet_masked_fulldata;
# Total rows = 80962 
# FIRST MOMENT BUSINESS DECISION (CENTRAL TENDENCY)
## MEAN ##
SELECT AVG(QTY) FROM pallet_masked_fulldata;
# MEAN OF QTY = 42.9650 
## MEDIAN ##
select QTY as median_QTY from(select QTY,ROW_NUMBER()OVER(ORDER BY QTY)AS row_num,
count(*) OVER() AS total_count from  pallet_masked_fulldata) 
AS subquery where row_num = (total_count + 1)/2 OR row_num = (total_count + 2)/2;
# MEDIAN OF QTY = 100
## MODE ##
 Select QTY AS mode_QTY 
from(select QTY, Count(*) AS frenquency 
from pallet_masked_fulldata
 GROUP BY QTY ORDER BY frenquency DESC
 Limit 1) AS subquery;
 # MODE OF QTY = 100
### Second Moment Business Decision(Measures of Dispersion) ###
## Standard Deviation ## 
select stddev(QTY)AS QTY_stddev
from pallet_masked_fulldata;
# STANDARD DEVIATION OF QTY = 212.70050290263885
## Range ##
select max(QTY)-min(QTY) AS
QTY_range
from pallet_masked_fulldata;
# Range of QTY = 1140
## Variance ## 
select variance(QTY) AS
performance_variance
from pallet_masked_fulldata;
# Variance of QTY = 45241.50393503548
### Third Moment Business ( SKEWNESS) ### 
select
(
sum(power(QTY-(select avg(QTY)from
pallet_masked_fulldata), 3))/
(COUNT(*)*power((select stddev(QTY)from
pallet_masked_fulldata),3))
) AS skewness
from pallet_masked_fulldata;
# Skewness of QTY = -0.21399377835270877
### Fourth Moment Business Decision (kurtosis) ###
select
(
(sum(power(QTY-(select avg(QTY)from
pallet_masked_fulldata),4))/
(COUNT(*)*power((select stddev(QTY)from
pallet_masked_fulldata),4)))-3
)AS kurtosis
from pallet_masked_fulldata;
# Kurtosis of QTY = -0.9177984575625486

# DATA PREPROCESSING

#Finding whether there is any null values present
SELECT
COUNT(*) AS total_rows,
SUM(CASE WHEN `Date` IS NULL THEN 1 ELSE 0 END) AS Date_missing,
SUM(CASE WHEN CustName IS NULL THEN 1 ELSE 0 END) AS CustName_missing,
SUM(CASE WHEN City IS NULL THEN 1 ELSE 0 END) AS City_missing,
SUM(CASE WHEN Region IS NULL THEN 1 ELSE 0 END) AS Region_missing,
SUM(CASE WHEN State IS NULL THEN 1 ELSE 0 END) AS State_missing,
SUM(CASE WHEN `Product Code` IS NULL THEN 1 ELSE 0 END) AS Product_Code_missing,
SUM(CASE WHEN `Transaction Type` IS NULL THEN 1 ELSE 0 END) AS Transaction_Type_missing,
SUM(CASE WHEN QTY IS NULL THEN 1 ELSE 0 END) AS QTY_missing,
SUM(CASE WHEN WHName IS NULL THEN 1 ELSE 0 END) AS WHName_missing
FROM pallet_masked_fulldata;
# /*This query provides the count of total rows and the number of missing columns for each column *
# NUMBER OF  NULL VALUES = 0

 #Handling duplicates
# Count duplicates
SELECT `Date`, CustName,City,Region,State,
`Product Code`,`Transaction Type`,QTY,WHName,
COUNT(*)AS DuplicateCount
FROM pallet_masked_fulldata
GROUP BY `Date`, CustName,City,Region,State,
`Product Code`,`Transaction Type`,QTY,WHName
HAVING count(*) > 1;
 # COUNT OF DUPLICATES = 11291
# Remove Duplicates
CREATE TABLE Pallet_clean  as select distinct * from pallet_masked_fulldata;
SELECT * from Pallet_clean;
# After removing duplicates total rows = 64024

# OUTLIER TREATMENT 
select count(case when abs((QTY - mean_stats.mean_value) / std_dev_stats.std_dev) > 3 then 1 end)
            as QTY_outliers
from  Pallet_clean
cross join (select avg(QTY) as mean_value from  Pallet_clean) as mean_stats
cross join (SELECT stddev(QTY) as std_dev from  Pallet_clean) as std_dev_stats;
## Outliers in QTY = 0

## EDA AFTER DATA PREPROCESSING ##
### FIRST MOMENT BUSINESS DECISION (CENTRAL TENDENCY) ###
## MEAN ##
SELECT AVG(QTY) FROM Pallet_clean;
# MEAN OF QTY = 43.0152 
## MEDIAN ##
select QTY as median_QTY from(select QTY,ROW_NUMBER()OVER(ORDER BY QTY)AS row_num,
count(*) OVER() AS total_count from Pallet_clean) 
AS subquery where row_num = (total_count + 1)/2 OR row_num = (total_count + 2)/2;
# MEDIAN OF QTY = 100
## MODE ##
 Select QTY AS mode_QTY 
from(select QTY, Count(*) AS frenquency 
from Pallet_clean
 GROUP BY QTY ORDER BY frenquency DESC
 Limit 1) AS subquery;
 # MODE OF QTY = 100
 
 
### Second Moment Business Decision(Measures of Dispersion) ###
## Standard Deviation ##
select stddev(QTY)AS QTY_stddev
from Pallet_clean;
# STANDARD DEVIATION OF QTY = 211.01670790590484
## Range ##
select max(QTY)-min(QTY) AS
QTY_range
from Pallet_clean;
# Range of QTY = 1140
## Variance ##
select variance(QTY) AS
performance_variance
from Pallet_clean;
# Variance of QTY = 44528.05101544596
### Third Moment Business (SKEWNESS) ###
select
(
sum(power(QTY-(select avg(QTY)from
Pallet_clean), 3))/
(COUNT(*)*power((select stddev(QTY)from
Pallet_clean),3))
) AS skewness
from Pallet_clean;
# Skewness of QTY = -0.17298168861613322
### Fourth Moment Business Decision (kurtosis) ###
select
(
(sum(power(QTY-(select avg(QTY)from
Pallet_clean),4))/
(COUNT(*)*power((select stddev(QTY)from
Pallet_clean),4)))-3
)AS kurtosis
from Pallet_clean;
# Kurtosis of QTY = -0.8636504387372224

# FINDING UNIQUE VALUES 
 select distinct `Date` FROM Pallet_clean;
 # 1608
select distinct CustName FROM Pallet_clean;
# 4183
select distinct City FROM Pallet_clean;
# 696
select distinct Region FROM Pallet_clean;
# 4
select distinct State FROM Pallet_clean;
# 33
select distinct`Product Code` FROM Pallet_clean;
 # 70
 select distinct `Transaction Type` FROM Pallet_clean;
 # 2
  select distinct QTY FROM Pallet_clean ;
# 961
 select distinct WHName FROM Pallet_clean ;
 # 87






