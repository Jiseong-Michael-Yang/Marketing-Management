# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 06:00:22 2018

@author: Jiseong Yang
"""

#%% Marketing Mix Regression.
import Lego_preprocessing as pp
import Lego_perceptual_map as pm
import matplotlib.pyplot as plt

# Correlation heatmap.
#mix_corr = pp.mix.corr()
#plt.matshow(mix_corr.corr())
#plt.xticks(range(len(mix_corr.columns)), mix_corr.columns, rotation = 90)
#plt.yticks(range(len(mix_corr.columns)), mix_corr.columns)
#plt.colorbar()
#plt.show()

#%% Mean Compare
import numpy as  np
import pandas as pd
from scipy import stats as st

# Create a table with mean of each mixes.
# Mean
mix_overall_mean = np.mean(pp.mix.iloc[:,-1])
mix_product_mean_total = np.mean(np.mean(pp.mix_product))
mix_price_mean_total = np.mean(np.mean(pp.mix_price))
mix_place_mean_total = np.mean(np.mean(pp.mix_place))
mix_promotion_mean_total = np.mean(np.mean(pp.mix_promotion))

mix_product_mean = pd.DataFrame(np.mean(pp.mix_product)).T
mix_product_mean.insert(column = "product_mean", value = mix_product_mean_total, loc = 4)

mix_price_mean = pd.DataFrame(np.mean(pp.mix_price)).T
mix_price_mean.insert(column = "price_mean", value = mix_price_mean_total, loc = 4)

mix_place_mean = pd.DataFrame(np.mean(pp.mix_place)).T
mix_place_mean.insert(column = "place_mean", value = mix_place_mean_total, loc = 4)

mix_promotion_mean = pd.DataFrame(np.mean(pp.mix_promotion)).T
mix_promotion_mean.insert(column = "promotion_mean", value = mix_promotion_mean_total, loc = 4)

# Intra-comparison
# Get mean
mix_product_mean
mix_price_mean
mix_place_mean
mix_promotion_mean


#mix_product_tscore = st.tscore(mix_product_mean.iloc[0,:4])
#mix_price_tscore = st.tscore(mix_price_mean.iloc[0,:4])
#mix_place_tscore = st.tscore(mix_place_mean.iloc[0,:4])
#mix_promotion_tscore = st.tscore(mix_promotion_mean.iloc[0,:4])

 
#%% Inter-comparison
mix_mean_overall_dict = {
        "product": [mix_product_mean_total],
        "price": [mix_price_mean_total],
        "place": [mix_place_mean_total],
        "promotion": [mix_promotion_mean_total],
        "overall": [mix_overall_mean],
        "average": np.mean([mix_product_mean_total, mix_price_mean_total, mix_place_mean_total, mix_promotion_mean_total])        
                 }
mix_mean_overall = pd.DataFrame(data=mix_mean_overall_dict)
mix_mean_overall
#%% Regression
# Preprocess for the regression

# Get submean of each product row.
pp.mix.iloc[:,:4]
product_mean = []
for i in range(pp.mix.shape[0]):
    product_mean.append(np.mean(pp.mix.iloc[:,:4].iloc[i,:]))

# Get submean of each price row.
pp.mix.iloc[:,4:8]
price_mean = []
for i in range(pp.mix.shape[0]):
    price_mean.append(np.mean(pp.mix.iloc[:,4:8].iloc[i,:]))

# Get submean of each place row.
pp.mix.iloc[:,8:12]
place_mean = []
for i in range(pp.mix.shape[0]):
    place_mean.append(np.mean(pp.mix.iloc[:,8:12].iloc[i,:]))

# Get submean of each promotion row.
pp.mix.iloc[:,12:16]
promotion_mean = []
for i in range(pp.mix.shape[0]):
    promotion_mean.append(np.mean(pp.mix.iloc[:,12:16].iloc[i,:]))

# Create a mean table.
mean_dict = {
        "product_mean": product_mean,
        "price_mean": price_mean, 
        "place_mean": place_mean, 
        "promotion_mean": promotion_mean
        }
mean = pd.DataFrame(data=mean_dict)

# Insert the submeans of each mixes.
demo_mix = pd.concat([pp.demo, mean], axis = 1)

# Remove the missing values.
#demo_mix.dropna(axis  = 0, inplace = True)

# Remove the minor values.
#demo_mix = demo_mix[demo_mix.sex == 0]
#demo_mix.drop(["sex", "bought"], axis = 1, inplace  = True)

#%% Check the correalation.
plt.matshow(demo_mix.corr())
plt.xticks(range(len(demo_mix.columns)), demo_mix.columns, rotation = 90)
plt.yticks(range(len(demo_mix.columns)), demo_mix.columns)
plt.colorbar()
plt.show()

# Correlation among mix satisfactions.
mix_mean_corr = demo_mix.iloc[:,-4:].corr()
#%% Import the module for regression.
#from statsmodels.formula.api import ols
#
## Target variable product mean.
#demo_mix_dependent = ["product_mean", "price_mean", "place_mean", "promotion_mean"]
#demo_mix_product_independent = demo_mix.copy()
#demo_mix_product_independent.drop(["id", demo_mix_dependent[0]], axis = 1, inplace = True)
#demo_mix_product_independent_str = " + ".join(demo_mix_product_independent.columns)
#
#model_product = ols(str("product_mean ~ " + demo_mix_product_independent_str), demo_mix).fit()
#model_product.summary()
# Target variable price mean.

# Target variable place mean.

# Target variable promotion mean. 
