
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import json_normalize
file = 'C:\\Users\\Kevin Sharp\\Desktop\\Springboard\\1574117884_data_wrangling_json_5_\\data_wrangling_json\\data\\world_bank_projects.json'
json_df = pd.read_json(file)
#%%
#Count how many times each country is listed in the dataframe, then plot the 10 highest count totals.
json_df['countryshortname'].value_counts()[:10].plot.bar(
    title='The 10 Countries with the Most Projects')

#Add plot details to make it easier to read.
plt.ylabel('# of projects')
plt.yticks(range(0, 21, 2))
plt.xticks(rotation=60, ha='right')
plt.show()
#%%
#Extract the theme name/code column. 
theme_codes = json_df['mjtheme_namecode']

#Initialize an empty list.
list_short_df = []

#Normalize each JSON string and add the resulting dataframe to a list.
for item in theme_codes:
    normed = json_normalize(item)
    list_short_df.append(normed)

#Concatenate the list of dataframes.
theme_codes_df = pd.concat(list_short_df)

#Count how often each theme name appears and plot the 10 most frequent themes.
theme_codes_df['name'].value_counts()[:10].plot.bar(
    title='The 10 Most Frequent Project Themes')

#Add plot details.
plt.ylabel('Project Theme Count')
plt.xticks(rotation=60, ha='right')
plt.show()

#%%
#To fill in the missing values, one strategy is to first sort the dataframe by code, then by name.
#This groups all the nameless entries at the top of their code number set.
theme_codes_df = theme_codes_df.sort_values(['code', 'name'])

#Next, replace the empty strings with NaN values and use bfill() fill the NaN values with the correct name.
#The sorting done in the previous step ensures that each NaN will get its new value from a row with the same code number.
theme_codes_df['name'] = theme_codes_df['name'].replace('', np.nan).bfill()

#Recount how often each theme name appears and plot the 10 most frequent themes.
theme_codes_df['name'].value_counts()[:10].plot.bar(
    title='The 10 Most Frequent Project Themes')

#Add plot details.
plt.ylabel('Project Theme Count')
plt.xticks(rotation=60, ha='right')
plt.show()