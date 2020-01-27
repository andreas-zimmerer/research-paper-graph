"""Family Service"""
from collections import defaultdict
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from app.main import db

def get(relative, distance, year, citations):
    """List all relatives of a paper."""
    distance, year, citations = correct_filters(distance, year, citations)
    query = create_query(relative, distance, year, citations)
    paper_query = create_paper_query(relative, distance, year, citations)
    citations_query = create_citations_query(relative, distance, year, citations)
    author_query = create_author_query(relative, distance, year, citations)
    paper_dictionary = create_papers(paper_query)
    paper_dictionary = add_citations(citations_query, paper_dictionary)
    paper_dictionary = add_authors(author_query, paper_dictionary)
    paper_list = paper_dictionary_to_paper_list(paper_dictionary)
    sorted_paper_list = sort_paper_list(paper_list)
    sorted_paper_list = add_clusters(sorted_paper_list)
    return sorted_paper_list

def correct_filters(distance, year, citations):
    """If a filter is too big or too small, set it to a default value."""
    distance = int(distance)
    distance = min(distance, 3)
    distance = max(distance, 1)
    year = int(year)
    citations = int(citations)
    citations = max(citations, 1)
    return distance, year, citations

def create_paper_query(relative, distance, year, citations):
    query = "with recursive family(from_paper, from_title, from_abstract, from_year, to_paper, " \
            "to_title, to_abstract, to_year, to_distance) as (" \
            "select distinct pf.id, pf.title, pf.abstract, pf.year, pt.id, pt.title, " \
            "pt.abstract, pt.year, 1 " \
            "from paper pf, reference r, paper pt " \
            "where pf.id = r.from_paper and pf.title like '" + relative + \
            "' and pt.id = r.to_paper and pt.year > " + str(year) + " " \
            "" \
            "UNION ALL " \
            "" \
            "select f.to_paper as from_paper, f.to_title as from_title, f.to_abstract as " \
            "from_abstract, f.to_year as from_year, pt.id as to_paper, pt.title as " \
            "to_title, pt.abstract as to_abstract, pt.year as to_year, f.to_distance + 1 " \
            "from family f, reference r, paper pt " \
            "where f.to_distance < " + str(distance) + " and f.to_paper = r.from_paper and " \
            "pt.id = r.to_paper and pt.year > " + str(year) + "), " \
            "" \
            "basics(from_paper, from_title, from_abstract, from_year, to_paper, to_title, to_abstract, to_year, to_distance, relevance, from_author, to_author) as ( " \
            "select distinct f.*, r.relevance, fa.name as from_author, ta.name as to_author " \
            "from family f inner join " \
            "(select to_paper, count(to_paper) as relevance " \
            "from family " \
            "group by to_paper) r " \
            "on f.to_paper = r.to_paper, author fa, write fw, author ta, write tw " \
            "where r.relevance > " + str(citations) + " and fw.author = fa.id and fw.paper = f.from_paper and tw.author = ta.id and tw.paper = f.to_paper) " \
            "" \
            "select distinct from_paper as paper, from_title as title, from_abstract as abstract, from_year as year " \
            "from basics " \
            "" \
            "UNION " \
            "" \
            "select distinct to_paper as paper, to_title as title, to_abstract as abstract, to_year as year " \
            "from basics "
    return query

def create_citations_query(relative, distance, year, citations):
    query = "with recursive family(from_paper, from_title, from_abstract, from_year, to_paper, " \
            "to_title, to_abstract, to_year, to_distance) as (" \
            "select distinct pf.id, pf.title, pf.abstract, pf.year, pt.id, pt.title, " \
            "pt.abstract, pt.year, 1 " \
            "from paper pf, reference r, paper pt " \
            "where pf.id = r.from_paper and pf.title like '" + relative + \
            "' and pt.id = r.to_paper and pt.year > " + str(year) + " " \
            "" \
            "UNION ALL " \
            "" \
            "select f.to_paper as from_paper, f.to_title as from_title, f.to_abstract as " \
            "from_abstract, f.to_year as from_year, pt.id as to_paper, pt.title as " \
            "to_title, pt.abstract as to_abstract, pt.year as to_year, f.to_distance + 1 " \
            "from family f, reference r, paper pt " \
            "where f.to_distance < " + str(distance) + " and f.to_paper = r.from_paper and " \
            "pt.id = r.to_paper and pt.year > " + str(year) + "), " \
            "" \
            "basics(from_paper, from_title, from_abstract, from_year, to_paper, to_title, to_abstract, to_year, to_distance, relevance, from_author, to_author) as ( " \
            "select distinct f.*, r.relevance, fa.name as from_author, ta.name as to_author " \
            "from family f inner join " \
            "(select to_paper, count(to_paper) as relevance " \
            "from family " \
            "group by to_paper) r " \
            "on f.to_paper = r.to_paper, author fa, write fw, author ta, write tw " \
            "where r.relevance > " + str(citations) + " and fw.author = fa.id and fw.paper = f.from_paper and tw.author = ta.id and tw.paper = f.to_paper) " \
            "" \
            "select distinct from_paper, to_paper " \
            "from basics "
    return query

def create_author_query(relative, distance, year, citations):
    query = "with recursive family(from_paper, from_title, from_abstract, from_year, to_paper, " \
            "to_title, to_abstract, to_year, to_distance) as (" \
            "select distinct pf.id, pf.title, pf.abstract, pf.year, pt.id, pt.title, " \
            "pt.abstract, pt.year, 1 " \
            "from paper pf, reference r, paper pt " \
            "where pf.id = r.from_paper and pf.title like '" + relative + \
            "' and pt.id = r.to_paper and pt.year > " + str(year) + " " \
            "" \
            "UNION ALL " \
            "" \
            "select f.to_paper as from_paper, f.to_title as from_title, f.to_abstract as " \
            "from_abstract, f.to_year as from_year, pt.id as to_paper, pt.title as " \
            "to_title, pt.abstract as to_abstract, pt.year as to_year, f.to_distance + 1 " \
            "from family f, reference r, paper pt " \
            "where f.to_distance < " + str(distance) + " and f.to_paper = r.from_paper and " \
            "pt.id = r.to_paper and pt.year > " + str(year) + "), " \
            "" \
            "basics(from_paper, from_title, from_abstract, from_year, to_paper, to_title, to_abstract, to_year, to_distance, relevance, from_author, to_author) as ( " \
            "select distinct f.*, r.relevance, fa.name as from_author, ta.name as to_author " \
            "from family f inner join " \
            "(select to_paper, count(to_paper) as relevance " \
            "from family " \
            "group by to_paper) r " \
            "on f.to_paper = r.to_paper, author fa, write fw, author ta, write tw " \
            "where r.relevance > " + str(citations) + " and fw.author = fa.id and fw.paper = f.from_paper and tw.author = ta.id and tw.paper = f.to_paper) " \
            "" \
            "select distinct from_paper as paper, from_author as author " \
            "from basics " \
            "" \
            "UNION " \
            "" \
            "select distinct to_paper as paper, to_author as author " \
            "from basics "
    return query

def create_query(relative, distance, year, citations):
    """Create the query that gets all the relatives of the paper."""
    query = "with recursive family(from_paper, from_title, from_abstract, from_year, to_paper, " \
            "to_title, to_abstract, to_year, to_distance) as (" \
            "select distinct pf.id, pf.title, pf.abstract, pf.year, pt.id, pt.title, " \
            "pt.abstract, pt.year, 1 " \
            "from paper pf, reference r, paper pt " \
            "where pf.id = r.from_paper and pf.title like '" + relative + \
            "' and pt.id = r.to_paper and pt.year > " + str(year) + " " \
            "" \
            "UNION ALL " \
            "" \
            "select f.to_paper as from_paper, f.to_title as from_title, f.to_abstract as " \
            "from_abstract, f.to_year as from_year, pt.id as to_paper, pt.title as " \
            "to_title, pt.abstract as to_abstract, pt.year as to_year, f.to_distance + 1 " \
            "from family f, reference r, paper pt " \
            "where f.to_distance < " + str(distance) + " and f.to_paper = r.from_paper and " \
            "pt.id = r.to_paper and pt.year > " + str(year) + ") " \
            "" \
            "select distinct f.*, r.relevance, fa.name as from_author, ta.name as to_author " \
            "from family f inner join " \
            "(select to_paper, count(to_paper) as relevance " \
            "from family " \
            "group by to_paper) r " \
            "on f.to_paper = r.to_paper, author fa, write fw, author ta, write tw " \
            "where r.relevance > " + str(citations) + " and fw.author = fa.id and fw.paper = f.from_paper and tw.author = ta.id and tw.paper = f.to_paper "
    return query

def create_papers(paper_query):
    """Transform the query format to a dictionary format."""
    papers = db.engine.execute(paper_query)
    paper_dictionary = defaultdict(list)
    for paper in papers:
        from_paper = paper['paper']
        paper_dictionary[from_paper] = {
            "id": from_paper,
            "title": paper['title'],
            "abstract": paper['abstract'],
            "year": paper['year'],
            "cluster": 0,
            "citations": [],
            "authors": [],
        }
    return paper_dictionary

def add_citations(citations_query, paper_dictionary):
    """Fill the citation field of every paper in the dictionary."""
    citations = db.engine.execute(citations_query)
    for citation in citations:
        from_paper = citation['from_paper']
        paper_dictionary[from_paper]['citations'].append(citation['to_paper'])
    return paper_dictionary

def add_authors(author_query, paper_dictionary):
    """Fill the author field of every paper in the dictionary."""
    writes = db.engine.execute(author_query)
    for write in writes:
        from_paper = write['paper']
        paper_dictionary[from_paper]['authors'].append(write['author'])
    return paper_dictionary

def paper_dictionary_to_paper_list(paper_dictionary):
    """Transform the paper dictionary into a data list."""
    paper_list = []
    for key in paper_dictionary:
        paper_list.append(paper_dictionary[key])
    return paper_list

def sort_paper_list(paper_list):
    """Sort the paper list by paper year."""
    keyfunc = lambda paper: paper['year']
    sorted_paper_list = sorted(paper_list, key=keyfunc)
    return sorted_paper_list

def add_clusters(sorted_paper_list):
    """Cluster the papers by abstract keywords. Assign each paper its cluster."""
    if len(sorted_paper_list) == 0:
        return sorted_paper_list

    abstract_list = extract_abstracts(sorted_paper_list)
    vectorizer, model = train_clusters(abstract_list)
    sorted_paper_list = predict_clusters(sorted_paper_list, vectorizer, model)
    return sorted_paper_list

def extract_abstracts(papers):
    """Extract an abstract list from the paper list."""
    abstracts = []
    for paper in papers:
        abstracts.append(paper['abstract'])
    return abstracts

def train_clusters(abstract_list):
    """Train the clustering algorithm."""
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(abstract_list)
    true_k = min(4, len(abstract_list))
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)
    return vectorizer, model

def predict_clusters(sorted_paper_list, vectorizer, model):
    """Cluster all papers by their abstract keywords."""
    for paper in sorted_paper_list:
        prediction = predict_cluster(vectorizer, model, paper['abstract'])
        paper['cluster'] = prediction
    return sorted_paper_list

def predict_cluster(vectorizer, model, abstract):
    """Map the given abstract to its cluster."""
    Y = vectorizer.transform([abstract])
    prediction = model.predict(Y)
    return prediction[0]
