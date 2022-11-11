#!/usr/bin/env python
# coding: utf-8

# # CNNS Audit Events 2 Firewall Rules Generator v1.0

# #### Author: Piotr Jablonski, pijablonski@paloaltonetworks.com
# #### 11 Nov 2022

# ## Initial import

# In[10]:


import json
import pandas as pd

# For Python 2+3 with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

import argparse

parser = argparse.ArgumentParser(description="CNNF/CNNS firewall rules generator v1.0",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-e", "--rule_effect",  help="rule effect",  default="alert", required=False)
parser.add_argument("-i", "--input",  help="image input",  default="in.csv", required=False)
parser.add_argument("-o", "--output",  help="image output", default="out.json", required=False)
args = vars(parser.parse_args())

# ## File variables

# In[19]:


file_in = args["input"]
file_result = args["output"]

# Available options:
# "allow"
# "alert"
# "prevent"
rule_effect = args["rule_effect"]


# ## Importing firewall audit events

# In[15]:


data_in = pd.read_csv(file_in)
df = pd.DataFrame(data_in)


# In[17]:


#df = df.head(10)
df


# In[18]:


df2 = df[df['Block'] == False]
#df2


# ## Extracting unique image names

# In[6]:


df3 = pd.DataFrame()
df4 = pd.DataFrame()
image_df = pd.DataFrame()

df3['ImageName'] = df2['SrcImageName']
df4['ImageName'] = df2['DstImageName']
image_df = pd.concat([df3,df4]).drop_duplicates()
image_df = image_df.reset_index(drop=True)
#image_df


# ## Start-up json template

# In[7]:


data = {
    "_id": "networkFirewall",
    "hostEnabled": True,
    "hostRules": [],
    "containerEnabled": True,
    "containerRules": [],
    "networkEntities": []
}


# ## Generating firewall rules

# In[8]:


#print(image_df)
for row in df2.itertuples():
    #print("No.", row.Index, " :" ,df2.loc[row.Index,'DstImageName'])
    
    #print(df2.loc[row.Index,"SrcImageName"])
    #df.index[df['column_name']==value].tolist()
    if df2.loc[row.Index,'SrcImageName'] in image_df['ImageName'].values :
        src = image_df.index[image_df['ImageName'] == df2.loc[row.Index,'SrcImageName']].tolist()
        #print(src)

    if df2.loc[row.Index,'DstImageName'] in image_df['ImageName'].values :
        dst = image_df.index[image_df['ImageName'] == df2.loc[row.Index,'DstImageName']].tolist()
        #print(dst)

    rulex = {
            "id": row.Index,
            "src": src[0]+100,
            "dst": dst[0]+100,
            "ports": [
                {
                    "start": row.Port,
                    "end": row.Port,
                    "deny": False
                }
            ],
            "effect": rule_effect
        }
    #print(rulex)
    
    data['containerRules'].append(rulex)

#print(data)


# ## Generating collections

# In[9]:


for i, row in image_df.itertuples():
    #print(i, " :" ,row)
    name = row.replace('/', '_') 
    name = name.replace('.', '-')
    #print(name)
    data_rule = {
            "_id": i+100,
            "name": name,
            "type": "container",
            "collections": [
                {
                    "hosts": [
                        "*"
                    ],
                    "images": [
                        row
                    ],
                    "labels": [
                        "*"
                    ],
                    "containers": [
                        "*"
                    ],
                    "functions": [
                        "*"
                    ],
                    "namespaces": [
                        "*"
                    ],
                    "appIDs": [
                        "*"
                    ],
                    "accountIDs": [
                        "*"
                    ],
                    "codeRepos": [
                        "*"
                    ],
                    "clusters": [
                        "*"
                    ],
                    "name": name,
                    "system": False,
                    "prisma": False
                }
            ]
            }

    data['networkEntities'].append(data_rule)
    
    #data['networkEntities'][0]['collections'][0]['images'] = row


# ## Saving the output to a JSON file

# In[ ]:


with io.open(file_result, 'w', encoding='utf8') as outfile:
    str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))

