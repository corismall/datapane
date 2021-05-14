#!/usr/bin/env python
# coding: utf-8

# In[64]:


import pandas as pd
import altair as alt
from functools import partial
import datapane as dp

# Authenticate with your API token
dp.login(token="TOKEN")


# In[68]:


#read in draft1
testdraft1 = pd.read_csv('/Users/Corinn/Documents/UCSF/Projects/BPDCN/test_draft1.csv')
dfpatients = pd.read_csv('/Users/Corinn/Documents/UCSF/Projects/BPDCN/patient_agesexloc.csv')

df = pd.DataFrame(testdraft1)
df


# In[6]:


#frequency of country
plot = alt.Chart(df).mark_bar().encode(
  x='country:N',
  y='count()'
)

paper_info = df[['paper_number','date_published','patient','country','region']]


report = dp.Report(
    dp.Text('Country frq'),
    dp.Plot(plot),
    dp.DataTable(paper_info)
    )


report.publish(name = 'country_frq', open = True)
#paper_info


# In[10]:


#sex frq ratio by country
plot = alt.Chart(df).mark_bar().encode(
   x = 'count()',
    y = 'country:N',
    color = 'sex:N'
)

data = df[['country', 'age', 'sex']]

report = dp.Report(
    dp.Text('Sex freq ratio by country'),
    dp.Plot(plot),
    dp.DataTable(data)
    )


report.publish(name = 'country_frq', open = True)


# In[70]:


#smoker frequency by country

plot = alt.Chart(df).mark_bar().encode(
    x='country:N',
    y='count()',
    color = 'smoker:N'
)

report = dp.Report(
    dp.Text('Patient smoking freq by country'),
    dp.Plot(plot),
    dp.DataTable(df)
    )


report.publish(name = 'smoking_frq', open = True)


# In[73]:


#frequency of year published

#converts date to datetime obj
to_datetime_fmt = partial(pd.to_datetime, format='%Y')
df['date_published'] = df['date_published'].apply(to_datetime_fmt)

plot = alt.Chart(df).mark_area().encode(
    x='date_published:T',
    y='count()',
    color = 'region:N'
).interactive()



report = dp.Report(
    dp.Text('publishing frq by region'),
    dp.Plot(plot),
    dp.DataTable(df)
    )


report.publish(name = 'publishing_freq', open = True)


# In[11]:


#age frequency

plot = alt.Chart(df).mark_area().encode(
    x = 'age',
    y = 'count()',
    color = 'sex:N' 
)

data = df[['country', 'age', 'sex']]

report = dp.Report(
    dp.Text('Age frq'),
    dp.Plot(plot),
    dp.DataTable(data)
    )


report.publish(name = 'age_frq', open = True)


# In[13]:


#patient cbc, showing relatedness between cell counts

#create selection
interval = alt.selection_interval(encodings = ['x','y'])

chart = alt.Chart(df).mark_point().encode(
    x='wbc_abs',
    y='rbc_abs',
    color = alt.condition(interval,'pb_involvement:N', alt.value('lightgray'))
).properties(
    selection = interval
)

plots = chart | chart.encode(x='plt_abs')



report = dp.Report(
    dp.Text('cbc relatedness'),
    dp.Plot(plots),
    dp.DataTable(df)
    )


report.publish(name = 'cbc_data', open = True)


# In[71]:





# In[66]:


#patient symptoms

patient_sym = pd.read_csv('/Users/Corinn/Documents/UCSF/Projects/BPDCN/testpatient_symptoms.csv')
df=pd.DataFrame(patient_sym)




# In[26]:


#patient tissues

#frequency of cd markers
cd4 = alt.Chart(df).mark_bar().encode(
    x='cd4:N',
    y='count():Q',
    color = 'biopsy_tissue:N'
)

cd45 = alt.Chart(df).mark_bar().encode(
    x='cd45:N',
    y='count()',
    color = 'biopsy_tissue:N'
)

cd56 = alt.Chart(df).mark_bar().encode(
    x='cd56:N',
    y='count()',
    color = 'biopsy_tissue:N'
)

cd123 = alt.Chart(df).mark_bar().encode(
    x='cd123:N',
    y='count()',
    color = 'biopsy_tissue:N'
)

mpo = alt.Chart(df).mark_bar().encode(
    x='mpo:N',
    y='count()',
    color = 'biopsy_tissue:N'
)

tdt = alt.Chart(df).mark_bar().encode(
    x='tdt:N',
    y='count()',
    color = 'biopsy_tissue:N'
)

plots = cd4 | cd45 | cd56 | cd123 | mpo | tdt 


'''report = dp.Report(
    dp.Text('Tissue cell markers'),
    dp.Plot(plots),
    dp.DataTable(df)
    )


report.publish(name = 'tissue_cd_markers', open = True)
'''

plots


# In[46]:


plot = alt.Chart(df).mark_point().encode(
    x='progression_free:Q',
    y='overall_survival_months:Q',
    color = 'initial_therapy:N',
    tooltip='death:N'
)

report = dp.Report(
    dp.Text('Therapy & Survival'),
    dp.Plot(plot),
    dp.DataTable(df)
    )


report.publish(name = 'therapy_survival', open = True)


# In[66]:


plot = alt.Chart(df).mark_bar().encode(
    y='current_infection:N',
    x='count(antibiotics):O',
    color = 'antibiotics:N',
).interactive()

report = dp.Report(
    dp.Text('Infections'),
    dp.Plot(plot),
    dp.DataTable(df)
    )


report.publish(name = 'infection', open = True)

