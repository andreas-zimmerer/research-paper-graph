# Backend Architecture
The user always first selects a paper in the frontend and then filters and sorts the paper family. 
For this, the backend should compute the family of a paper and prepare the output so that afterwards the backend can 
filter quickly and the frontend can sort quickly. 

## Backend Components
The backend consists of a Flask controller, a Service, and a Repository. 
The Flask controller manages the REST API for the frontend. 
The Service takes over the actual backend logic. 
We use the Repository to access the database entities. 
![../img/img_06.png](../img/img_06.png)

### Repository
The getPapers call of the repository recursively queries the database for the family of the paper.
Query: `with recursive family (related, distance) as (
                select referencing, 1 as distance
                from references
                where referenced = Best WebDatabases Paper Ever)    
                  union all
                select ref.referencing, distance + 1 as distance
                from family fam, references ref
                where fam.related = ref.referenced)` 
                
The query will return something like this:
![../img/img_07.png](../img/img_07.png)

### Service
The service will then transform the received family into something like this:
![../img/img_08.png](../img/img_08.png)

Thereby, the service will count how often a paper is referenced in the family.
In addition, the service pre-sorts the resulting family by time, distance, and relevance, and caches these results to 
facilitate later filtering and sorting. To do this, the service stores the following maps locally:
![../img/img_09.png](../img/img_09.png)

### Flask Controller
The Flask Controller acts as the REST API. 
It forwards the UI actions to the Service and returns the computed paper families back to the frontend.


## Database schema
A paper has a DOI, a title, an Abstract and it is written on a fixed date. 
A paper references none, one, or several papers and it is never, once, or several times referenced. 
A paper has at least one author and several authors can work on a paper from different institutes. 
Each author and each institute have a name.
![../img/img_04.png](../img/img_04.png)

![../img/img_05.png](../img/img_05.png)