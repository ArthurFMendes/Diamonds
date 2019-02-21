#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 02:36:22 2018

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

file ='diamonds_flagged.xlsx'
diamonds = pd.read_excel(file)


###############################################################################
# Correlation analysis
###############################################################################


# We can find the correlation between two variables using np.corrcoef
y = pd.np.corrcoef(diamonds['price'],
                   diamonds['carat']).round(2)

print(y)



# We can generate a single correlation coefficient by specifying [1, 0] 
pd.np.corrcoef(diamonds['price'],
               diamonds['carat'])[1,0].round(2)


# See Footnote 1 for an explanation of the code above


"""
Use the space below to check other correlations with pd.np.corrcoef
"""



########################
# Correlation matricies
########################

df_corr = diamonds.corr().round(2)

print(df_corr)

# Sending df_corr to Excel
df_corr.to_excel("diamond_corr_matrix.xlsx")



"""
Let's focus on how price relates to other variables. We can do so with
the code below.
"""

df_corr.loc['price'].sort_values(ascending = False)


#######################
# Heatmaps
########################

sns.heatmap(df_corr,
            cmap = 'Blues',
            square = True,
            annot = False,
            linecolor = 'black',
            linewidths = 0.5)


plt.savefig('Diamond Correlation Heatmap.png')
plt.show()


# See Footnote 2 for an explanation of the code above


"""
Prof. Chase:
    More info on cmap themes can be found here:
    https://matplotlib.org/examples/color/colormaps_reference.html
"""

# Using palplot to view a color scheme
sns.palplot(sns.color_palette('coolwarm', 12))

fig, ax = plt.subplots(figsize=(15,15))

sns.heatmap(df_corr,
            cmap = 'coolwarm',
            square = True,
            annot = True,
            linecolor = 'black',
            linewidths = 0.5)


plt.savefig('Diamond Correlation Heatmap 2.png')
plt.show()


########################
# Scatterplots
########################

# carat and price
plt.scatter(x = 'carat',
            y = 'price',
            alpha = 0.7,
            cmap = 'bwr',
            data = diamonds)


plt.xlabel('Carat Weight')
plt.ylabel('Price')
plt.grid(True)
plt.show()


# See Footnote 3 for an explanation of the code above



# color and price
plt.scatter(x = 'color',
            y = 'price',
            alpha = 0.3,
            cmap = 'bwr',
            data = diamonds)


plt.xlabel('Color')
plt.ylabel('Price')
plt.grid(True)
plt.show()


########################
# Adding subplots
########################

plt.subplot(2, 2, 1)

plt.scatter(x = 'carat',
            y = 'price',
            alpha = 0.7,
            color = 'red',
            data = diamonds)


plt.title('Carat Weight')
plt.ylabel('Price')
plt.grid(True)



########################



plt.subplot(2, 2, 2)

plt.scatter(x = 'color',
            y = 'price',
            alpha = 0.7,
            color = 'blue',
            data = diamonds)


plt.title('Color')
plt.grid(True)



########################



plt.subplot(2, 2, 3)

plt.scatter(x = 'clarity',
            y = 'price',
            alpha = 0.7,
            color = 'magenta',
            data = diamonds)


plt.title('Clarity')
plt.ylabel('Price')
plt.grid(True)



########################



plt.subplot(2, 2, 4)

plt.scatter(x = 'cut',
            y = 'price',
            alpha = 0.7,
            color = 'brown',
            data = diamonds)


plt.title('Cut')
plt.grid(True)
plt.tight_layout()
plt.savefig('Diamond Data Scatterplots.png')
plt.show()



########################
# Pairplots
########################

# let's pick up the pace with pairplot
sns.pairplot(diamonds)
plt.show()



# this can be further focused using subsetting
diamonds_sel = diamonds.loc[:,['price', 'carat', 'color', 'clarity', 'cut']]
sns.pairplot(data = diamonds_sel)
plt.tight_layout()
plt.show()



# and further using hue
sns.pairplot(data = diamonds,
             x_vars = ['price', 'carat', 'color', 'clarity', 'cut'],
             y_vars = ['price', 'carat', 'color', 'clarity', 'cut'],
             hue = 'channel', palette = 'plasma')


plt.tight_layout()
plt.savefig('Diamond Data Pairplot.png')
plt.show()



# Filtering to focus on their relationship with price
sns.pairplot(data = diamonds,
             x_vars = ['carat', 'color', 'clarity', 'cut'],
             y_vars = ['price'],
             hue = 'channel', palette = 'plasma')


plt.tight_layout()
plt.savefig('Diamond Price Pairplot.png')
plt.show()


# See Footnote 4 for an explanation of the code above



"""
Prof. Chase:
    sns.pairplot() can be slow on large datasets
"""


###############################################################################
# Do prices vary by store?
###############################################################################

sns.lmplot(x = 'carat',
           y = 'price',
           data = diamonds,
           fit_reg = False,
           hue= 'store',
           scatter_kws= {"marker": "D", 
                        "s": 30},
           palette = 'plasma')

plt.title("Price and Carat by Store")
plt.grid()
plt.tight_layout()
plt.show()


# See Footnote 5 for an explanation of the code above



# it's hard to tell because the scatterplot is too crowded
# let's break it down by channel


########################
# Relabeling channels and stores
########################

"""
Prof. Chase:
    Let's relabel our channels and stores with actual names. It is a
    bad practice to use numbers for categorical variables as it can
    likely lead to mistakes (i.e. treating our variables as ordinal
    data as opposed to categorical data).
    
    We can use .map to help us.
""" 


# Using dictionaries to make new labels for categorical variables
diamonds['channel'] = diamonds['channel'].map(
        {0: 'mall',
         1: 'independent',
         2: 'online'})

    
print(diamonds['channel'])


# See Footnote 6 for an explanation of the code above



diamonds['store'] = diamonds['store'].map(
        {1: "Goodman's",
         2: "Chalmer's",
         3: "Fred Meyer",
         4: 'R. Holland',
         5: "Ausman's",
         6: "University",
         7: "Kay",
         8: "Zales",
         9: "Danford",
         10: "Blue Nile",
         11: "Ashford"})


    
print(diamonds['store'])



# Creating seperate datasets for each channel
mall_df = diamonds[diamonds['channel'] == 'mall']

independent_df = diamonds[diamonds['channel'] == 'independent']

online_df = diamonds[diamonds['channel'] == 'online']


########################
# Shopping malls
########################

sns.lmplot(x = 'carat',
           y = 'price',
           data = mall_df,
           fit_reg = False,
           hue= 'store',
           scatter_kws= {"marker": "D", 
                        "s": 30},
           palette = 'plasma')


plt.title("Shopping Malls")
plt.grid()
plt.tight_layout()
plt.show()



########################
# Independent shops
########################

sns.lmplot(x = 'carat',
           y = 'price',
           data = independent_df,
           fit_reg = False,
           hue= 'store',
           scatter_kws= {"marker": "D", 
                        "s": 30},
           palette = 'plasma')


plt.title("Independent")
plt.grid()
plt.tight_layout()
plt.show()



########################
# Online stores
########################

sns.lmplot(x = 'carat',
           y = 'price',
           data = online_df,
           fit_reg = False,
           hue= 'store',
           scatter_kws= {"marker": "D", 
                        "s": 30},
           palette = 'plasma')


plt.title("Online")
plt.grid()
plt.tight_layout()
plt.show()



########################
# Violin plots
########################

"""
Prof. Chase:
    Violin plots are a hybrid between boxplots and histograms.
"""

sns.violinplot(x = 'store',
               y = 'price',
               data = mall_df,
               orient = 'v')

plt.show()


########################


sns.violinplot(x = 'store',
               y = 'price',
               data = independent_df,
               orient = 'v')

plt.show()


########################


sns.violinplot(x = 'store',
               y = 'price',
               data = online_df,
               orient = 'v')

plt.show()


# Goodman's distribution looks very similar to the online retailers.
# let's investigate.

online_goodman = online_df.append(
        independent_df[independent_df['store'] == "Goodman's"])



sns.violinplot(x = 'store',
               y = 'price',
               data = online_goodman,
               orient = 'v')

plt.show()


"""
Prof. Chase:
    The distributions via violin plots look similar. However,
    distributions can be misleading as they are dependent on the
    number of observations in the dataset.
    
    Let's investigate further using a hybrids of different plots.
"""


########################
# Hybrid plots
########################

# We empty the violin plot with the optional argument 'fill'
sns.violinplot(x = 'store',
               y = 'price',
               data = online_goodman,
               orient = 'v',
               inner = None,
               color = 'white')



# We can use stripplots to visualize the datapoints
sns.stripplot(x = 'store',
              y = 'price',
              data = online_goodman,
              jitter = True,
              size = 5,
              orient = 'v')


plt.show()


# See Footnote 7 for an explanation of the code above



########################

"""
Prof. Chase:
    This may be more visually dramatic if we utilized swarmplots to
    fill in the values.
"""

sns.violinplot(x = 'store',
               y = 'price',
               data = online_goodman,
               orient = 'v',
               inner = None,
               color = 'white')



sns.swarmplot(x = 'store',
              y = 'price',
              data = online_goodman,
              size = 5,
              orient = 'v')
plt.show()



# Goodman's values v. online store values
n_ashford = len(diamonds[diamonds['store'] == "Ashford"])

n_blue_nile = len(diamonds[diamonds['store'] == "Blue Nile"])

n_goodmans = len(diamonds[diamonds['store'] == "Goodman's"])


print(f"""
Prof. Chase:
    Goodman's appeared to exhibit a similar distribution to online
    retailers in the violin plot. However, after looking deeper, this
    retailer only has {n_goodmans} datapoints. This is much less than
    Ashford (n = {n_ashford}) and Blue Nile (n = {n_blue_nile}) Given
    this, we may want
    to collect more data before concluding that Goodman's diamond
    prices are similar to that of online retailers.
""")


###############################################################################
# Saving things for future use
###############################################################################

diamonds.to_excel('diamonds_explored.xlsx', index = False)



"""
###############################################################################
# Footnotes
###############################################################################


Footnote 0: the purpose of footnotes

to give a line-by-line explanation of a code snippet


*******************************************************************************


Footnote 1: calling a single correlation coefficient
 
pd.np.corrcoef(                      # calling the corrcoef function from pd.np
diamonds['price'],                   # with price
diamonds['carat'])                   # and carat
[1,0]                                # ...and subsetting so that only one value is called instead of the entire matrix
.round(2)                            # ...and finally rounding to two decimal places


*******************************************************************************


Footnote 2: utilizing sns.heatmap

df_corr = diamonds.corr().round(2)   # creating a correlation matrix: df_corr

sns.heatmap(                         # calling sns.heatmap
df_corr,                             # ...on the matrix df_corr
cmap = 'Blues',                      # setting the color theme to 'Blues'
square = True,                       # making the plot print as a square
annot = False,                       # not displaying numbers in the boxes
linecolor = 'black',                 # setting line color (borders) to black
linewidths = 0.5)                    # setting line width (borders) to 0.5


plt.savefig('Diamond Correlation Heatmap.png')  # saving the figure
plt.show()                                      # ...and displaying the plot


*******************************************************************************


Footnote 3: utilizing sns.heatmap

df_corr = diamonds.corr().round(2)   # creating a correlation matrix: df_corr

sns.heatmap(                         # calling sns.heatmap
df_corr,                             # ...on the matrix df_corr
cmap = 'Blues',                      # setting the color theme to 'Blues'
square = True,                       # making the plot print as a square
annot = False,                       # not displaying numbers in the boxes
linecolor = 'black',                 # setting line color (borders) to black
linewidths = 0.5)                    # setting line width (borders) to 0.5


plt.savefig('Diamond Correlation Heatmap.png')  # saving the figure
plt.show()                                      # ...and displaying the plot


*******************************************************************************


Footnote 4: utilizing sns.pairplot

sns.pairplot(                                    # calling sns.pairplot
data = diamonds,                                 # using the diamonds dataset
x_vars = ['carat', 'color', 'clarity', 'cut'],   # with these variables on the x-axis
y_vars = ['price'],                              # and this variable on the y-axis
hue = 'channel',                                 # and also color-coding (hue) based on channel
palette = 'plasma')                              # using the plasma color theme

plt.tight_layout()                               # cleaning up the format of the plot
plt.savefig('Diamond Price Pairplot.png')        # saving the figure
plt.show()                                       # ...and displaying the plot


*******************************************************************************


Footnote 5: utilizing sns.lmplot

sns.lmplot(                             # calling sns.lmplot
x = 'carat',                            # with carat on the x-axis
y = 'price',                            # and price on the y-axis
data = diamonds,                        # using the diamonds dataset
fit_reg = False,                        # specifying not to create a regresion line
hue= 'store',                           # color-coding (hue) on store
scatter_kws= {"marker": "D",  "s": 30}, # using the folowing customizations for themes               
palette = 'plasma')                     # using the plasma color theme

plt.title("Price and Carat by Store")   # specifying a custom title
plt.grid()                              # specifying to plot gridlines
plt.tight_layout()                      # cleaning up the layout
plt.show()                              # ...and displaying the plot


*******************************************************************************


Footnote 6: mapping using a dictionary


diamonds['channel'] =                   # setting channel from diamonds
diamonds['channel'].map(                # using its old values and mapping them to new values
{                                       # wrapper to open a dictionary
0: 'mall',                              # channels with a value of 0 are now set to mall
1: 'independent',                       # channels with a value of 1 are now set to independent
2: 'online'                             # channels with a value of 2 are now set to online
})                                      # wrapper to close a dictionary and the function

    
print(diamonds['channel'])              # printing the new values of channel


*******************************************************************************


Footnote 7: mapping using a dictionary


sns.violinplot(                         # calling sns.violinplot
x = 'store',                            # with store on the x-axis
y = 'price',                            # and price on the y-axis
data = online_goodman,                  # using the online_goodman dataset
orient = 'v',                           # specifying vertical alignment
inner = None,                           # specifying no fill
color = 'white')                        # ...and a white background

                                        # notice how there's no plt.show() here

sns.stripplot(                          # calling sns.stripplot
x = 'store',                            # with store on the x-axis
y = 'price',                            # and price on the y-axis
data = online_goodman,                  # using the online_goodman dataset
jitter = True,                          # specifying jitter = True so that we can see overlapping data points more clearly
size = 5,                               # specifying the size of each data point
orient = 'v')                           # specifying vertical alignment


plt.show()                              # ...and displaying the plot

*******************************************************************************
"""