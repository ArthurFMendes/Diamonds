#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: ArthurFMendes

Purpose:
    This code is meant to treat outliers in the diamond dataset
"""


###############################################################################
# Importing libraries and base dataset
###############################################################################
import pandas as pd # data science essentials
import matplotlib.pyplot as plt # data visualization
import seaborn as sns # more data visualization

file ='diamonds_imputed.xlsx'
diamonds = pd.read_excel(file)



###############################################################################
# Outlier detection using quantile techniques
###############################################################################

# Using describe() for distribution analysis 
diamonds.describe()


# We can also use .quantile to set our own parameters for
# distribution analysis
diamonds[['carat',
          'color',
          'clarity',
          'cut',
          'price']].quantile([0.20,
                              0.40,
                              0.60,
                              0.80,
                              1.00])



###############################################################################
# Outlier detection using boxplots
###############################################################################

# Using boxplots for distribution analysis

# A basic boxplot
diamonds.boxplot(column = ['carat'])



# A boxplot that's segmented
diamonds.boxplot(column = ['carat'],
                  by = 'channel',)



# A more advanced boxplot that segmented
diamonds.boxplot(column = ['carat'],
                 by = 'channel',
                 vert = False,
                 manage_xticks = True,
                 patch_artist = False,
                 meanline = True,
                 showmeans = True)


plt.title("Carat by Channel")
plt.suptitle("")

plt.show()



# ...and a more advanced set of boxplots

# carat
diamonds.boxplot(column = ['carat'],
                 by = 'channel',
                 vert = False,
                 patch_artist = True,
                 meanline = True,
                 showmeans = True)



plt.suptitle('')
plt.tight_layout()
plt.savefig('Carat by Channel Boxplot.png')
plt.show()



# color
diamonds.boxplot(column = ['color'],
                 by = 'channel',
                 vert = False,
                 patch_artist = True,
                 meanline = True,
                 showmeans = True)


plt.suptitle('')
plt.tight_layout()
plt.show()



# clarity
diamonds.boxplot(column = ['clarity'],
                 by = 'channel',
                 vert = False,
                 patch_artist = True,
                 meanline = True,
                 showmeans = True)

plt.suptitle('')
plt.tight_layout()
plt.show()



# cut
diamonds.boxplot(column = ['cut'],
                 by = 'channel',
                 vert = False,
                 patch_artist = True,
                 meanline = True,
                 showmeans = True)

plt.suptitle('')
plt.tight_layout()
plt.show()



# carat, color, clarity, and cut
diamonds.boxplot(column = ['carat', 'color', 'clarity', 'cut'],
                 vert = False,
                 manage_xticks = True,
                 patch_artist = False,
                 meanline = True,
                 showmeans = True,
                 )


plt.title("Boxplots for Carat, Color, Clarity, and Cut")

plt.show()



###############################################################################
# Using matplotlib.pyplot
###############################################################################

plt.boxplot(x = 'price',
            data = diamonds,
            vert = False,
            patch_artist = False,
            meanline = True,
            showmeans = True)


plt.xlabel("Price")
plt.show()



###############################################################################
# Refining outlier detection with histograms
###############################################################################

# Using pandas
diamonds['price'].hist()

plt.xlabel("Price")
plt.show()



# Using matplotlib.pyplot
plt.hist(x = 'price',
            data = diamonds)

plt.xlabel("Price")
plt.show()



########################

plt.hist(x = 'price',
         data = diamonds,
         bins = 'fd',
         cumulative = True,
         histtype = 'step'
         )


plt.xlabel("Price")
plt.show()

########################

plt.hist(x = 'price',
         data = diamonds,
         bins = 'fd',
         cumulative = False,
         histtype = 'barstacked',
         orientation = 'horizontal'
         )


plt.xlabel("Price")
plt.show()



########################
########################

plt.subplot(2, 1, 1)
plt.hist(x = 'price',
         data = diamonds,
         bins = 'fd',
         cumulative = False,
         log = False,
         color = 'black',
         label = 'Log Price'
         )


plt.xlabel("Price")
plt.show()



########################

plt.subplot(2, 1, 2)
plt.hist(x = 'price',
         data = diamonds,
         bins = 'fd',
         cumulative = False,
         log = True,
         color = 'purple',
         label = 'Log Price'
         )


plt.xlabel("Price")
plt.show()



###############################################################################
# Refining graphical displays with seaborn
###############################################################################

# Basic histogram with sns.distplot
sns.distplot(diamonds['price'])

plt.show()


########################

# Customizing with sns.distplot
plt.subplot(2, 2, 1)
sns.distplot(diamonds['price'],
             bins = 'fd',
             color = 'g')

plt.xlabel('Price')



########################

plt.subplot(2, 2, 2)
sns.distplot(diamonds['carat'],
             bins = 'fd',
             color = 'y')

plt.xlabel('Carat')



########################

plt.subplot(2, 2, 3)
sns.distplot(diamonds['color'],
             bins = 17,
             kde = False,
             rug = True,
             color = 'orange')

plt.xlabel('Color')



########################

plt.subplot(2, 2, 4)

sns.distplot(diamonds['clarity'],
             bins = 17,
             kde = False,
             rug = True,
             color = 'r')


plt.xlabel('Clarity')

plt.tight_layout()
plt.savefig('Diamond Data Histograms 1 of 3.png')

plt.show()



########################
########################

plt.subplot(2, 2, 1)
sns.distplot(diamonds['cut'],
             kde = False,
             rug = True,
             color = 'navy')

plt.xlabel('Cut')



########################

plt.subplot(2, 2, 2)
sns.distplot(diamonds['store'],
             bins = 25,
             kde = False,
             color = 'maroon')

plt.xlabel('Store')



########################

plt.subplot(2, 2, 3)
sns.distplot(diamonds['channel'],
             bins = 8,
             kde = False,
             color = 'gold')

plt.xlabel('Channel')

plt.tight_layout()
plt.savefig('Diamond Data Histograms 2 of 3.png')

plt.show()



###############################################################################
# Outlier cutoff notes (exclusive)
###############################################################################

price_limit_hi = 12500

carat_limit_0 = 2.03

carat_limit_1 = 1.25

carat_limit_2 = 1.5

color_limit_hi = 7

clarity_limit_lo = 3

clarity_limit_hi = 9



########################
# Histograms with cutoff points
########################

########################

# Customizing with sns.distplot
plt.subplot(2, 2, 1)
sns.distplot(diamonds['price'],
             bins = 35,
             color = 'g')

plt.xlabel('Price')



plt.axvline(x = price_limit_hi,
            label = 'Outlier Thresholds',
            linestyle = '--')



########################

plt.subplot(2, 2, 2)
sns.distplot(diamonds['carat'],
             bins = 30,
             color = 'y')

plt.xlabel('Carat')



plt.axvline(x = carat_limit_0,
            linestyle = '--',
            color = 'purple')

plt.axvline(x = carat_limit_1,
            linestyle = '--',
            color = 'red')

plt.axvline(x = carat_limit_2,
            linestyle = '--',
            color = 'red')



########################

plt.subplot(2, 2, 3)
sns.distplot(diamonds['color'],
             bins = 17,
             kde = False,
             rug = True,
             color = 'orange')



plt.axvline(x = color_limit_hi,
            linestyle = '--')

plt.xlabel('Color')



########################

plt.subplot(2, 2, 4)

sns.distplot(diamonds['clarity'],
             bins = 17,
             kde = False,
             rug = True,
             color = 'r')

plt.xlabel('Clarity')



plt.axvline(x = clarity_limit_lo,
            linestyle = '--')

plt.axvline(x = clarity_limit_hi,
            linestyle = '--')



plt.tight_layout()
plt.savefig('Diamond Data Histograms 3 of 3.png')



plt.show()



###############################################################################
# Flagging outliers
###############################################################################

diamonds = pd.read_excel(file)


########################
# price
########################

# Writing a variable for outlier flags
diamonds['out_price'] = 0


# Building a for loop
for val in enumerate(diamonds.loc[ : , 'price']):
    
    if val[1] > price_limit_hi:
        diamonds.loc[val[0], 'out_price'] = 1



# Checking to see how many outliers were flagged
diamonds['out_price'].abs().sum()
    

check = (diamonds.loc[ : , ['price', 'out_price']]
                             .sort_values('price',
                                          ascending = False))


for val in enumerate(diamonds['price']):
    
    if val[1] > price_limit_hi:
        diamonds['out_price'][val[0]] = 1


diamonds['out_price'].abs().sum()



########################
# A more surgical approach to outlier flagging
########################

########################
# carat
########################


diamonds['out_carat'] = 0


for val in enumerate(diamonds.loc[ : , 'carat']):
    
    if diamonds.loc[val[0], 'channel'] == 0 and val[1] > carat_limit_0:
        
        diamonds.loc[val[0], 'out_carat'] = 1



for val in enumerate(diamonds.loc[ : , 'carat']):

    if diamonds.loc[val[0], 'channel'] == 1 and val[1] > carat_limit_1:
        
        diamonds.loc[val[0], 'out_carat'] = 1



for val in enumerate(diamonds.loc[ : , 'carat']):
    
    if diamonds.loc[val[0], 'channel'] == 2 and val[1] > carat_limit_2:
        
        diamonds.loc[val[0], 'out_carat'] = 1


        

diamonds['out_carat'].abs().sum()


check = (diamonds.loc[ : , ['channel', 'carat', 'out_carat']]
                             .sort_values(['channel', 'carat'],
                                          ascending = False))

########################
# clarity
########################

diamonds['out_clarity'] = 0


for val in enumerate(diamonds.loc[ : , 'clarity']):
    
    if val[1] < clarity_limit_lo:
        diamonds.loc[val[0], 'out_clarity'] = 1



for val in enumerate(diamonds.loc[ : , 'clarity']):
    
    if val[1] > clarity_limit_hi:
        diamonds.loc[val[0], 'out_clarity'] = 1



diamonds['out_clarity'].abs().sum()


check = (diamonds.loc[ : , ['clarity', 'out_clarity']]
                             .sort_values(['clarity'],
                                          ascending = False))



########################
# color
########################

diamonds['out_color'] = 0


# Building a for loop
for val in enumerate(diamonds.loc[ : , 'color']):
    
    if val[1] > color_limit_hi:
        diamonds.loc[val[0], 'out_color'] = 1



# Checking to see how many outliers were flagged
diamonds['out_color'].abs().sum()
    

check = (diamonds.loc[ : , ['color', 'out_color']]
                             .sort_values('color',
                                          ascending = False))





########################
# cut
########################

diamonds['out_cut'] = 0



for val in enumerate(diamonds.loc[ : , 'cut']):
    
    if val[1] == 1:
        diamonds.loc[val[0], 'out_cut'] = 1



diamonds['out_cut'].abs().sum()



check = (diamonds.loc[ : , ['cut', 'out_cut']]
                             .sort_values(['cut'],
                                          ascending = False))




########################
# Analyzing outlier flags
########################

diamonds['out_sum'] = (diamonds['out_price']   +
                       diamonds['out_carat']   +
                       diamonds['out_clarity']   +
                       diamonds['out_color'] +
                       diamonds['out_cut'])




check = (diamonds.loc[ : , ['out_sum',
                            'out_price',
                            'out_carat',
                            'out_clarity',
                            'out_color',
                            'out_cut']].sort_values(['out_sum'],
                                          ascending = False))



###############################################################################
# Saving things for future use
###############################################################################

diamonds.to_excel('diamonds_flagged.xlsx', index = False)


