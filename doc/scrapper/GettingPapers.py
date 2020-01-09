#!/usr/bin/env python
# coding: utf-8

# Trying to fetch date from SemanticScholar, Clarivate, and ArXiv databases (und web of science)

# ## SemanticScholar
# license : https://api.semanticscholar.org/corpus/legal/
# Resume: License Grant. Effective as of the Effective Date, AI2 grants to Licensee a worldwide, perpetual (except as provided in Section 8(d) below), non-exclusive, non-transferable, non-sublicensable license to use and make derivatives of the Data only for Licensee’s non-commercial, internal operation and use and subject to the further provisions below
# 
# About the size , it has 178 zip files off 0.5 GB zipped each ->1.5Gb unzipped.....

# In[26]:


#SemanticScholar
#licence https://api.semanticscholar.org/corpus/legal/
#about the dat
import requests
URL = "https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2019-11-01/manifest.txt"
manifesto = requests.get(url = URL).text
URLzips = "https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2019-11-01/"
Zip_entryes = manifesto.split("\n")
Zip_UrLs = [URLzips+x for x in Zip_entryes]


# In[35]:


Zip_entryes = manifesto.split("\n")
Zip_UrLs = [URLzips+x for x in Zip_entryes]


# In[40]:


#Run this off you have a good internet connection and 2.5Gb free space in the disc
#note to reallly destroy your computer you can remove break and then you need arround 200GB and a infinite
#amount of time
from urllib.request import urlretrieve
ProjectPath = "/home/ricostynha/Desktop/Erasmus/Apps/FoolingAround"
for (file_name,file_url) in zip(Zip_entryes,Zip_UrLs):
    print("You are requesting a get to:" +file_url)
    dst = ProjectPath+"/"+file_name
    urlretrieve(file_url, dst)
    print("Finished retreiving")
    break

