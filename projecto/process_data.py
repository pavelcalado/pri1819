#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 13:15:24 2018

@author: pavel
"""

import pandas as pd

#%%

#FILE = 'en_docs.csv'
#OUT_FILE = 'en_docs_clean.csv'
FILE = 'pt_docs.csv'
OUT_FILE = 'pt_docs_clean.csv'
DATASET = 'MPDataset_MPDS2018a.csv'

#%%

docs = pd.read_csv(FILE, header=0, encoding='utf-8')
docs = docs[['text', 'manifesto_id', 'party', 'date', 'title']]

# parties must be idetified by (year,code) because they change name overtime
party_ids = [(int(r[1].date/100), r[1].party) for r in docs.iterrows()]
docs['party'] = party_ids

dat = pd.read_csv(DATASET, header=0, encoding='utf-8')
dat = dat[['date', 'party', 'partyname']]
ids_map = dict([((int(r[1].date/100), r[1].party), r[1].partyname) for r in dat.iterrows()])

# Add party names
docs['party'] = docs['party'].map(ids_map)

#%%

# Filter some data
party_counts = docs['party'].value_counts()
party_counts = party_counts[party_counts > 100]
docs = docs[docs['party'].isin(party_counts.index)]

docs = docs[docs['text'].notnull()]

#%%

print(docs['party'].value_counts(), "\n")
print(docs['manifesto_id'].value_counts())

#%%

docs.to_csv(OUT_FILE, index=False)
