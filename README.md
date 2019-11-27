# Research Paper Analyser
The Research Paper Analyser examines to what extent research work is related to each other, 
i.e. whether and how often it refers to each other. 
For example, if paper C is based on papers A and B and paper B is based on paper A, then papers A, B and C are connected. 

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
communicating researchers.

### Paper Families
Given is a paper B and we are interested in its related papers. 
For this, we pass the Research Paper Analyser our paper B, i.e. we give its name, its DOI, or its author.
The Research Paper Analyser now presents all papers on which our paper B is based, and it presents all papers 
that are based on our paper B in the form of a graph.
Because these are potentially very many papers, we can filter and scale graphs according by time, distance, or relevance: 

#### Parameters for Filtering and Sorting
- The time of a paper is its year of origin. 
Example: Paper A was written in 2018. Its time is 2018.
- The distance of two papers indicates how closely they are related. 
Example: If paper A quotes paper B, i.e. they are directly connected, then their distance is 1. 
If a paper E quotes paper D that quotes paper C that quotes paper B, then paper E and paper B are only indirectly connected.
They have a distance of 3. 
- The relevance of a paper counts its direct quotes. 
For example, if paper A quotes both paper B and paper C, and if paper B quotes paper C, 
then this group of three quotes 0 times paper A, 1 times paper B, and 2 times paper C. 
For this group, paper C is the most relevant.

#### Examples for Filtering and Sorting
- If we filter for papers written between 2015 and 2019, our graphs only present papers from 2015 - 2019.
- If we sort these papers by newness, then the graph initially only presents papers from this year. If we zoom out of the graph by scrolling, it displays more and more papers from earlier years until we reach 2015.   

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
It reads this data from a research API such as SemanticScholar, Clarivate, and ArXiv and it 
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
- As our database we use PostgreSQL.
- We implement our scraper in Python and let it access the SemanticScholar Paper API.
- We build our backend on Flask using Python.
- We write our frontend in Typescript and React, integrating frameworks for graph visualization.

### PostgreSQL
PostgreSQL is a free, open source object-relational database management system. 
It supports SQL language, extensible data types, operators, functions and aggregates as well as the ACID conditions.
Reliability, robustness, and performance characterize PostgreSQL.
Link: [https://www.postgresql.org](https://www.postgresql.org)

### Python
Python is a universal, interpreted, and higher programming language. 
Because it is both concise and readable, we can easily learn and understand Python. 
Data is particularly well analysed with Python.
Link: [https://www.python.org](https://www.python.org) 

### SemanticScholar Paper API
SemanticScholar stores metainformation about papers, their authors, and their references. 
We can download this information and access it through an API.
Link: [https://api.semanticscholar.org](https://api.semanticscholar.org) 

### Flask
Flask is a Web Application Framework in Python. 
We use Flask to develop the components of our web application because it helps us integrate existing libraries into our software.
Extensibility and good documentation characterize Flask. 
Link: [https://www.palletsprojects.com/p/flask/](https://www.palletsprojects.com/p/flask/)

### TypeScript
TypeScript is a superset of JavaScript, i.e. it extends JavaScript by features such as, 
in particular, the optional static typing at the time of compilation. 
This allows us to , for example, structurally type, infer types, and parameterize types. 
Link: [https://www.typescriptlang.org](https://www.typescriptlang.org)

### React
React is a JavaScript-based web framework, i.e. it acts as a basic framework for the output of UI components on websites. 
In React, we build components hierarchically and represent them as self-defined HTML tags. 
React is designed for simplicity, performance, and reusability. 
Link: [https://reactjs.org](https://reactjs.org)

### Graph Visualization Frameworks
Graph visualization frameworks let us represent structural information as networks. 

#### ECharts
ECharts is an open source, cross-platform framework for rapidly constructing data visualizations. 
ECharts is characterized by its high performance, ease of use, and richness of built-in interactions. 
Link: [https://echarts.apache.org/en/index.html](https://echarts.apache.org/en/index.html)

#### Chart.js
Chart.js is an open source diagram library for designers and developers. 
It is based on JavaScript and supports HTML5 Canvas and JSON. 
Its high responsiveness makes Chart.js stand out.
Link: [https://www.chartjs.org](https://www.chartjs.org)

#### D3.js
D3.js (Data Driven Documents) is a JavaScript-based library that allows you to visualize data with graphical elements in your browser. 
D3.js is based on the web standards SVG, CSS, and HTML5, which makes D3.js not only fast even with large amounts of data, but also future-proof.
Link: [https://d3js.org](https://d3js.org)

## Contribute
If you want to contribute to the research-graph repository, please first read the Contributing Guidelines in the [Contributing](CONTRIBUTING.md) file.

## Project Setup
If you are using IntelliJ/PyCharm Professional, you should simply be able to open the project.
You will find some useful run configurations as well.

### Backend
The backend is a Python application with Flask framework.

Some good starting resources are:
 - [The Flask mega tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
 - [Flask Project Website](https://palletsprojects.com/p/flask/)

If you don't want to use `virtualenv`, you can install the required dependencies with
```
pip install -r requirements.txt
```
Overall, it is advisable to use `virtualenv`.

#### Installing new Packages
When installing new packages, make sure that they appear in the `requirements.txt` file

To update the `requirements.txt` file, run
```
pip freeze > requirements.txt
```

#### Starting the Backend
To start the backend on a local machine, navigate to the `backend` directory.
Next, activate the `virtualenv` as described before.
Now you can run the backend on [http://localhost:5000](http://localhost:5000) by typing
```
flask run
```

#### Linting
This project uses `pylint` as a linter. Simply run
```
pylint app
```
in the `backend` folder.

If you are using IntelliJ , it is recommended to install the [PyLint Plugin](https://plugins.jetbrains.com/plugin/11084-pylint/).


### Frontend
The frontend is located in the `frontend` folder and is written in TypeScript with React.

Some good staring resources are:
 - [The TypeScript Handbook](https://www.typescriptlang.org/)
 - [TypeScript Example on React](https://www.typescriptlang.org/play/index.html?jsx=2&esModuleInterop=true&e=196#example/typescript-with-react)
 - [React + TypeScript Cheatsheets](https://github.com/typescript-cheatsheets/react-typescript-cheatsheet#reacttypescript-cheatsheets)
 - [React: Getting Started](https://reactjs.org/docs/getting-started.html)

#### Starting the Frontend
To build the frontend, make sure you have `npm` or `yarn` installed.
Change to the `frontend` directory and run
```
npm install
```
and then
```
npm start
```
Now the frontend should open in your browser.

#### Linting
The project uses `tslint`. Run `tslint` with
```
npm run lint
```

If you use `yarn`, issue the same commands but with `yarn` instead of `npm`.


## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

