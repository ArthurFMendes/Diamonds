#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: ArthurFMendes

Purpose:
    This code is meant to treat missing values in the diamond dataset
"""

###############################################################################
# Importing libraries and base dataset
###############################################################################

import pandas as pd # data science essentials (read_excel, DataFrame)
import matplotlib.pyplot as plt # data visualization

file ='diamonds_missing_values.xlsx'
diamonds = pd.read_excel(file)



###############################################################################
# Viewing our dataset
###############################################################################


# Taking a look at the entire dataset
diamonds



# Viewing the first 5 rows of the dataset
diamonds.head()



# Viewing the first 50 rows of the dataset
diamonds.head(n = 50)



# We can also view the last n rows of our dataset
diamonds.tail(n = 10)



# We can view subsets of columns and rows with loc and iloc

diamonds.loc[:, 'carat']



diamonds.iloc[:, 1]



diamonds.iloc[0:9, :]



diamonds.iloc[20:35, :]



# We can also provide more detailed subsets with loc and iloc
diamonds.loc[:, ['carat', 'price']]



###############################################################################
# Summarizing our dataset
###############################################################################

diamonds.shape


diamonds.info()


diamonds.describe()


diamonds.describe().round(2)



###############################################################################
# Subsetting our dataset
###############################################################################

diamonds[diamonds['carat'] > 1]



diamonds['carat'][
        (diamonds['carat'] > 1) &
        (diamonds['carat'] < 2)
        ]



####Which diamonds cost less than or equal to 1000 (USD)?

diamonds[diamonds['price'] <= 1000]



# Let's sort this set by price.
diamonds[diamonds['price'] <= 1000].sort_values(['price'],ascending= False)


# See Footnote 2 for an explanation of the code above






low_price = diamonds[diamonds['price'] <= 1000]

low_price.sort_values(['price'],
                      ascending= False)



# We can sort on multiple criteria

low_price.sort_values(['cut', 'carat'],
                      ascending= False)




"""
It's interesting that are all of these diamonds come from the same
store. Let's explore this store in more detail.
"""

store_10 = diamonds[diamonds['store'] == 10]


# Rounding this summary to make things more clean.
store_10.describe().round(1)



###############################################################################
# Checking for missing values
###############################################################################

# Let's first check how many observations aren't missing
diamonds.count()



# Stretching out our code so that we can read it more clearly
print(
      diamonds.isnull()
      .any()
      )



# Missing values in absolute numbers
print(
      diamonds
      .isnull()
      .sum()
      )



# As a percentage of total observations (take note of the parenthesis)
print(
      (diamonds.isnull().sum())
      /
      len(diamonds)
)




missing_diamonds = diamonds.isnull().sum()


total_diamonds = diamonds.count()


missing_ratio = missing_diamonds / total_diamonds


missing_ratio.round(2)


###############################################################################
# Flagging missing values
###############################################################################




# How to create a missing value flag
diamonds['carat'].isnull()
diamonds['carat'].isnull().astype(int)



# Sorting to display the missing value flags
(diamonds['carat']
            .isnull()
            .astype(int)
            .sort_values(ascending = False))


# See Footnote 4 for an explanation of the code above






"""
Objective:
    Create columns that are 0s if a value was not missing and 1 if
    a value is missing.
"""


# Coding line by line
diamonds['m_carat'] = (diamonds['carat']
                        .isnull()
                        .astype(int)
                        )



# Since we are repeating the same line of code many times, there is no
# reason to spread it out again.

diamonds['m_color'] = diamonds['color'].isnull().astype(int)


diamonds['m_clarity'] = diamonds['clarity'].isnull().astype(int)


diamonds['m_cut'] = diamonds['cut'].isnull().astype(int)





# Let's check to make sure the code above is working properly.
print(diamonds['carat']
                .isnull()
                .sum())



print(diamonds['m_carat']
                .sum())



# We could also check with the following code
diamonds['carat'].isnull().sum() == diamonds['m_carat'].sum()




###############################################################################
# Looping through missing values
###############################################################################



# Resetting the dataset
diamonds = pd.read_excel(file)



# Creating a loop to improve efficiency
for col in diamonds:

    """ Create columns that are 0s if a value was not missing and 1 if
    a value is missing. """
    
    if diamonds[col].isnull().any():
        diamonds['m_'+col] = diamonds[col].isnull().astype(int)



# checking to see if the for loop worked
print(diamonds.head())


# making a more formal check
a = diamonds.isnull().sum().sum()
b = diamonds.iloc[:,-5:].sum().sum()



if a == b:
    print('All missing values accounted for.')
else:
    print('Some missing values may be unaccounted for, please audit.')


###############################################################################
# Imputing missing values
###############################################################################

# Start by creating three different datasets


# The following code copies and makes each DataFrame independent
df_mean  = pd.DataFrame.copy(diamonds)


df_median = pd.DataFrame.copy(df_mean)


df_dropped = pd.DataFrame.copy(df_median)


# We could fill each column one-by-one
carat_mean = diamonds['carat'].mean()



diamonds['carat'] = (diamonds['carat']
                            .fillna(carat_mean)
                            .round(2))


# See Footnote 8 for a breakdown of the code above



# ... or we could create a loop
for col in df_mean:
    
    """ Impute missing values using the mean of each column """
    
    if df_mean[col].isnull().any():
        
        col_mean = df_mean[col].mean()
        
        df_mean[col] = df_mean[col].fillna(col_mean).round(2)


# See Footnote 9 for a breakdown of the code above



# Creating a loop for df_median
for col in df_median:
    
    """ Impute missing values using the mean of each column """
    
    if df_median[col].isnull().any():
        
        col_median = df_median[col].median()
        
        df_median[col] = df_median[col].fillna(col_median).round(2)



# Using dropna() for df_dropped
df_dropped = df_dropped.dropna().round(2)


# See Footnote 10 for a breakdown of the code above



# With new values imputed, our means should be different between some datasets
print(diamonds['color'].mean())


print(df_mean['color'].mean())


print(df_median['color'].mean())


print(df_dropped['color'].mean())



# We can check this as follows:
diamonds.mean() == df_mean.mean()



# Also, there should be no missing values in our new datasets
print(df_mean.isnull()
                .any()
                .any())



print(df_median.isnull()
                .any()
                .any())



print(df_dropped.isnull()
                .any()
                .any())


# See Footnote 11 for an explanation of the code above



###############################################################################
# Choosing imputation techniques
###############################################################################

# Checking variable distributions

# Creating histograms
plt.hist(df_dropped['carat'], bins = 50)
plt.show()


plt.hist(df_dropped['color'], bins = 50)
plt.show()


plt.hist(df_dropped['clarity'], bins = 50)
plt.show()


plt.hist(df_dropped['cut'], bins = 50)
plt.show()



# Develop something more sophisticated

###################
# Mean or median? #
###################

plt.subplot(2, 2, 1)
plt.hist(df_dropped['carat'],
         bins = 25,
         color='blue',
         alpha = 0.3)
plt.title('Carat Weight')



plt.subplot(2, 2, 2)
plt.hist(df_dropped['color'],
         bins = 20,
         color='green',
         alpha = 0.3)
plt.title('Color')



plt.subplot(2, 2, 3)
plt.hist(df_dropped['clarity'],
         bins = 20,
         color='red',
         alpha = 0.3)
plt.xlabel('Clarity')



plt.subplot(2, 2, 4)
plt.hist(df_dropped['cut'],
         bins = 3,
         color='purple',
         alpha = 0.1)
plt.xlabel('Cut')



plt.savefig('Histograms before Imputation.png')
plt.show()



# carat seems skewed positive... median
# color seems skewed positive... median
# clarity looks normally distributed... mean
# cut is binomial... mode expressed as the median



###############################################################################
# Imputing missing values on the original dataset
###############################################################################

# Median imputation carat

fill = diamonds['carat'].median()


diamonds['carat'] = diamonds['carat'].fillna(fill)



# Median imputation color
fill = diamonds['color'].median()


diamonds['color'] = diamonds['color'].fillna(fill)



# Median imputation cut
fill = diamonds['cut'].median()


diamonds['cut'] = diamonds['cut'].fillna(fill)



print(diamonds['carat'].isnull().any())

print(diamonds['color'].isnull().any())

print(diamonds['cut'].isnull().any())



# Mean imputation (clarity)
fill = diamonds['clarity'].mean()


diamonds['clarity'] = diamonds['clarity'].fillna(fill).astype(int)


# See Footnote 13 for an explanation of the code above


print(diamonds['clarity'].isnull().any())



###############################################################################
# Checking data after imputation
###############################################################################

plt.subplot(2, 2, 1)
plt.hist(diamonds['carat'],
         bins = 25,
         color='blue',
         alpha = 0.98)
plt.title('Carat Weight')



plt.subplot(2, 2, 2)
plt.hist(diamonds['color'],
         bins = 20,
         color='green',
         alpha = 0.8)
plt.title('Color')



plt.subplot(2, 2, 3)
plt.hist(diamonds['clarity'],
         bins = 20,
         color='red',
         alpha = 0.8)
plt.xlabel('Clarity')



plt.subplot(2, 2, 4)
plt.hist(diamonds['cut'],
         bins = 3,
         color='purple',
         alpha = 0.8)
plt.xlabel('Cut')



plt.savefig('Histograms after Imputation.png')
plt.show()


###############################################################################
# Saving things for future use
###############################################################################

# saving dataset
diamonds.to_excel('diamonds_imputed.xlsx', index = False)
