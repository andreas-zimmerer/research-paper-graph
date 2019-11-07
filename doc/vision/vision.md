# Vision
The Research Paper Analyser examines to what extent research work is related to each other, 
i.e. whether and how often it refers to each other. 
For example, if paper C is based on paper B and paper B is based on paper A, then papers A, B and C are connected. 
![../img/img_01.png](../img/img_01.png)

## Motivation
When we read a paper for our research and are interested in further work on our topic, 
we are sometimes not sure which reference of the paper or which reference of reference of the paper is appropriate. 
What we need here is a tool that gives us all the relevant papers for a particular paper. 
We want to filter and sort these papers according to their relevance for our research.

Sometimes we don't come across a special paper, but a whole field of research that interests us. 
On the one hand, we will ask ourselves which papers are relevant for the respective research area. 
On the other hand, we want to know into which topics our field can be subdivided.  
We therefore need an instrument that assigns families of research work to their research topic and their field of research.

When our government discusses a problem, it often involves external professors and asks them for advice. 
Our governments could choose these experts more safely if they were able to visualize all the experts on a particular topic. 
When a university calls a professor to a chair, their selection can be supported by a tool that visualizes all their candidates. 

## Goal
The Research Paper Analyser will examine related research papers in such a way that it firstly presents groups of 
papers that build on each other, secondly research areas with their respective papers, and thirdly groups of 
communicating researchers:

1. Given is a Paper B. 
In order to find similar papers to B, we pass the Research Paper Analyser our paper B, i.e. 
we give its name, its DOI, or its author.
The Research Paper Analyser now presents all papers on which our paper B is based, and it presents all papers 
that are based on our paper B in the form of a graph. 
Because these are potentially very many papers, we can filter and sort papers according to our interest. 
When filtering, we can let the Research Paper Analyser only output papers from a certain period of time. 
Or we can only have it present papers with a certain keyword.
The Research Paper Analyser can sort papers by time, distance, and relevance. 
For example, we might be particularly interested in those relatives of our paper B that were created around 2018. 
After sorting, the Research Paper Graph first shows us only relatives of paper B from 2018. 
If we zoom out the graph by scrolling over it, it also shows us papers from 2017 and 2019. 
The more we shrink the graph by scrolling, the more papers we see and the more scattered they are around 2018.

2. A research area is given, for example "Web Databases" or "Join Optimisation". 
In a Research Paper Graph we will be able to see all the papers from this research area. 
For this purpose, our Research Paper Analyser records all papers whose keywords contain the name of the research area. 
The Research Paper Analyser then classifies the papers thus recorded into their respective families. 
Families that consist of many papers with the research area in their keywords are considered to be relevant.

![../img/img_02.png](../img/img_02.png)

3. Given is researcher Bob. 
We ask ourselves which researchers Bob often communicates with due to a similar background. 
We give the Research Paper Analyser the name of the researcher -- Bob. 
The Research Paper Analyser identifies which paper families Bob is involved in and presents the names of the other 
researchers from those families. 
So, analogous to the Research Paper Graph, here we create a Researcher Graph. 
