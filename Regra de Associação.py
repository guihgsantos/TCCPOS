#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install mlxtend


# In[18]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# In[89]:


#Trazendo os dataframes necessários da análise
dataframeFato = pd.read_excel("Fato.xlsx")
dataframeProduto = pd.read_excel("dProdutos.xlsx")


# In[90]:


dataframeFato.head()


# In[119]:


#Realizando o join entre as duas tabelas
dataframeJoin = pd.merge(dataframeFato, dataframeProduto, left_on='Cod_sku', right_on='cod_sku').dropna()

dataframeJoin["Categoria_Embalagem"] = dataframeJoin["nom_tipo_prod"] + "_" + dataframeJoin["Embalagem"]


# In[120]:


dataframeJoin.head()


# In[153]:


#Grouping dataframe by order and transforming it from pandas object to list, keeping only category names 
grouped = dataframeJoin.groupby("cod_pdv") 
Agrupamento1 = grouped['Categoria_Embalagem'].apply(list).to_list() 

Agrupamento2 = grouped['nom_tipo_prod'].apply(list).to_list() 

Agrupamento3 = grouped['nom_sku'].apply(list).to_list() 


# In[154]:


#Deleting orders one item only in order to increase both confidence and lift
for lista in Agrupamento1:
    if len(lista) == 1:
        Agrupamento1.remove(lista)
for lista in Agrupamento2:
    if len(lista) == 1:
        Agrupamento2.remove(lista)
for lista in Agrupamento3:
    if len(lista) == 1:
        Agrupamento3.remove(lista)


# In[135]:


#One hot encoding

from mlxtend.preprocessing import TransactionEncoder
te = TransactionEncoder()
teArray = te.fit(Agrupamento1).transform(Agrupamento1)
teDataframe1 = pd.DataFrame(teArray, columns=te.columns_)

teDataframe1.head()


# In[136]:


from mlxtend.frequent_patterns import apriori

frequent_itemsets = apriori(teDataframe1, min_support = 0.3, use_colnames = True) 
frequent_itemsets.sort_values(by=['support'], ascending = True).head(10)

#Support is defined as frequency that both items occur together in the basket divided by total of transactions in the dataset
#Since there are too many orders with no category variability, support is low


# In[137]:


from mlxtend.frequent_patterns import association_rules

rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)
#rules
rules.sort_values(by=['lift'], ascending = False).drop(['antecedent support', 'consequent support', 'leverage', 'conviction'], axis=1)

#Lift > 1 means that there's a significative association rule


# In[138]:


#One hot encoding

from mlxtend.preprocessing import TransactionEncoder
te = TransactionEncoder()
teArray = te.fit(Agrupamento2).transform(Agrupamento2)
teDataframe2 = pd.DataFrame(teArray, columns=te.columns_)

teDataframe2.head()


# In[139]:


from mlxtend.frequent_patterns import apriori

frequent_itemsets = apriori(teDataframe2, min_support = 0.1, use_colnames = True) 
frequent_itemsets.sort_values(by=['support'], ascending = True).head(10)

#Support is defined as frequency that both items occur together in the basket divided by total of transactions in the dataset
#Since there are too many orders with no category variability, support is low


# In[141]:


from mlxtend.frequent_patterns import association_rules

rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)
#rules
rules.sort_values(by=['lift'], ascending = False).drop(['antecedent support', 'consequent support', 'leverage', 'conviction'], axis=1)

#Lift > 1 means that there's a significative association rule


# In[155]:


#One hot encoding

from mlxtend.preprocessing import TransactionEncoder
te = TransactionEncoder()
teArray = te.fit(Agrupamento3).transform(Agrupamento3)
teDataframe3 = pd.DataFrame(teArray, columns=te.columns_)

teDataframe3.head()


# In[160]:


from mlxtend.frequent_patterns import apriori

frequent_itemsets = apriori(teDataframe3, min_support = 0.25, use_colnames = True) 
frequent_itemsets.sort_values(by=['support'], ascending = True).head(10)

#Support is defined as frequency that both items occur together in the basket divided by total of transactions in the dataset
#Since there are too many orders with no category variability, support is low


# In[161]:


from mlxtend.frequent_patterns import association_rules

rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)
#rules
rules.sort_values(by=['lift'], ascending = False).drop(['antecedent support', 'consequent support', 'leverage', 'conviction'], axis=1)

#Lift > 1 means that there's a significative association rule

