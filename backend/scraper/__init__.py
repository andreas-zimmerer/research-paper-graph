"""Scrape research papers from the Semantic Scholar API and put them into the database."""
import semanticscholar as ss
import requests

def scrape():
    """Scrape research papers from the Semantic Scholar API"""
    # Determine the ids of all relevant research papers.
    papers = get_all_papers()
    for paperId in papers:
        # Get all relevant information for the paper: id, title, abstract, year
        paper = ss.paper(paperId)
        paperTitle = paper['title']
        paperAbstract = paper['abstract']
        paperYear = paper['year']
        # Put the given paper into the database.
        post_paper(paperId, paperTitle, paperAbstract, paperYear)

        # Get all relevant information for the author: id, name
        authors = paper['authors']
        for author in authors:
            authorId = author['authorId']
            authorName = author['name']
            # Put the given author and writing relation into the database.
            post_author(authorId, authorName)
            post_write(paperId, authorId)

        # Get all references
        citations = paper['citations']
        for citation in citations:
            citationId = citation['paperId']
            post_reference(paperId, citationId)


def get_all_papers():
    """Determine the ids of all relevant research papers."""
    authorIds = [143993045, 144122431]
    paperIds = []
    for authorId in authorIds:
        author = ss.author(authorId)
        papers = []
        if author != {}:
            papers = author['papers']
        for paper in papers:
            paperId = paper['paperId']
            paperIds.append(paperId)
    return paperIds

def extractIds(items, idName):
    """Extract from an object list the ID of each object and create a list of all object IDs."""
    listIds = []
    for item in items:
        itemId = item[idName]
        listIds.append(itemId)
    return listIds

def post_paper(paper_id, paper_title, paper_abstract, paper_year):
    """Put the given paper into the database."""
    data = {'id':paper_id,
            'title':paper_title,
            'abstract':paper_abstract,
            'year':paper_year,
            'authors':['kemper', 'neumann']
            }
    r = requests.post(url='http://127.0.0.1:5000/paper/', json=data)
    print(r.status_code)

def post_paper(paper_id, paper_title, paper_abstract, paper_year):
    """Post the given paper into the database."""
    data = {'id':paper_id,
            'title':paper_title,
            'abstract':paper_abstract,
            'year':paper_year
            }
    r = requests.post(url='http://127.0.0.1:5000/paper/', json=data)
    print(r.status_code)

def post_author(author_id, author_name):
    """Post the given author into the database."""
    data = {'id':author_id,
            'name':author_name,
            }
    r = requests.post(url='http://127.0.0.1:5000/author/', json=data)
    print(r.status_code)

def post_write(paper, author):
    """Post the given writing relation into the database."""
    data = {'paper':paper,
            'author':author,
            }
    r = requests.post(url='http://127.0.0.1:5000/write/', json=data)
    print(r.status_code)

def post_reference(source, sink):
    """Post the given reference into the database."""
    data = {'from_paper':source,
            'to_paper':sink,
            }
    r = requests.post(url='http://127.0.0.1:5000/reference/', json=data)
    print(r.status_code)

scrape()
