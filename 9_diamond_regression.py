#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 21:25:55 2018

@author: chase.kusterer

Working Directory:
/Users/chase.kusterer/Desktop/PyCourse

Purpose:
    This code is meant for exploratory data analysis (EDA) of the 
    diamond dataset.
"""

###############################################################################
# Importing libraries and base dataset
###############################################################################
import pandas as pd # data science essentials
import matplotlib.pyplot as plt # data visualization
import seaborn as sns # more data visualization
import statsmodels.api as sm
import statsmodels.formula.api as smf # regression modeling
import statsmodels.graphics as smg

file ='diamonds_explored.xlsx'
diamonds = pd.read_excel(file)


###############################################################################
# Visual Regression Analysis
###############################################################################

# Let's start by plotting carat and price
sns.lmplot(x = 'carat',
           y = 'price',
           data = diamonds)


plt.grid()
plt.tight_layout()
plt.show()



# Now let's segment by channel
sns.lmplot(x = 'carat',
           y = 'price',
           data = diamonds,
           hue = 'channel',   # segments by channel
           legend = True,     # creates a legend
           legend_out = True, # moves the legend slightly outside
           scatter_kws= {"marker": "D", 
                        "s": 10},
           palette = 'nipy_spectral')


plt.grid()
plt.title("Price ~ Carat|Channel Regression")
plt.tight_layout()
plt.show()



"""
Prof. Chase:
   The plot generated is very busy. It is very challenging to
   graphically display multivariate regression, hence why we tend to
   rely on a numeric approach for problems such as these.
   
   We can simplify our plots by printing them out seperately.
"""


# Let's build a seperate plot for each channel

my_plot = sns.lmplot(x = 'carat',
           y = 'price',
           data = diamonds,
           hue = 'channel',
           col = 'channel', # creates seperate plots
           col_wrap = 2,    # sets the number of plots per row
           scatter_kws= {"marker": "D", 
                        "s": 10},
           palette = 'nipy_spectral')


my_plot.set_axis_labels("", "Price")


plt.tight_layout()
plt.savefig("Price ~ Carat|Channel Regression.png")
plt.show()

# See Footnote 1 for an explanation of the code above



# Adding information based on store
my_plot = sns.lmplot(x = 'carat',
                     y = 'price',
                     data = diamonds,
                     hue = 'store',
                     col = 'channel', # creates seperate plots
                     col_wrap = 2,    # sets the number of plot rows
                     legend = True,
                     legend_out = True,
                     scatter_kws= {"marker": "D", 
                                   "s": 10},
                                   palette = 'nipy_spectral')


my_plot.set_axis_labels("", "Price")



plt.tight_layout()
plt.savefig("Price ~ Carat by Channel and Store.png")
plt.show()



########################
# Using regplot
########################

"""
Prof. Chase:
    regplot is very similar to lmplot, but has a few advantages as
    expressed below. Notice that the syntax is similar to lmplot,
    however, several of the options in lmplot are not valid in regplot.
"""


# Adding information based on store
my_plot = sns.regplot(x = 'carat',
                     y = 'price',
                     data = diamonds,
                     x_estimator = pd.np.mean,
                     x_bins = 8)


my_plot.set_axis_labels("", "Price")



plt.tight_layout()
plt.savefig("Price ~ Carat by Channel and Store.png")
plt.show()



########################
# Using jointplot
########################

my_plot = sns.jointplot(x = 'carat',
                     y = 'price',
                     kind = 'reg',
                     joint_kws={'color':'blue'},
                     data = diamonds)


my_plot.set_axis_labels("", "Price")



plt.tight_layout()
plt.savefig("Price ~ Carat Jointplot.png")
plt.show()



###############################################################################
# More Visual Regression Analysis
###############################################################################


"""
Prof. Chase:
    Visual regression analysis is generally done to help us observe
    which may be a good fit for linear regression.
    
    Use this area to test other variables using sns.lmplot
"""



###############################################################################
# Plotting Residuals
###############################################################################

"""
Prof. Chase:
    We can plot the residuals from univariate models using
    sns.residplot. Note: It is not common to plot the residuals of more
    complicated models, thus we rely on a numeric approach.
"""

my_resid = sns.residplot(x = 'carat',
                         y = 'price',
                         data = diamonds,
                         lowess = True,
                         color = 'r',
                         line_kws = {'color':'black'})


plt.tight_layout()
plt.savefig("Price ~ Carat Redidual Plot.png")
plt.show()



# Cleaning up the plot with an x estimator

my_resid = sns.residplot(x = 'carat',
                         y = 'price',
                         data = diamonds,
                         lowess = True,
                         color = 'r',
                         line_kws = {'color':'black'},)


plt.tight_layout()
plt.savefig("Price ~ Carat Redidual Plot.png")
plt.show()



###############################################################################
# Regression in statsmodels
###############################################################################


"""
Prof. Chase:
    We can use statsmodels.formula.api (smf) for a more sophisticated
    regression analysis.
"""

########################
# Univariate OLS regression
########################

# OLS linear regression can be run usning 'smf.ols'
lm_price_carat = smf.ols(formula = 'price ~ carat',
                         data = diamonds)



# We can use .fit() to access the results of our model.
results = lm_price_carat.fit()



# Printing the summary statistics, similar to the output generated
# from Excel
print(results.summary())



# There is also a summary2 function in results
print(results.summary2())



# To learn more about what is available in results, you can use the
# following command.
dir(results)



# Let's utlize results.params

carat_weight = 2

pred_price = results.params[0] + results.params[1] * carat_weight



# We can build a function based on our regression model
def price_pred():
    """Predicts price based on the carat weight."""
    
    import statsmodels.formula.api as smf
    
    results = smf.ols(formula = 'price ~ carat',
                      data = diamonds).fit()
    
    carat_weight = int(input("Input carat weight > "))

    pred_price = results.params[0] + results.params[1] * carat_weight

    print(f"""
      
A diamond of that size will cost approximately {round(pred_price, 2)}.

      """)

price_pred()


# See Footnote 2 for an explanation of the code above



# We can refine our fuction using confidence intervals.
results.conf_int()


"""
Prof. Chase:
    To index individual elements of the confidence interval, we can
    add .iloc after conf_int(). We need the () before .iloc because
    not including it returns a statsmodels object.
"""


# Aggressive estimate (lower price)
lower_95 = results.conf_int().iloc[0,0] + results.conf_int().iloc[1,0]


# Conservative estimate (higher price)
upper_95 = results.conf_int().iloc[0,1] + results.conf_int().iloc[1,1]




# Refining the price_pred() function.
def price_pred_rng(carat_weight):
    """Predicts price based on the carat weight."""
    
    import statsmodels.formula.api as smf
    
    results = smf.ols(formula = 'price ~ carat',
                      data = diamonds).fit()
    
    pred_price = results.params[0] + results.params[1] * carat_weight

    lower_95 = (results.conf_int().iloc[0,0] + 
                results.conf_int().iloc[1,0] *
                carat_weight)
    
    upper_95 = (results.conf_int().iloc[0,1] +
                results.conf_int().iloc[1,1] *
                carat_weight)
    
    print(f"""
      
A diamond of that size will cost approximately between {round(lower_95, 2)} and
{round(upper_95, 2)}. The best estimate for that size is {round(pred_price, 2)}.

      """)

price_pred_rng(2)


# See Footnote 3 for an explanation of the code above



########################
# Other key results calls
########################

results.aic

results.bic

results.rsquared

results.rsquared_adj

results.fittedvalues

results.pvalues

results.resid



###############################################################################
# Residual Analysis
###############################################################################

"""
Prof. Chase:
    Residual analysis is very useful in understanding how far off we
    are on each individual observation. In this section we will compare
    residuals with the predicted and actual diamond values.
"""

# The model results are below for reference
lm_price_carat = smf.ols(formula = 'price ~ carat',
                         data = diamonds)


results = lm_price_carat.fit()



# Residuals
residuals = results.resid

print(residuals)



# Fitted values
predicted_prices = results.fittedvalues

print(predicted_prices)



# Creating a DataFrame with original, predicted, and residual values
predict_df = pd.DataFrame(diamonds['Obs'])

predict_df['Price'] = pd.DataFrame(diamonds['price'])

predict_df['Predicted'] = predicted_prices.round(2)

predict_df['Residuals'] = residuals.round(2)

predict_df['Abs_Residuals'] = residuals.round(2).abs()

print(predict_df)



# Let's add the absolute values of the residuals
predict_df = predict_df.sort_values(by = 'Abs_Residuals', ascending = False)

print(predict_df)




########################
# Visual Residual Analysis
########################

# Below is a command for setting a large plot size
fig, ax = plt.subplots(figsize=(12,8))



# Plotting the residuals
figure = smg.regressionplots.plot_fit(results = results,
                                      exog_idx = 'carat',
                                      ax = ax)


# Adding a line
line = smg.regressionplots.abline_plot(model_results = results,
                                           ax = figure.axes[0])


plt.legend(loc = 'lower right')

plt.savefig('Price ~ Carat Predicted v. Actual Diamond Values.png')

plt.show()


# See Footnote 4 for an explanation of the code above



###############################################################################
# Advanced Regression Techniques - Regression Outliers
###############################################################################

"""
Prof. Chase:
    The Bonferroni outlier test is a good method for detecting
    regression outliuers. This helps detect outliers based on how far
    off an observation is from its predicted value. It is similar to
    the boxplot, but instead of taking the mean as the measure of
    center, it takes the average residual as its measure of center.
    That means with different models, you will get different sets of
    outliers.
"""

# Bonferroni outlier test
test = results.outlier_test()

print('Bad data points (bonf(p) < 0.05):')
print(test[test.iloc[:, 2] < 0.05])



# Let's investigate these outliers further
outlier_list = [199, 209, 210, 380]

bonf_outliers = diamonds.iloc[outlier_list, : ]

print(bonf_outliers)



# Dropping the missing and outlier columns
bonf_outliers = bonf_outliers.iloc[:, 0:8]

print(bonf_outliers)



# Adding predicted_price
pred_val = results.fittedvalues.iloc[outlier_list]

bonf_outliers['pred_price'] = pred_val

print(bonf_outliers)



# Comparing to the average diamond
diamonds.iloc[:, 0:8].mean()



# We can append the means to our DataFrame with .append()
bonf_outliers = bonf_outliers.append(diamonds.iloc[:, 0:8].mean(),
                                     ignore_index = True)


print(bonf_outliers)



# We can fix the missing pred_price with the following code
bonf_outliers.loc[4, 'pred_price'] = results.fittedvalues.mean()



# Rounding to two decimal places
bonf_outliers = round(bonf_outliers, 2)

print(bonf_outliers)



# Using price_pred_new() to investigate Obs 405
price_pred_rng(1.01)



########################
# Influence Plots
########################

"""
Prof. Chase:
    Influence plots are a method for visually inspecting how much
    influence and leverage an observation has on the goodness of fit
    line.
"""

# Influence plots based on Cook's Distance

lm_price_carat = smf.ols(formula = 'price ~ carat' , data = diamonds)

results = lm_price_carat.fit()


fig, ax = plt.subplots(figsize=(12,8))
fig = sm.graphics.influence_plot(results,
                                 ax = ax,
                                 criterion = 'cooks')


# See Footnote 5 for an explanation of the code above


# Setting axis limits
plt.xlim(0.00, 0.04)
plt.ylim(-8, 8)


# Adding horizontal lines
plt.axhline(y = 4,
            linestyle = '--',
            color ='red')


plt.axhline(y = -4,
            linestyle = '--',
            color = 'red')



plt.savefig("Diamond ~ Carat Outlier Influence Plot.png")

plt.show()



###############################################################################
# Multivariate Regression (1 of 2)
###############################################################################


########################
# Coding categorical variables
########################


lm_full = smf.ols(formula = """
                  price ~ 
                  carat +
                  clarity +
                  color +
                  cut +
                  C(channel) +
                  C(store) +
                  m_carat +
                  m_color +
                  m_clarity +
                  m_cut +
                  out_price +
                  out_carat +
                  out_clarity +
                  out_cut
                  """ , data = diamonds)


results = lm_full.fit()

print(results.summary())


# See Footnote 6 for an explanation of the code above



"""
Prof. Chase:
    Notice the 'C()' around our categorical variables. This is one way
    to code categorical variables for modeling so that Python knows to
    treat each category as a unique subset of the column. Also notice
    that some of our subsets are insignificant. This can be addressed
    via one-hot encoding, which is explained in the following section.
    
    Also notice that out_price has the third-highest coefficient. In a
    way, this is gaming our model as it can be interpreted as:
        
        "Really expensive diamonds are going to cost more."
    
    However, this is also informative, as it lets us know how much more
    we should expect to pay if a diamond is beyond our price threshold.
"""


########################
# One-hot Encoding
########################


"""
Prof. Chase:
    In the following, we are going to develop a binary matrix for our
    categorical variables using a technique called one-hot encoding.
    This will allow us to work with categorical variables in regression
    in Python.
"""


# Creating binary matricies for categorical variables
channel_dummies = pd.get_dummies(list(diamonds['channel']))
store_dummies = pd.get_dummies(list(diamonds['store']))



# concatenating binaries matricies with the diamonds dataset
diamonds_2 = pd.concat(
        [diamonds.loc[:,:],
         channel_dummies, store_dummies],
         axis = 1)


# See Footnote 7 for an explanation of the code above



###############################################################################
# Multivariate Regression (2 of 2)
###############################################################################


lm_one_hot = smf.ols(formula = """
                  price ~ 
                  carat +
                  clarity +
                  color +
                  cut +
                  independent +
                  mall +
                  online + 
                  Ashford +
                  diamonds_2["Ausman's"] +
                  diamonds_2["Blue Nile"] +
                  Danford +
                  diamonds_2["Fred Meyer"] +
                  diamonds_2["Goodman's"] +
                  Kay +
                  diamonds_2["R. Holland"] +
                  diamonds_2["Riddle's"] +
                  University +
                  Zales +
                  m_carat +
                  m_clarity +
                  m_cut +
                  out_price +
                  out_carat +
                  out_cut
                  """ , data = diamonds_2)


results = lm_one_hot.fit()

print(results.summary())


# See Footnote 7 for an explanation of the code above



"""
Prof. Chase:
    It looks like there are some stores with unacceptable p-values.
    Let's group these into a group called "other store" and see if it
    adds any value.
"""



########################
# Grouping Stores with High p-values
########################

other_store = diamonds_2[[
        "Ashford",
        "Ausman's",
        "Blue Nile",
        "Kay",
        "University"]]


diamonds_2['other_store'] = 0



# sum of other store values
diamonds_2['other_store'] = (diamonds_2["Ashford"] +
                             diamonds_2["Ausman's"] +
                             diamonds_2["Blue Nile"] +
                             diamonds_2["Kay"] +
                             diamonds_2["University"])



# a more efficient way to do this is as follows
diamonds_2['other_store'] = other_store.sum(axis = 1)



########################
# Modeling with Other Store and no m_clarity
########################

lm_one_hot_2 = smf.ols(formula = """
                  price ~ 
                  carat +
                  clarity +
                  color +
                  cut +
                  independent +
                  mall +
                  online + 
                  Danford +
                  diamonds_2["Fred Meyer"] +
                  diamonds_2["Goodman's"] +
                  diamonds_2["R. Holland"] +
                  diamonds_2["Riddle's"] +
                  Zales +
                  other_store +
                  m_carat +
                  m_cut +
                  out_price +
                  out_carat +
                  out_cut
                  """ , data = diamonds_2)

results = lm_one_hot_2.fit()


print(results.summary())


"""
Prof. Chase:
    Notice how this changed the significance of other variables. This
    is related to the concept called variance inflation. Also, our new
    variable 'other_store' not significant based on its p-value.
    
    Now we are at a crossroads. If we take out stores that are
    insignificant, we will lose interpretability in our model. However,
    if we include insignificant variables, we will be adding noise.
    
    I'm going to take the approach of removing all store variables from
    the model as I feel that we have enough information/insights by
    simply reducing the granularity to online channels
"""

########################
# Modeling without Store
########################

lm_no_store = smf.ols(formula = """
                  price ~ 
                  carat +
                  clarity +
                  color +
                  cut +
                  independent +
                  mall +
                  online +
                  m_carat +
                  m_clarity +
                  m_cut +
                  out_price +
                  out_carat +
                  out_cut
                  """ , data = diamonds_2)


results = lm_no_store.fit()

print(results.summary())


"""
Prof. Chase:
    There is definitely a model with stronger predictive power. However,
    the 'no_store' model is interpretable. Reducing the complexity of a
    model is also known as taking a parsimonious approach. This
    approach is ideal when our goal is to gain insights as opposed to
    pure predictive accuracy.
"""



###############################################################################
# Returning to Residual and Outlier Analysis
###############################################################################


########################
# Visual Residual Analysis
########################

"""
Prof. Chase:
    As we are running multivariate regression, we need to delete the
    goodness of fit line to run our regression plots.
"""


# Below is a command for setting a large plot size
fig, ax = plt.subplots(figsize=(12,8))



# Plotting the residuals
figure = smg.regressionplots.plot_fit(results = results,
                                      exog_idx = 'carat',
                                      ax = ax)




plt.legend(loc = 'lower right')

plt.savefig('Price ~ Carat Predicted v. Actual Diamond Values.png')

plt.show()



########################
# Bonferroni outlier test
########################

test = results.outlier_test()

print('Bad data points (bonf(p) < 0.05):')
print(test[test.iloc[:, 2] < 0.05])



# Let's investigate these outliers further
outlier_list = [209, 210, 380]

bonf_outliers = diamonds.iloc[outlier_list, : ]

print(bonf_outliers)



# Dropping the missing and outlier columns
bonf_outliers = bonf_outliers.iloc[:, 0:8]

print(bonf_outliers)



# Adding predicted_price
pred_val = results.fittedvalues.iloc[outlier_list]

bonf_outliers['pred_price'] = pred_val

print(bonf_outliers)


# We can append the means to our DataFrame with .append()
bonf_outliers = bonf_outliers.append(diamonds.iloc[:, 0:8].mean(),
                                     ignore_index = True)


print(bonf_outliers)



# We can fix the missing pred_price with the following code
bonf_outliers.loc[3, 'pred_price'] = results.fittedvalues.mean()



# Rounding to two decimal places
bonf_outliers = round(bonf_outliers, 2)

print(bonf_outliers)



########################
# Influence Plots
########################

results = lm_no_store.fit()


fig, ax = plt.subplots(figsize=(12,8))
fig = sm.graphics.influence_plot(results,
                                 ax = ax,
                                 criterion = 'cooks')

plt.xlim(0.00, 0.05)
plt.ylim(-8, 8)



# Adding horizontal lines
plt.axhline(y = 4,
            linestyle = '--',
            color ='red')


plt.axhline(y = -4,
            linestyle = '--',
            color = 'red')



plt.savefig("Diamond Model Influence Plot.png")

plt.show()



# Investigating
residuals_df = residuals.round(2).abs()

residuals_df = predict_df.sort_values(by = 'Abs_Residuals', ascending = False)

print(residuals_df)



###############################################################################
# Saving things for future use
###############################################################################

diamonds = pd.concat(
        [diamonds.loc[:,:],
         channel_dummies, store_dummies],
         axis = 1)


diamonds.to_excel('diamonds_wide.xlsx', index = False)



"""
###############################################################################
# Footnotes
###############################################################################


Footnote 0: the purpose of footnotes

to give a line-by-line explanation of a code snippet


*******************************************************************************


Footnote 1: multiple plots with sns.lmplot

my_plot =                                # setting a new object called my_plot
sns.lmplot(                              # calling sns.lmplot
x = 'carat',                             # with carat on the x-axis
y = 'price',                             # and price on the y-axis
data = diamonds,                         # from the diamonds dataset
hue = 'channel',                         # using channel for color-coding
col = 'channel',                         # and breaking up the plots so each one represents a different channel
col_wrap = 2,                            # with a total of 2 columns
scatter_kws= {"marker": "D", "s": 10},   # specifiying custom formatting
palette = 'nipy_spectral')               # setting the color theme to nipy_spectral


my_plot.set_axis_labels("", "Price")     # setting the y-axis to price for all plots


plt.tight_layout()                                    # cleaning up the layout
plt.savefig("Price ~ Carat|Channel Regression.png")   # saving the figure
plt.show()                                            # ...and displaying the plot


*******************************************************************************


Footnote 2: building a prediction function

def price_pred():                                                        # defining a function with no arguments
\"""Predicts price based on the carat weight. \"""                       # docstring
    
import statsmodels.formula.api as smf                                    # importing smf WITHIN the function so that it is more likely to work on external scripts

results = smf.ols(formula = 'price ~ carat',                             # defining the model
                      data = diamonds).fit()
    
carat_weight = int(input("Input carat weight > "))                       # locally defining carat weight

pred_price = results.params[0] + results.params[1] * carat_weight        # locally defining pred_price

print(f\"""                                                              # writing an output using an f string
      
A diamond of that size will cost approximately {round(pred_price, 2)}.  

\""")

price_pred()                                                             # calling the function


*******************************************************************************


Footnote 3: expanding the prediction function

def price_pred_rng(carat_weight):                                   # defining a function with one argument
\"""Predicts price based on the carat weight.\"""                   # docstring
    
import statsmodels.formula.api as smf                               # importing smf WITHIN the function so that it is more likely to work on external scripts
    
results = smf.ols(formula = 'price ~ carat',                        # defining the model
                      data = diamonds).fit()                            
    
pred_price = results.params[0] + results.params[1] * carat_weight   # locally defining pred_price

lower_95 = (                                                        # locally defining lower_95
results.conf_int().iloc[0,0] +                                      # which takes the intercept
results.conf_int().iloc[1,0] *                                      # and the coefficient for carat_weight
carat_weight)                                                       # times carat weight
    
upper_95 = (results.conf_int().iloc[0,1] +                          # locally defining upper_95 (similar to lower_95)
                results.conf_int().iloc[1,1] *                      
                carat_weight)                                       
    
    print(f\"""                                                     # writing an output using an f string
      
A diamond of that size will cost approximately between {round(lower_95, 2)} and
{round(upper_95, 2)}. The best estimate for that size is {round(pred_price, 2)}.

     \""")

price_pred_rng(2)                                                   # calling the function


*******************************************************************************


Footnote 4: customizations to regressionplots

fig, ax = plt.subplots(figsize=(12,8))   # setting the axis window (unpacking fig and ax)


figure =                                 # creating a new object called figure
smg.regressionplots                      # calling the sns.regressionplots sub-package
.plot_fit(                               # calling the plot_fit function
results = results,                       # setting results equal to our previously-defined model output: results
exog_idx = 'carat',                      # basing this on the variable carat (exog_idx will allow you to define one of the variables in a regression if multiple are stated in the model)
ax = ax)                                 # setting the axis (ax) to the unpacked variable ax from above


line =                                   # creating a new object called line
smg.regressionplots                      # calling the sns.regressionplots sub-package
.abline_plot(                            # calling the abline_plot function
model_results = results,                 # setting results equal to our previously-defined model output: results
ax = figure.axes[0])                     # setting the figure axes to what is in position 0

plt.legend(loc = 'lower right')          # setting the legend to appear in the lower right

plt.savefig('Price ~ Carat Predicted v. Actual Diamond Values.png')   # saving the figure

plt.show()                                                            # ...and displaying the plot


*******************************************************************************


Footnote 5: utilizing sm.graphics.influence_plot

lm_price_carat =                         # defining a new object lm_price_carat
smf.ols(                                 # calling smf.ols for ols regression
formula = 'price ~ carat',               # specifying the formula
data = diamonds)                         # ...and using the diamonds dataset

results =                                # defining a new object called results
lm_price_carat.fit()                     # set to our lm_price_carat object .fit


fig, ax =                                # unpacking fig and ax from plt.subplots
plt.subplots(figsize=(12,8))             # and setting the plot window to 12 x 8 

fig =                                    # defining a new object called fig
sm.graphics.influence_plot(              # calling sm.graphics.influence_plot
results,                                 # on results
ax = ax,                                 # with ax set to the unpacked ax above
criterion = 'cooks')                     # and setting the influence criterion to Cook's Distance


*******************************************************************************


Footnote 6: ols regression modeling using smf.ols

lm_full =                                   # creating a new object called lm_full 
smf.ols(formula = \"""                      # calling smf.ols and specifying the formula
                  price ~                   # setting price as the dependent variable
                  carat +                   # ...and the following independent variables
                  clarity +
                  color +
                  cut +
                  C(channel) +
                  C(store) +
                  m_carat +
                  m_color +
                  m_clarity +
                  m_cut +
                  out_price +
                  out_carat +
                  out_clarity +
                  out_cut
                  \""" , data = diamonds)   # ...from the diamonds dataset


results = lm_full.fit()                     # creating a new object called results based on lm_full using .fit

print(results.summary())                    # printing the model result summary


*******************************************************************************


Footnote 8: one-hot encoding


channel_dummies =                        # creating a new object called channel_dummies
pd.get_dummies(                          # calling pd.get_dummies for one-hot encoding
list(diamonds['channel']))               # ...by feeding in each unique channel as a list


store_dummies =                          # creating a new object called store_dummies
pd.get_dummies(                          # calling pd.get_dummies for one-hot encoding
list(diamonds['store']))                 # ...by feeding in each unique store as a list


diamonds_2 =                             # creating a new DataFrame called diamonds_2
pd.concat(                               # calling pd.concat to add the one-hot encoded variables to the othe data in diamonds
[diamonds.loc[:,:],                      # ...by calling all columns and all rows in diamonds
channel_dummies, store_dummies],         # ... and concatenating with channel_dummies and sotre_dummies
axis = 1)                                # specifying axis = 1 so that concatenation occurs as columns


*******************************************************************************


Footnote 8: ols regression with one-hot encoding

lm_one_hot = smf.ols(formula = \"""              # Very similar to Footnote 7
                  price ~ 
                  carat +
                  clarity +
                  color +
                  cut +
                  independent +
                  mall +
                  online + 
                  Ashford +
                  diamonds_2["Ausman's"] +       # ...but calling specific stores based on one-hot encoding
                  diamonds_2["Blue Nile"] +
                  Danford +
                  diamonds_2["Fred Meyer"] +
                  diamonds_2["Goodman's"] +
                  Kay +
                  diamonds_2["R. Holland"] +
                  diamonds_2["Riddle's"] +
                  University +
                  Zales +
                  m_carat +
                  m_clarity +
                  m_cut +
                  out_price +
                  out_carat +
                  out_cut
                  \""" , data = diamonds_2)


results = lm_one_hot.fit()

print(results.summary())


"""