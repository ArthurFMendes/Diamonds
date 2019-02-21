
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



########################
# Correlation matricies
########################

df_corr = diamonds.corr().round(2)

print(df_corr)

# Sending df_corr to Excel
df_corr.to_excel("diamond_corr_matrix.xlsx")


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



# it's hard to tell because the scatterplot is too crowded
# let's break it down by channel


########################
# Relabeling channels and stores
########################

# Using dictionaries to make new labels for categorical variables
diamonds['channel'] = diamonds['channel'].map(
        {0: 'mall',
         1: 'independent',
         2: 'online'})

    
print(diamonds['channel'])



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

online_goodman = online_df.append(
        independent_df[independent_df['store'] == "Goodman's"])



sns.violinplot(x = 'store',
               y = 'price',
               data = online_goodman,
               orient = 'v')

plt.show()



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
