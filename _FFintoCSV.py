import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

# Reading txt.

with open('html.txt', 'r') as f:
  file_contents = f.read()

# Search for table (need lxml parser installed)

soup = BeautifulSoup(file_contents, 'lxml')
table = soup.find('table', class_='calendar__table')

# Convert to dataframe

data = []
for row in table.find_all('tr'):
    row_data = []
    for cell in row.find_all('td'):
        row_data.append(cell.text)
    data.append(row_data)

df = pd.DataFrame(data)

# Drop none line.

for index, row in df.iterrows():
  if row[1] is None and row[2] is None:
      df.drop(index, inplace=True)

# Drop empty column.

df.drop(df.columns[2],axis=1, inplace=True)
df.drop(df.columns[3],axis=1, inplace=True)
df.drop(df.columns[4],axis=1, inplace=True)

# Switches column.

temp = df[df.columns[1]].copy()
df[df.columns[1]] = df[df.columns[3]]
df[df.columns[3]] = temp

# Add empty line between each week.

ind=[]
row_above=0

for index, row in df.iterrows():
  if "sat" in str(row[0]).lower() or "sun" in str(row[0]).lower():
    df.at[index,0]=None

# Switches to a table for easy change.

table=pd.DataFrame(df).to_numpy()

# Create a copy table for inserting data.

new_table=[]
new_table_row=[]

for y in range(len(table)):
  for z in range(len(table[y])):
    new_table_row.append(table[y][z])
  new_table_row=[]
  new_table.append(new_table_row)

# Get all the indexes of non-empty day.

ind=[]
for i in range(len(new_table)-3):
  if new_table[i][0] is not None and new_table[i][0]!='':
      ind.append(i)

# Insert empty line between each day.

start=0
for k in range(len(ind)):
  row_insert=[None]*8
  new_table.insert(ind[k]+start,row_insert)
  start=start+1

# Lift Day value.

ind=[]
for i in range(len(new_table)-3):
  if new_table[i][0] is not None and new_table[i][0]!='':
      ind.append(i)

start=0

for k in range(len(ind)):
  new_table.insert(ind[k]+start-1,[None]*8)
  new_table[ind[k]+start][0]=new_table[ind[k]+start+1][0]
  new_table[ind[k]+start+1][0]=None;
  start=start+1

# Switch first pos with last.

for i in range(len(new_table)-3):
  if new_table[i][0] is None or new_table[i][0]=='':
    new_table[i]=new_table[i][1:]
    new_table[i].append(None)
    
# Convert back to panda dataframe.

df=pd.DataFrame(new_table)

#Write to csv.

df.to_csv('data.csv', index=False)





