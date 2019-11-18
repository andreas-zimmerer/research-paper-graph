#!/usr/bin/env python
# coding: utf-8

# Assuming you have already extracted the files

# In[1]:


import re
#number of entries in this zip: 996181
filename= "s2-corpus-000"
filedir= "/home/ricostynha/Desktop/Erasmus/Apps/FoolingAround"
filepath = filedir+"/"+filename


# In[2]:


#just for modularity read the first 10000 entries and save in a file just to have one
Maxentries = 1000000;
Maxsize = Maxentries;
dstname = "fist10000papers.txt"
dstpath = filedir+"/"+dstname;
file_list = []
dstfile= open(dstpath,"w+")
with open(filepath) as infile:
    for line in infile:
        Maxentries-=1
        file_list.append(line)
        dstfile.write(line);
        if(Maxentries==0):
            break
Maxsize = Maxsize -Maxentries
dstfile.close()


# In[3]:


def parsingraw_entry(raw):
    #year is ommisee for web pages , so it will have less fields
    fields = ['"entities":','"journalVolume":','"journalPages":','"pmid":','"year":','"outCitations":','"s2Url":','"s2PdfUrl"',
         '"id":','"authors":','"journalName":','"paperAbstract":','"inCitations":','"pdfUrls":',
         '"title":','"doi":','"sources":','"doiUrl":','"venue":']
    helper_list=[]
    for field in fields:
        match = re.search(field,raw)
        if(match != None):
            helper_list.append([match.group(),match.span()])

    reference_list=[]
    for i in range(0,len(helper_list)-1):
        begin = helper_list[i][1][1]
        end   = helper_list[i+1][1][0]
        reference_list.append([helper_list[i][0],raw[begin:end]])
    begin = helper_list[-1][1][1]
    reference_list.append([helper_list[-1][0],raw[begin:]])
    return reference_list
   
    


# In[5]:


#basicaly ,a lot of papers dont have the filed year
data = []
for i in range(Maxsize):
    a = parsingraw_entry(file_list[i])
    if(len(a)==19):
        c = [b[1] for b in a]
        data.append(c)
    else:
        c1 = [b[1] for b in a[0:4]]
        c2 = [None]
        c3 = [b[1] for b in a[4:]]
        data.append(c1+c2+c3)
  
        
        


# In[6]:


import pandas as pd
titles  = ['entities','journalVolume','journalPages','pmid','year','outCitations','s2Url','s2PdfUrl',
'id','authors','journalName','paperAbstract','inCitations','pdfUrls',
'title','doi','sources','doiUrl','venue']

df = pd.DataFrame(data,columns=titles)


# In[7]:


#replacing empty things by none
df = df.replace({"[],":None})
df = df.replace({'"",':None})
df = df.replace({':""':None})
df = df.replace({'""}\n':None})
df = df.replace({':"",':None})


# In[8]:


def parse_journalVolume(string):
    if(string == None):
        return None
    # removing " " in numbers
    newstring = string[1:-2]
    #can appear in multiple journal volumes
    newstring = newstring.split(' ')
    #diferent volumes diferent array members
    return newstring
def parse_journalPages_helper(string):
    #removing \n
    if(string == None):
        return None
    string = string.replace(" ","")
    string = string.replace("\\n","")
    string = string[1:-2]
    #exist weirs formations irrefular like : S6-9;discussionS26-8  
    #(now i will parse for a range of pages)
    match = re.search('[1-9]+-[1-9]+',string)
    if(match != None):
        string = string[match.span()[0]:match.span()[1]]
        return string
    #checking if just one page
    match = re.search('[1-9]+',string)
    if(match != None):
        string = string[match.span()[0]:match.span()[1]]
        return string
    return string

def parse_journalPages(string):
    string = parse_journalPages_helper(string);
    if(string!= None):
        if(string.split('-') == []):
            print(string,string.split('-'))
        string = string.split('-')
    return string
def parse_pmid(string):
    if(string != None):
            string = string[1:-2]
    return string
def parse_year(string):
    if(string != None):
            string = string[0:-1]
    return string
def parse_outCitations(string):
    if(string ==None):
        return string
    string = string[1:-2]
    string = string.split(',')
    for i in range(len(string)):
        string[i] = string[i][1:-1]
    return string
def parse_s2Url(string):
    if(string == None):
        return string
    string = string[1:-2]
    return string
def parse_s2PdfUrl(string):
    if(string == None):
        return string
    string = string[2:-2]
    return string
def parse_id(string):
    if(string == None):
        return string
    string = string[1:-2]
    return string
    


# In[9]:


def parse_authors_helper(string):
    string = string.replace('"name":','')
    string = string.replace('"ids":','')
    string = string.replace('{','')
    string = string.replace('}','')
    string = string.replace('"','')
    string = string.replace("'",'')
    
    #separate author and id
    string = string.split(',')
    return string
def parse_authors(string):
    if(string == None):
        return string
    string = string[:-1]
    string = string.replace('[','')
    string = string.replace(']','')
    string = string.split("},{")
    for i in range(len(string)):
        string[i] = parse_authors_helper(string[i])
    
def parse_journalName(string):
    if(string == None):
        return string
    return string[1:-2]
def parse_paperAbstract(string):
    if(string == None):
        return string
    #to be able to read i must replace | for another carachter
    string = string.replace('|','///')
    return string[1:-2]

def parse_incitations(string):
    return parse_outCitations(string)

def parse_pdfUrls(string):
    if(string == None):
        return string
    
    string = string[2:-3]
    string = string.replace('"','')
    string = string.replace(' ','')
    string = string.split(',')
    return string
def parse_title(string):
    if(string == None):
        return string
    return string[1:-2]
def parse_doi(string):
    if(string == None):
        return string
    return string[1:-2]
def parse_sources(string):
    if(string == None):
        return string
    string = string[1:-2]
    string = string.replace('"','')
    string = string.split(',')
    return string
def parse_doiUrl(string):
    if(string == None):
        return string
    return string[1:-2]

def parce_venue(string):
    if(string==None):
        return string
    string = string[1:-3]
    return string
    
    
    


# In[10]:


df['journalVolume'] = df['journalVolume'].apply(parse_journalVolume)
df['journalPages'] = df['journalPages'].apply(parse_journalPages)
df['pmid'] = df['pmid'].apply(parse_pmid)
df['year'] = df['year'].apply(parse_year)
df['outCitations'] = df['outCitations'].apply(parse_outCitations)
df['s2Url'] = df['s2Url'].apply(parse_s2Url)
df['s2PdfUrl'] = df['s2PdfUrl'].apply(parse_s2PdfUrl)
df['id'] = df['id'].apply(parse_id)
df['authors'] = df['authors'].apply(parse_authors)
df['journalName'] = df['journalName'].apply(parse_journalName)
df['paperAbstract'] = df['paperAbstract'].apply(parse_paperAbstract)
df['inCitations'] = df['inCitations'].apply(parse_incitations)
df['pdfUrls'] = df['pdfUrls'].apply(parse_pdfUrls)
df['title'] = df['title'].apply(parse_title)
df['doi'] = df['doi'].apply(parse_doi)
df['sources'] = df['sources'].apply(parse_sources)
df['doiUrl'] = df['doiUrl'].apply(parse_doiUrl)
df['venue'] = df['venue'].apply(parce_venue)
                                
#just to being possible to wokr with stuff change None to -1
df.fillna(-1, inplace=True)


# In[11]:


#creating some usefull information
def getNumcitations(x):
    if(x==-1):
        return 0
    return len(x)

df['NumOutCitations'] = df['outCitations'].apply(getNumcitations)
df['NumInCitations'] = df['inCitations'].apply(getNumcitations)


# In[12]:


#No null df
Cyteddf = df[(df['NumInCitations'] != 0) & (df['NumOutCitations'] != 0) ]
del df


# In[13]:


len(Cyteddf)


# In[14]:


Cyteddf.sort_values(by = 'NumInCitations',ascending=False)
Cyteddf = Cyteddf.reset_index()


# In[16]:


inCitdic = {}
outCitdic = {}
related_ind = []
for ind in Cyteddf.index:
    for Cit in Cyteddf.loc[ind]['inCitations']:
        inCitdic[Cit] = 1 
        
    for Cit in Cyteddf.loc[ind]['outCitations']:
        outCitdic[Cit] = 1 
        
for index,idis in enumerate(Cyteddf['id']):
        if (idis in inCitdic) or (idis in outCitdic):
            related_ind.append(index)


# In[19]:


related_papers = Cyteddf.loc[related_ind]


# In[22]:


related_papers = related_papers.drop('index', 1)
related_papers


# In[23]:


related_papers.to_csv("/home/ricostynha/Desktop/first1000entries",sep = "|",na_rep = "* *",index = False)

