
"""
@author: ArthurFMendes

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
    Visual regression analysis is generally done to help us observe
    which may be a good fit for linear regression.
    
    Use this area to test other variables using sns.lmplot
"""



###############################################################################
# Plotting Residuals
###############################################################################

"""
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

# We can refine our fuction using confidence intervals.
results.conf_int()


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



###############################################################################
# Advanced Regression Techniques - Regression Outliers
###############################################################################

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

# Influence plots based on Cook's Distance

lm_price_carat = smf.ols(formula = 'price ~ carat' , data = diamonds)

results = lm_price_carat.fit()


fig, ax = plt.subplots(figsize=(12,8))
fig = sm.graphics.influence_plot(results,
                                 ax = ax,
                                 criterion = 'cooks')


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



########################
# One-hot Encoding
########################


# Creating binary matricies for categorical variables
channel_dummies = pd.get_dummies(list(diamonds['channel']))
store_dummies = pd.get_dummies(list(diamonds['store']))



# concatenating binaries matricies with the diamonds dataset
diamonds_2 = pd.concat(
        [diamonds.loc[:,:],
         channel_dummies, store_dummies],
         axis = 1)


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


###############################################################################
# Returning to Residual and Outlier Analysis
###############################################################################


########################
# Visual Residual Analysis
########################


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
