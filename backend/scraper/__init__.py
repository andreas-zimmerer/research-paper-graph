"""Scrape research papers from the Semantic Scholar API and put them into the database."""
import semanticscholar as ss
import requests

def scrape(): # pylint:disable=too-many-locals
    """Scrape research papers from the Semantic Scholar API"""
    # Determine the ids of all relevant research papers.
    papers = get_all_papers()
    for paperId in papers:
        # Get all relevant information for the paper: id, title, abstract, year
        paper = ss.paper(paperId)
        paperTitle = paper['title']
        paperAbstract = paper['abstract']
        paperYear = paper['year']
        citations = paper['citations']
        paperCitations = len(citations)
        # Put the given paper into the database.
        post_paper(paperId, paperTitle, paperAbstract, paperYear, paperCitations)

        # Get all relevant information for the author: id, name
        authors = paper['authors']
        for author in authors:
            authorId = author['authorId']
            authorName = author['name']
            # Put the given author and writing relation into the database.
            post_author(authorId, authorName)
            post_write(paperId, authorId)

        # Get all references.
        # A reference is a paper that the current paper cites/uses.
        references = paper['references']
        for reference in references:
            referenceId = reference['paperId']
            referenceIsInfluential = reference['isInfluential']
            post_reference(paperId, referenceId, referenceIsInfluential)

        # Get all citations.
        # A citation is a paper that cites/uses the given paper.
        for citation in citations:
            citationId = citation['paperId']
            citationIsInfluential = citation['isInfluential']
            post_reference(citationId, paperId, citationIsInfluential)

        # Get all citations.
        # A citation is a paper that cites/uses the given paper.
        for citation in citations:
            citationId = citation['paperId']
            post_reference(citationId, paperId)

def get_all_papers():
    """Determine the ids of all relevant research papers."""
    neumann = 143993045
    valenzuela = 143990000
    li = 144000000
    grant = 144100000
    kemper = 144122431
    authorIds = [neumann, valenzuela, li, grant, kemper]
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

def post_paper(paper_id, paper_title, paper_abstract, paper_year, paper_citations):
    """Put the given paper into the database."""
    data = {'id':paper_id,
            'title':paper_title,
            'abstract':paper_abstract,
            'year':paper_year,
            'citations':paper_citations
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

def post_reference(source, sink, isInfluential):
    """Post the given reference into the database."""
    data = {'from_paper':source,
            'to_paper':sink,
            'is_influential': isInfluential,
            }
    r = requests.post(url='http://127.0.0.1:5000/reference/', json=data)
    print(r.status_code)

scrape()
