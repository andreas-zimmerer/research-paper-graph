# Vision
The Research Paper Analyser examines to what extent research work is related to each other, 
i.e. whether and how often it refers to each other. 
For example, if paper C is based on paper B and paper B is based on paper A, then papers A, B and C are connected. 
![../img/img_01.png](../img/img_01.png)

## Motivation

When we read a paper for our research and are interested in further work on our topic, 
going through all cited papers to find out which one is important can be a tedious exercise. In our project, we want to facilitate the process by providing a citation graph which will easily give the opportunity to see which papers are similar and hence close to our paper and which are generally most important to the topic by identifying the most central papers in the topic cluster in the graph.

Sometimes we don't come across a special paper, but a whole field of research that interests us. 
On the one hand, we will ask ourselves which papers are relevant for the respective research area. 
On the other hand, we want to know into which topics our field can be subdivided.  
We therefore need an instrument that assigns families of research work to their research topic and their field of research.

When our government discusses a problem, it often involves external professors and asks them for advice. 
We want to make sure that our government has the best information in order to decide which experts to invite concerning a special topic by seeing how central the professor's papers are within the field of interest. The same holds for universities calling a professor to a chair. Our graph provides multiple additional information which can support their decision making. It also helps to easily identify members of the appointment commission, which have been publishing with a candidate and which are therefore biased. 

## Goal
The Research Paper Analyser will examine related research papers in such a way that it firstly presents groups of 
papers that build on each other, secondly research areas with their respective papers, and thirdly groups of 
communicating researchers:

### Paper Families
Given is a Paper B and we are interested in its related papers. 
For this, we pass the Research Paper Analyser our paper B, i.e. we give its name, its DOI, or its author.
The Research Paper Analyser now presents all papers on which our paper B is based, and it presents all papers 
that are based on our paper B in the form of a graph.
Because these are potentially very many papers, we can filter and scale graphs according by time, distance, or relevance: 

#### Parameters for Filtering and Sorting
- The time of a paper is its year of origin. 
Example: Paper A was written in 2018. Its time is 2018.
- The distance of two papers indicates how closely they are related. 
Example: If paper A quotes paper B, i.e. they are directly connected, then their distance is 1. 
If a paper E quotes paper D that quotes paper C that quotes Paper B, then Paper E and Paper B are only indirectly connected.
They have a distance of 3. 
- The relevance of a paper counts its direct quotes. 
For example, if paper A quotes both paper B and paper C, and if paper B quotes paper C, 
then this group of three quotes 0 times paper A, 1 times paper B, and 2 times paper C. 
For this group, paper C is the most relevant.

#### Examples for Filtering and Sorting
- If we filter for papers written between 2015 and 2019, our graphs only present papers from 2015 - 2019.
- If we sort these papers by newness, then the graph initially only presents papers from this year.
 If we zoom out of the graph by scrolling, it displays more and more papers from earlier years until we reach 2015.   

### Research Fields
We give a research area, for example we enter the name "Web Databases" or "Join Optimisation".
Our Research Paper Graph will display all papers from this area and we can filter and sort these papers by 
their time, distance, and relevance.

Our Research Paper Analyser considers which paper families contain the most papers that have our research area as a buzzword. 
These families represent our research area. 

![../img/img_02.png](../img/img_02.png)

### Researcher Families
Given is researcher Bob and we ask ourselves with which researchers he has frequent exchange. 
For this, we pass our Research Paper Analyser the researcher's name -- Bob -- and it presents Bob in a graph of
researchers that he communicates with.

For this, our Research Paper Analyser observes which paper families Bob is involved in and 
considers other researchers from these families. 

## Architecture
Our Research Paper Analyzer is composed of a scraper, a database, an analyzing backend and a graph-heavy frontend:
- The scraper stores the meta information and references of research papers in a database. 
It reads this data from a research API such as SemanticScholar, Clarivate, ArXiv and Google Scholar and it 
adapts the format of the data to the schema of the underlying database. 
- The research graphs in the frontend represent firstly families of related research papers, 
secondly research areas with their respective work, 
and thirdly families of communicating researchers. 
The user can filter and sort the graphs according to his research interests. 
- The Research Paper Analyser acts as a backend. 
It translates the user's actions into equivalent database queries and 
passes the resulting data to the frontend in an efficiently usable format. 

![../img/img_03.png](../img/img_03.png)

## Technologies
- As our database we use Postgres.
- We implement our scraper in Python and let it access the SemanticScholar Paper API.
- We develop our backend in Python.
- We write our frontend in Typescript and React, integrating frameworks for graph visualization.

### SemanticScholar Paper API
SemanticScholar stores metainformation about papers, their authors, and their references. 
We can download this information and access it through an API.
Link: https://api.semanticscholar.org 

## Scope
- In our project we will primarily read the papers from the SemanticScholar API. 
Reading other papers and information from secondary APIs is optional. 
- We will primarily present families of papers as graphs, while we will only optionally present research areas and 
families of communicating researchers.
- We initially limit our filtering and sorting parameters to time, distance, and relevance.
