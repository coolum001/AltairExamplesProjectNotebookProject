
# coding: utf-8

# In[1]:


import altair as alt
import pandas as pd

from urllib.request import urlretrieve


# ### Define data source, and local file name

# In[2]:


url = 'https://data.seattle.gov/api/views/65db-xm6k/rows.csv?accessType=DOWNLOAD'
csv_file = '../data/fremont.csv'


# ### Access data, save locally

# In[3]:


urlretrieve(url, csv_file)


# In[4]:


bike_df = pd.read_csv(csv_file)


# In[5]:


bike_df.columns


# In[6]:


bike_df.columns = ['DateString', 'West', 'East']


# ### Fix string date, convert to datetime timestamps

# In[10]:


bike_df['Date2'] = pd.to_datetime(bike_df['DateString'], format='%m/%d/%Y %I:%M:%S %p')


# In[12]:


bike_df[0:24]


# In[13]:


bike_df['Year']=bike_df['Date2'].dt.year


# ### Save dataframe r ows as json file

# In[16]:


json_file = 'data.json'
bike_df[0:24].to_json(json_file, orient='records')


# ## Altair Charting

# In[18]:


alt.Chart(json_file).mark_line().encode(
    x='Date2:T',
    y='East:Q')


# In[24]:


alt.Chart(bike_df[0:24]).mark_bar().encode(
    alt.X('Date2:T', timeUnit='hours'),
    y='mean(East):Q')


# In[28]:


alt.Chart(json_file).mark_bar().encode(
    alt.X('Date2:T', timeUnit='hours'),
    y='mean(East):Q')

