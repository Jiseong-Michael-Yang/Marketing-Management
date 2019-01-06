# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 03:51:45 2018

@author: Jiseong Yang
"""

#%% Set the working directory.
import os
os.chdir("C:/Users/Jiseong Yang/Documents/Jiseong Yang/Scholar/Semesters/4-2/Marketing Management/Project/Market Research")

#%% Import the preprocessing script.
import Lego_preprocessing as pp
#%% Clustering

#%% Perceptual Map Visualization
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from mpl_toolkits.mplot3d import Axes3D

# Define a function that flattens the lists of lists.
def flatten(list):
    flattened_list = []
    for i in range(len(list)):
        for j in range(len(list[i])):
            flattened_list.append(list[i][j])
    return flattened_list

#%% Hyperparameters
brand_names =["Lego", "Sonogong", 
              "Young Toys", "Oxford",
              "Froebel", "Montessori",
              "Edu Hansol", "Riot Games",
              "PUBG", "Mojang"]

colors = ["blue", "green", "red"]
markers = ["o", "^", "x"]
industries = ["Toys", "Education", "Games"]

color_range = [[0]] + [[i] * 3 for i in range(3)]
color_range_flattened = flatten(color_range)

marker_range = [[0]] + [[i, i+1, i+2] * 3 for i in range(1)]
marker_range_flattened = flatten(marker_range)
    
#%% The ignorant.
# Get the axes.
#fig1 = plt.figure()
#ax = fig1.add_subplot(111, projection='3d')
#
## Get the data.
#X1 = pp.ignorant_price
#Y1 = pp.ignorant_purpose
#Z1 = pp.ignorant_popularity
#
## Plot the data
#for i in range(10): 
#    ax.scatter(X1[i], Y1[i], Z1[i], label = brand_names[i], \
#               c = colors[color_range_flattened[i]], marker = markers[marker_range_flattened[i]], \
#               s=100)
#    
## Plot the text
#for i in range(len(brand_names)):
#    ax.text(X1[i], Y1[i], Z1[i], brand_names[i], fontsize = 12)
#
## Set the axes range
#ax.set_xlim3d(1, 10)
#ax.set_ylim3d(1, 10)
#ax.set_zlim3d(1, 10)
#
## Set the lable
#ax.set_xlabel("Low Price vs. High Price")
#ax.set_ylabel("Education vs. Entertainment")
#ax.set_zlabel("Low Popularity vs. High Popularity")
#ax.set_title("Perceptual Map (Unfamiliar with the brands)", fontsize = 30)
#plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

#plt.show()

#%% The moderate.
# Get the axes.
#fig2 = plt.figure()
#ax = fig2.add_subplot(111, projection='3d')
#
## Get the data.
#X1 = pp.moderate_price
#Y1 = pp.moderate_purpose
#Z1 = pp.moderate_popularity
#
## Plot the data
#for i in range(10): 
#    ax.scatter(X1[i], Y1[i], Z1[i], label = brand_names[i], \
#               c = colors[color_range_flattened[i]], marker = markers[marker_range_flattened[i]], \
#               s=100)
#    
## Plot the text
#for i in range(len(brand_names)):
#    ax.text(X1[i], Y1[i], Z1[i], brand_names[i], fontsize = 12)
#
## Set the axes range
#ax.set_xlim3d(1, 10)
#ax.set_ylim3d(1, 10)
#ax.set_zlim3d(1, 10)
#
## Set the lable
#ax.set_xlabel("Low Price vs. High Price")
#ax.set_ylabel("Education vs. Entertainment")
#ax.set_zlabel("Low Popularity vs. High Popularity")
#ax.set_title("Perceptual Map (Moderate Knowledge of the brands)", fontsize = 30)
#plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

#plt.show()

#%% The knowledgeable.
import pandas as pd

# Get the axes.
fig3 = plt.figure()
ax = fig3.add_subplot(111, projection='3d')

# Get the data.
X1 = pp.knowledgeable_price
Y1 = pp.knowledgeable_purpose
Z1 = pp.knowledgeable_popularity

# Check the coordinates.
#coord = pd.DataFrame(data = {"price": X1, "purpose": Y1, "popularity": Z1})
#coord.index = brand_names
#coord = coord.round(2)
#writer = pd.ExcelWriter('coords.xlsx')
#coord.to_excel(writer)
#writer.save()

# Plot the data
for i in range(10): 
    ax.scatter(X1[i], Y1[i], Z1[i], label = brand_names[i], \
               c = colors[color_range_flattened[i]], marker = markers[marker_range_flattened[i]], \
               s=100)
    
# Plot the text
for i in range(len(brand_names)):
    ax.text(X1[i], Y1[i], Z1[i], brand_names[i], fontsize = 12)

# Set the axes range
ax.set_xlim3d(1, 10)
ax.set_ylim3d(1, 10)
ax.set_zlim3d(1, 10)

# Set the lable
ax.set_xlabel("Low Price vs. High Price", fontsize = 12)
ax.set_ylabel("Education vs. Entertainment", fontsize = 12)
ax.set_zlabel("High Popularity vs. Low Popularity", fontsize = 12)
ax.set_title("Perceptual Map", fontsize = 20)
plt.legend(bbox_to_anchor=(1, 1), loc=1, borderaxespad=0.)

plt.show()

