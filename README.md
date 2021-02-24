# Project Description

This project is to give you a first glance in the day of a full stack data scientist. The idea is to predict Real Estate House prices in Germany. Steps we do:

## Scrape Data
- First, scrape all houses information you can get from the website ```https://www.athome.de/en/```. We limit ourselves to following features:
  -  sales price
  -  living surface
  -  land
  -  number of rooms 
  -  location

## Cleanining Data
- Second, cleaning all the data including NaN values, formatting etc. 

## Feature Engineering
- In the third step we will do some Feature Engineering like One-Hot Encoding, Handling Outliers, and Dimensionality Reduction etc.

After above three-steps the data preparation part should be done, which according to Forbes takes about 80% of the work of a data scientist.

## Build a Model, measuring accuracy, and finding best model
- Our base model will be Linear Regression
- We will use k-fold Cross-Validation to measure accuracy of our Linear Regression model
- Finding the best model via GridSearchCV


### Note: Feature Engineering and Model Building code should be uploaded until 1.March 2021
