
# coding: utf-8

# #  Altair Examples
# 
# These examples use the Seattle bike trip dataset, as discussed by Jake Vanderpla

# ## Import require packages

# In[15]:


import altair as alt
import pandas as pd

# used to retreive datasets
from urllib.request import urlretrieve

# used for file existance testing
import pathlib


# ### Define data source, and local file name

# In[16]:


url = 'https://data.seattle.gov/api/views/65db-xm6k/rows.csv?accessType=DOWNLOAD'
csv_file = '../data/fremont.csv'


# ### Access data, save locally (if needed)

# In[17]:


data_file = pathlib.Path(csv_file)
if( data_file.exists() ):
    urlretrieve(url, csv_file)
#end if


# In[18]:


# read the data set
bike_df = pd.read_csv(csv_file)


# ### Show original column names, then reset to shorter names

# In[19]:


bike_df.columns


# In[20]:


bike_df.columns = ['DateString', 'West', 'East']


# ### Fix string date, convert to datetime timestamps
# 
# We do this as calculations (eg day of week) are much easier with DateTime objects

# In[21]:


bike_df['Date2'] = pd.to_datetime(bike_df['DateString'], format='%m/%d/%Y %I:%M:%S %p')


# ### Create convenience columns, show the hour and year of each observation, as well as the day number since the start of dataset (a form of pseudo-Julian Day number)

# In[22]:


bike_df['Year'] = bike_df['Date2'].dt.year
bike_df['Hour'] = bike_df['Date2'].dt.hour
bike_df['WeekDay'] = bike_df['Date2'].dt.dayofweek

bike_df['JulianDay'] =  ((bike_df['Date2'] - pd.datetime(2012, 10, 3)).dt.total_seconds()//(24*60*60)).astype(int)


# ### Save dataframe rows as json file
# 
# In order for Altair to understand the JSON file as written by Pandas, we must perform some data conversions.
# 
# For example, pandas converts all datetimes to UTC before writing to JSON, which Altair reads as local times.

# In[23]:


bike2_df = alt.utils.sanitize_dataframe(bike_df)


# In[24]:


json_file = 'data.json'
bike2_df.to_json(json_file, orient='records')


# ## Altair Charting

# In[25]:


c1 = alt.Chart(bike2_df[0:1000]).mark_line(opacity=0.05).encode(
    x=alt.X('Hour:Q'),
    y='East:Q',
    color=alt.Color('JulianDay:N', legend=None, scale=alt.Scale(range=['red'])))
c1


# In[26]:


c2 = alt.Chart(bike2_df[0:1000]).mark_line(opacity=0.1).encode(
    x=alt.X('Hour:Q'),
    y='East:Q',
    color=alt.Color('JulianDay:Q',  legend=None, scale=alt.Scale(range=['red'])))
c2


# In[27]:


c3 = alt.Chart(bike2_df[0:1000]).mark_line(opacity=0.1).encode(
    x=alt.X('Hour:Q'),
    y='East:Q',
    color=alt.Color('JulianDay:O',  legend=None, scale=alt.Scale(range=['red'])))
c3


# In[28]:


c3.save('singleColorRangeOrdinal.png')
c2.save('singleColorRangeQuant.png')
c1.save('singleColorRangeNominal.png')

