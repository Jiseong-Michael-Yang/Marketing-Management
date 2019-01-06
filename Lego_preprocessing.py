# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 04:28:46 2018

@author: Jiseong Yang
"""

#%% Set the working directory.
import os
wd = r"C:\Users\Jiseong Yang\git_projects\Marketing-Management"
wd = wd.replace("'\'", '/')
os.chdir(wd)
os.getcwd()

# Load the data.
import pandas as pd
import numpy as np

kidults_xlsx = "lego_kidults.xlsx"
kidults_csv = "lego_kidults.csv"
kidults = pd.read_excel(kidults_xlsx)
kidults.to_csv(kidults_csv, encoding = 'utf-8')

kidults = pd.read_csv(kidults_csv, encoding = "utf-8")

# Check the data.
kidults.head()
#moms.head()

kidults.shape
kidults

# Set the mmaximum number of rows displayed.
pd.options.display.max_columns = 15

#%% Exploratory Data Analysis
# Create lists of values.
sex = ["남성", "여성"]
region = ["서울특별시", "인천광역시", "대전광역시", "대구광역시", "울산광역시",
          "부산광역시", "광주광역시", "세종특별자치시", "경기도", "강원도",
          "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", 
          "경상남도", "제주특별자치도"]
bought = ['구입한 적 있음', '구입한 적은 없으나 앞으로 구입할 의사가 있음',
          "구입한 적이 없으며 앞으로 구입할 의사도 없음"]
my_purpose = ["선물", "수집", "완구", "교구재", "전시용"]

raw_cols = kidults.columns
kidults[raw_cols[0]]
kidults[raw_cols[3]]
kidults[raw_cols[5]]
kidults[raw_cols[6]]

np.unique(kidults[raw_cols[1]])
np.unique(kidults[raw_cols[3]])
np.unique(kidults[raw_cols[5]])
np.unique(kidults[raw_cols[6]])

# Erase the weird sex category. 
kidults = kidults[(kidults[raw_cols[1]] == "남성") | (kidults[raw_cols[1]] == "여성")]
#%% Data Preprocessing

# Remove the last three columns that are unneccessary. 
kidults = pd.DataFrame(kidults)
kidults.columns[-3:]
kidults.drop(kidults.columns[-3:], axis =1, inplace = True)
kidults.columns[-3:]

# Remove the first column that are redundant.
kidults.drop(kidults.columns[0], axis = 1, inplace = True)

#%% Split the dataset into three parts and merge with the ID column.
kidults.columns[48:50]
demo = kidults.iloc[:,:8]
demo.columns

brand = kidults.iloc[:,8:48]
brand.columns

mix = kidults.iloc[:,48:]
mix.columns

demo.shape
brand.shape
mix.shape

# Check
kidults.shape[1] == demo.shape[1] + brand.shape[1] + mix.shape[1]
#%% Rename the columns

# Get the new and old lists of demographic dataset columns. 
demo_oldcols = demo.columns
demo_newcols = ["sex", "age", "region", "income", "bought", "my_purpose", "present_purpose", "present_age"]
len(demo_oldcols) == len(demo_newcols)

# Get the new and old lists of brand perception dataset columns.
brand_oldcols = brand.columns
brand_newcols = []
questions = ["price", "purpose", "popularity", "accuracy"]
for i in range(1, 11):
    for j in range(4):
        brand_newcols.append(questions[j] + str(i))
len(brand_oldcols) == len(brand_newcols)

# Get the new and old lists of marketing mix perception dataset columns.
mix_oldcols = mix.columns
mix_newcols = []
marketing_mix = ["product", "price", "place", "promotion"]
for i in range(4):
    for j in range(1,5):
        mix_newcols.append(marketing_mix[i] + str(j))
mix_newcols.append("overall")
len(mix_oldcols) == len(mix_newcols)

# Define the function that creates a dictionary of the old and new column names.
def get_col_dic(oldcols, newcols):
    col_dic = {}
    for i in range(len(oldcols)):
        col_dic[oldcols[i]] = newcols[i]
    return col_dic

# Assign the dictionaries created by the fucntion and rename the column names.        
demo_columns_dic = get_col_dic(demo_oldcols, demo_newcols)
brand_columns_dic = get_col_dic(brand_oldcols, brand_newcols)
mix_columns_dic = get_col_dic(mix_oldcols, mix_newcols)

demo.rename(columns=demo_columns_dic, inplace=True)
brand.rename(columns=brand_columns_dic, inplace=True)
mix.rename(columns=mix_columns_dic, inplace=True)

# Arrange the column order.
demo_col_rearrange = ['sex', 'region', 'bought', 'my_purpose', 
                      'present_purpose', 'present_age', 'age', 'income']
demo = demo[demo_col_rearrange]

demo
brand
mix

#%% Encode the first dataset (demographic dataset)
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_selection import SelectKBest

# Drop the gift-related columns. 
demo.columns
demo.drop(demo.columns[4:6], axis =1, inplace = True)

# Get the mapping dictionaries.
age_mapping = {
        "12세 미만": 0,
        "12세 이상 19세 미만": 1, 
        "19세 이상 29세 미만": 2, 
        "29세 이상 30세 미만": 3, 
        "30세 이상 40세 미만": 3, 
        "40세 이상 50세 미만": 4, 
        "50세 이상 60세 미만": 5, 
        "60세 이상": 6
        }

sex_mapping = {sex: i for i, sex in enumerate(sex)}
region_mapping = {region: i for i, region in enumerate(region)}
bought_mapping = {bought: i for i, bought in enumerate(bought)}
my_purpose_mapping = {my_purpose: i for i, my_purpose in enumerate(my_purpose)}

# Preprocessing for clustering &(|) regression.
    
# Fix the error of the survey question that inquire the age range and encode the ordinal features. (age)    
demo.age = demo.age.map(age_mapping)
set(demo.age)

# Encode the nominal features. (sex, region, bought, my_purpose)
nominal_features = ["sex", "region", "bought", "my_purpose"]
demo[nominal_features[0]] = demo[nominal_features[0]].map(sex_mapping)
demo[nominal_features[1]] = demo[nominal_features[1]].map(region_mapping)
demo[nominal_features[2]] = demo[nominal_features[2]].map(bought_mapping)
demo[nominal_features[3]] = demo[nominal_features[3]].map(my_purpose_mapping)
    
# Features by types
demo_categorical = ["sex", "region", "bought", "my_purpose"]
demo_numerical = ["age", "income"]

#demo_dummies = pd.DataFrame(pd.get_dummies(demo[nominal_features], drop_first=True))
   
# Add the knowledge level on brands as features to the demographic dataset. 
knowledge = brand[brand.filter(regex="^accuracy").columns]
demo_numerical = pd.concat([demo[demo_numerical], knowledge], axis = 1)

#%% Scale the numerical features. 
from sklearn.preprocessing import StandardScaler

# Normailze
stds = StandardScaler()
stds.fit(demo_numerical)
demo_stds = pd.DataFrame(stds.transform(demo_numerical))

# Rename the columns
demo_stds.shape[1]
demo_numerical.shape[1]
demo_stds.rename(columns=get_col_dic(demo_stds.columns, demo_numerical.columns), inplace = True)

# Concatenate the scaled table with categorical tables.
demo = pd.concat([demo[demo_categorical], demo_stds], axis =1)
demo
    
#%% Segment the perceptual data
# Getting a list of each company's data.
brands_data = []
for i in range(1,11):
    brands_data.append(brand.iloc[:,(i-1)*4:i*4])

# Define the function that adds the ID columns.
def concat_id(dataset_whole, dataset_brand):
    import pandas as pd
    dataset_brand = pd.concat([dataset_whole[dataset_whole.columns[0]], dataset_brand], axis = 1)
    dataset_brand.rename(columns = {dataset_brand.columns[0]: "ID"}, inplace = True)
    return dataset_brand

# Get the dataset for each brand.
lego, sonogong, young_toys, oxford, froebel, montessori, edu_hansol, riot_games, pubg, mojang = brands_data

# Get the dataset of each brand.
brand_perception_by_knowledge = []

# Store them all in a single list.
for name in brands_data:
    # Combine the dataset with ID columns. 
    name = concat_id(kidults, name) 
    
    # Filter out the dataset depending on the accuarcy.
    brand_ignorant = name[name[name.columns[4]] < 3]
    brand_moderate = name[name[name.columns[4]] == 3]
    brand_knowledgeable = name[name[name.columns[4]] > 3]
    
    # Append three different gruops by the level of knowledge to a single list. 
    brand_perception_by_knowledge.append([brand_ignorant, brand_moderate, brand_knowledgeable])

# Wait for a second to prevent the errors.
import time
time.sleep(1)        
  
#%% Acquiring datasets by brands.

# Lego
# Ignorant group
lego_ignorant = brand_perception_by_knowledge[0][0]
lego_ignorant_average = lego_ignorant.describe().iloc[1,:3]

# Moderate Group
lego_moderate = brand_perception_by_knowledge[0][1]
lego_moderate_average = lego_moderate.describe().iloc[1,:3]

# Knowledgeable Group
lego_knowledgeable = brand_perception_by_knowledge[0][2]
lego_knowledgeable_average = lego_knowledgeable.describe().iloc[1,:3]

# Sonogong
# Ignorant group
sonogong_ignorant = brand_perception_by_knowledge[1][0]
sonogong_ignorant_average = sonogong_ignorant.describe().iloc[1,:3]

# Moderate Group
sonogong_moderate = brand_perception_by_knowledge[1][1]
sonogong_moderate_average = sonogong_moderate.describe().iloc[1,:3]

# Knowledgeable Group
sonogong_knowledgeable = brand_perception_by_knowledge[1][2]
sonogong_knowledgeable_average = sonogong_knowledgeable.describe().iloc[1,:3]

# Young Toys
    # Ignorant group
young_toys_ignorant = brand_perception_by_knowledge[2][0]
young_toys_ignorant_average = young_toys_ignorant.describe().iloc[1,:3]

# Moderate Group
young_toys_moderate = brand_perception_by_knowledge[2][1]
young_toys_moderate_average = young_toys_moderate.describe().iloc[1,:3]

# Knowledgeable Group
young_toys_knowledgeable = brand_perception_by_knowledge[2][2]
young_toys_knowledgeable_average = young_toys_knowledgeable.describe().iloc[1,:3]

# Oxford
# Ignorant group
oxford_ignorant = brand_perception_by_knowledge[3][0]
oxford_ignorant_average = oxford_ignorant.describe().iloc[1,:3]

# Moderate Group
oxford_moderate = brand_perception_by_knowledge[3][1]
oxford_moderate_average = oxford_moderate.describe().iloc[1,:3]

# Knowledgeable Group
oxford_knowledgeable = brand_perception_by_knowledge[3][2]
oxford_knowledgeable_average = oxford_knowledgeable.describe().iloc[1,:3]

# Froebel
# Ignorant group
froebel_ignorant = brand_perception_by_knowledge[4][0]
oxford_ignorant_average = oxford_ignorant.describe().iloc[1,:3]

# Moderate Group
froebel_moderate = brand_perception_by_knowledge[4][1]
froebel_moderate_average = froebel_moderate.describe().iloc[1,:3]

# Knowledgeable Group
froebel_knowledgeable = brand_perception_by_knowledge[4][2]
froebel_knowledgeable_average = froebel_knowledgeable.describe().iloc[1,:3]

# Montessori
# Ignorant group
montessori_ignorant = brand_perception_by_knowledge[5][0]
montessori_ignorant_average = montessori_ignorant.describe().iloc[1,:3]

# Moderate Group
montessori_moderate = brand_perception_by_knowledge[5][1]
montessori_moderate_average = montessori_moderate.describe().iloc[1,:3]

# Knowledgeable Group
montessori_knowledgeable = brand_perception_by_knowledge[5][2]
montessori_knowledgeable_average = montessori_knowledgeable.describe().iloc[1,:3]

# Edu Hansol
# Ignorant group
edu_hansol_ignorant = brand_perception_by_knowledge[6][0]
edu_hansol_ignorant_average = edu_hansol_ignorant.describe().iloc[1,:3]

# Moderate Group
edu_hansol_moderate = brand_perception_by_knowledge[6][1]
edu_hansol_moderate_average = edu_hansol_moderate.describe().iloc[1,:3]

# Knowledgeable Group
edu_hansol_knowledgeable = brand_perception_by_knowledge[6][2]
edu_hansol_knowledgeable_average = edu_hansol_knowledgeable.describe().iloc[1,:3]

# Riot Games
# Ignorant group
riot_games_ignorant = brand_perception_by_knowledge[7][0]
riot_games_ignorant_average = riot_games_ignorant.describe().iloc[1,:3]

# Moderate Group
riot_games_moderate = brand_perception_by_knowledge[7][1]
riot_games_moderate_average = riot_games_moderate.describe().iloc[1,:3]

# Knowledgeable Group
riot_games_knowledgeable = brand_perception_by_knowledge[7][2]
riot_games_knowledgeable_average = riot_games_knowledgeable.describe().iloc[1,:3]

# PUBG
# Ignorant group
pubg_ignorant = brand_perception_by_knowledge[8][0]
pubg_ignorant_average = pubg_ignorant.describe().iloc[1,:3]

# Moderate Group
pubg_moderate = brand_perception_by_knowledge[8][1]
pubg_moderate_average = pubg_moderate.describe().iloc[1,:3]

# Knowledgeable Group
pubg_knowledgeable = brand_perception_by_knowledge[8][2]
pubg_knowledgeable_average = pubg_knowledgeable.describe().iloc[1,:3]

# Mojang
# Ignorant group
mojang_ignorant = brand_perception_by_knowledge[9][0]
mojang_ignorant_average = mojang_ignorant.describe().iloc[1,:3]

# Moderate Group
mojang_moderate = brand_perception_by_knowledge[9][1]
mojang_moderate_average = mojang_moderate.describe().iloc[1,:3]

# Knowledgeable Group
mojang_knowledgeable = brand_perception_by_knowledge[9][2]
mojang_knowledgeable_average = mojang_knowledgeable.describe().iloc[1,:3]   

#%% Concatenating all the datasets by the level of knowledge.
# Set the hyper parameter
price_index = [i*3 for i in range(10)]    
purpose_index = [i*3+1 for i in range(10)]
popularity_index = [i*3+2 for i in range(10)]
    
# Get the ignorant perceptual data.
ignorant_average = [lego_ignorant_average, sonogong_ignorant_average, 
            young_toys_ignorant_average, oxford_ignorant_average, \
            froebel_knowledgeable_average, montessori_knowledgeable_average, 
            edu_hansol_ignorant_average, riot_games_ignorant_average,
            pubg_ignorant_average, mojang_ignorant_average]

ignorant = pd.concat(ignorant_average, axis = 0)
ignorant

ignorant_price = ignorant[price_index]
ignorant_purpose = ignorant[purpose_index]
ignorant_popularity = ignorant[popularity_index]

# Convert the values into lists
ignorant_price = list(ignorant_price)
ignorant_purpose = list(ignorant_purpose)
ignorant_popularity = list(ignorant_popularity)

# The moderate.
moderate_average = [lego_moderate_average, sonogong_moderate_average, 
            young_toys_moderate_average, oxford_moderate_average, \
            froebel_knowledgeable_average, montessori_knowledgeable_average, 
            edu_hansol_moderate_average, riot_games_moderate_average,
            pubg_moderate_average, mojang_moderate_average]

moderate = pd.concat(moderate_average, axis = 0)
moderate

moderate_price = moderate[price_index]
moderate_purpose = moderate[purpose_index]
moderate_popularity = moderate[popularity_index]

# Convert the values into lists
moderate_price = list(moderate_price)
moderate_purpose = list(moderate_purpose)
moderate_popularity = list(moderate_popularity)
    
# The Knowledgeable.
knowledgeable_average = [lego_knowledgeable_average, sonogong_knowledgeable_average, 
            young_toys_knowledgeable_average, oxford_knowledgeable_average, 
            froebel_knowledgeable_average, montessori_knowledgeable_average, 
            edu_hansol_knowledgeable_average, riot_games_knowledgeable_average,
            pubg_knowledgeable_average, mojang_knowledgeable_average]

knowledgeable = pd.concat(knowledgeable_average, axis = 0)
knowledgeable

knowledgeable_price = knowledgeable[price_index]
knowledgeable_purpose = knowledgeable[purpose_index]
knowledgeable_popularity = knowledgeable[popularity_index]

# Convert the values into lists
knowledgeable_price = list(knowledgeable_price)
knowledgeable_purpose = list(knowledgeable_purpose)
knowledgeable_popularity = list(knowledgeable_popularity)

#%% Encoding the last datset (marketing mix dataset)

# Preprocesing for Regression Analysis.
mix
mix.describe()

mix_product = mix.iloc[:,:4]
mix_price = mix.iloc[:,4:8]
mix_place = mix.iloc[:,8:12]
mix_promotion = mix.iloc[:,12:16]

mix_product.corr().iloc[0,:]
np.mean(mix_product.corr().iloc[0,:])

# Create ID column as the first column.
demo["id"] = [i+1 for i in range(demo.shape[0])]
demo = demo[["id",'sex', 'region', 'bought', 'my_purpose', 'age', 'income', 'accuracy1',
       'accuracy2', 'accuracy3', 'accuracy4', 'accuracy5', 'accuracy6',
       'accuracy7', 'accuracy8', 'accuracy9', 'accuracy10']]

# Concatenate demographic and marketing mix columns (especially, for the regression analysis)
#demo_mix = pd.concat([demo, mix], axis = 1)


