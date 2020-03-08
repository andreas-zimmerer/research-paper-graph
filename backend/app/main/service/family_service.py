"""Family Service"""
from collections import defaultdict
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from app.main import db

def get_preceding(relative, distance, year, citations):
    """List all preceding relatives of a paper."""
    distance, year, citations = correct_filters(distance, year, citations)
    family_query = create_preceding_family_query(relative, distance, year, citations)
    preceding_paper_list = get(relative, family_query)
    return preceding_paper_list

def get_succeeding(relative, distance, year, citations):
    """List all succeeding relatives of a paper."""
    distance, year, citations = correct_filters(distance, year, citations)
    family_query = create_succeeding_family_query(relative, distance, year, citations)
    succeeding_paper_list = get(relative, family_query)
    return succeeding_paper_list

def get_entire(relative, distance, year, citations):
    """List all succeeding relatives of a paper."""
    distance, year, citations = correct_filters(distance, year, citations)
    family_query = create_entire_family_query(relative, distance, year, citations)
    entire_paper_list = get(relative, family_query)
    return entire_paper_list

def correct_filters(distance, year, citations):
    """If a filter is too big or too small, set it to a default value."""
    distance = int(distance)
    distance = min(distance, 5)
    distance = max(distance, 0)
    year = int(year)
    citations = int(citations)
    citations = max(citations, 1)
    return distance, year, citations

def create_preceding_family_query(relative, distance, year, citations):
    """Get the preceding family of the given paper."""
    query = """
            with recursive family(from_id, from_title, from_abstract, from_year, from_is_influential, from_citations, from_author, to_id, to_title, to_abstract, to_year, to_is_influential, to_citations, to_author, distance) as 
                (select fp.id as from_id, fp.title as from_title, fp.abstract as from_abstract, fp.year as from_year, false as from_is_influential, fp.citations as from_citations, fa.name as from_author, tp.id as to_id, tp.title as to_title, tp.abstract as to_abstract, tp.year as to_year, r.is_influential as to_is_influential, tp.citations as to_citations, ta.name as to_author, 1 as distance 
                from paper fp, write fw, author fa, reference r, paper tp, write tw, author ta 
                where fp.title = '{title}' and fp.id = fw.paper and fw.author = fa.id and fp.id = r.from_paper and r.to_paper = tp.id and tp.id = tw.paper and tw.author = ta.id and tp.year >= {year} and tp.citations >= {citations}
            
                union all 
            
                select f.to_id as from_id, f.to_title as from_title, f.to_abstract as from_abstract, f.to_year as from_year, f.from_is_influential as from_is_influential, f.to_citations as from_citations, f.to_author as from_author, tp.id as to_id, tp.title as to_title, tp.abstract as to_abstract, tp.year as to_year, false as to_is_influential, tp.citations as to_citations, ta.name as to_author, f.distance + 1 as distance 
                from family f, reference r, paper tp, write tw, author ta 
                where f.distance < {distance} and tp.year >= {year} and tp.citations >= {citations} and f.to_id = r.from_paper and r.to_paper = tp.id and tp.id = tw.paper and tw.author = ta.id) 
            
            select * 
            from family
            """.format(title=relative, distance=distance, year=year, citations=citations)
    return query

def create_succeeding_family_query(relative, distance, year, citations):
    """Get the succeeding family of the given paper."""
    query = """
            with recursive family(from_id, from_title, from_abstract, from_year, from_is_influential, from_citations, from_author, to_id, to_title, to_abstract, to_year, to_is_influential, to_citations, to_author, distance) as 
                (select fp.id as from_id, fp.title as from_title, fp.abstract as from_abstract, fp.year as from_year, r.is_influential as from_is_influential, fp.citations as from_citations, fa.name as from_author, tp.id as to_id, tp.title as to_title, tp.abstract as to_abstract, tp.year as to_year, false as to_is_influential, tp.citations as to_citations, ta.name as to_author, 1 as distance 
                from paper fp, write fw, author fa, reference r, paper tp, write tw, author ta 
                where tp.title = '{title}' and fp.id = fw.paper and fw.author = fa.id and fp.id = r.from_paper and r.to_paper = tp.id and tp.id = tw.paper and tw.author = ta.id and fp.year >= {year} and fp.citations >= {citations}
            
                union all 
            
                select f.from_id as to_id, f.from_title as to_title, f.from_abstract as to_abstract, f.from_year as to_year, f.from_is_influential as to_is_influential, f.from_citations as to_citations, f.from_author as to_author, fp.id as from_id, fp.title as from_title, fp.abstract as from_abstract, fp.year as from_year, false as from_is_influential, fp.citations as from_citations, fa.name as from_author, f.distance + 1 as distance 
                from family f, reference r, paper fp, write fw, author fa 
                where f.distance < {distance} and fp.year >= {year} and fp.citations >= {citations} and f.from_id = r.to_paper and r.from_paper = fp.id and fp.id = fw.paper and fw.author = fa.id) 
            
            select * 
            from family
            """.format(title=relative, distance=distance, year=year, citations=citations)
    return query

def create_entire_family_query(relative, distance, year, citations):
    """Get the entire family of the given paper."""
    query = """
            with recursive duplicates(from_paper, to_paper, is_influential) as 
                (select from_paper as from_paper, to_paper as to_paper, is_influential as is_influential
                from reference 
                
                union all 
                
                select to_paper as from_paper, from_paper as to_paper, is_influential as is_influential
                from reference),
                
            family(from_id, from_title, from_abstract, from_year, from_is_influential, from_citations, from_author, to_id, to_title, to_abstract, to_year, to_is_influential, to_citations, to_author, distance) as 
                (select fp.id as from_id, fp.title as from_title, fp.abstract as from_abstract, fp.year as from_year, false as from_is_influential, fp.citations as from_citations, fa.name as from_author, tp.id as to_id, tp.title as to_title, tp.abstract as to_abstract, tp.year as to_year, d.is_influential as to_is_influential, tp.citations as to_citations, ta.name as to_author, 1 as distance 
                from paper fp, write fw, author fa, duplicates d, paper tp, write tw, author ta 
                where fp.title = '{title}' and fp.id = fw.paper and fw.author = fa.id and fp.id = d.from_paper and d.to_paper = tp.id and tp.id = tw.paper and tw.author = ta.id and tp.year >= {year} and tp.citations >= {citations}
            
                union all 
            
                select f.to_id as from_id, f.to_title as from_title, f.to_abstract as from_abstract, f.to_year as from_year, f.from_is_influential as from_is_influential, f.to_citations as from_citations, f.to_author as from_author, tp.id as to_id, tp.title as to_title, tp.abstract as to_abstract, tp.year as to_year, false as to_is_influential, tp.citations as to_citations, ta.name as to_author, f.distance + 1 as distance 
                from family f, duplicates d, paper tp, write tw, author ta 
                where f.distance < {distance} and tp.year >= {year} and tp.citations >= {citations} and f.to_id = d.from_paper and d.to_paper = tp.id and tp.id = tw.paper and tw.author = ta.id) 
            
            select * 
            from family
            """.format(title=relative, distance=distance, year=year, citations=citations)
    return query

def get(relative, family_query):
    """List all relatives of a paper."""
    default_query = create_default_query(relative)
    paper_dictionary = create_papers(family_query, default_query)
    paper_list = paper_dictionary_to_paper_list(paper_dictionary)
    sorted_paper_list = sort_paper_list(paper_list)
    sorted_paper_list = add_clusters(sorted_paper_list)
    return sorted_paper_list

def create_default_query(relative):
    """Get the given paper."""
    query = """
            select p.id as from_id, p.title as from_title, p.abstract as from_abstract, p.year as from_year, false as from_is_influential, p.citations as from_citations, a.name as from_author
            from paper p, write w, author a 
            where p.title = '{title}' and p.id = w.paper and w.author = a.id
            """.format(title=relative)
    return query

def create_papers(family_query, default_query):
    """Transform the query format to a dictionary format."""
    paper_dictionary = defaultdict(list)
    papers = db.engine.execute(family_query)
    paper_dictionary = add_family(paper_dictionary, papers)
    if len(paper_dictionary) == 0:
        papers = db.engine.execute(default_query)
        paper_dictionary = add_default_paper(paper_dictionary, papers)
    return paper_dictionary

def add_family(paper_dictionary, papers):
    """Add a family to the dictionary."""
    for paper in papers:
        paper_dictionary = add_paper(paper_dictionary, paper, 'from')
        paper_dictionary = add_paper(paper_dictionary, paper, 'to')
        from_id = paper['from_id']
        to_id = paper['to_id']
        references = paper_dictionary[from_id]['references']
        if to_id not in references:
            references.append(to_id)
    return paper_dictionary

def add_default_paper(paper_dictionary, papers):
    """Add the given paper to the dictionary."""
    for paper in papers:
        paper_dictionary = add_paper(paper_dictionary, paper, 'from')
    return paper_dictionary

def add_paper(paper_dictionary, paper, direction):
    """Add a paper to the dictionary."""
    paper_id = paper[direction + '_id']
    paper_title = paper[direction + '_title']
    paper_abstract = paper[direction + '_abstract']
    paper_year = paper[direction + '_year']
    paper_is_influential = paper[direction + '_is_influential']
    paper_citations = paper[direction + '_citations']
    paper_author = paper[direction + '_author']
    paper = create_paper(paper_id, paper_title, paper_abstract, paper_year, paper_citations)
    paper_dictionary.setdefault(paper_id, paper)
    is_influential = paper_dictionary[paper_id]['is_influential']
    if not is_influential:
        paper_dictionary[paper_id]['is_influential'] = paper_is_influential
    authors = paper_dictionary[paper_id]['authors']
    if paper_author not in authors:
        authors.append(paper_author)
    return paper_dictionary

def create_paper(paper_id, paper_title, paper_abstract, paper_year, paper_citations):
    """Initialize a paper."""
    paper = {
        "id": paper_id,
        "title": paper_title,
        "abstract": paper_abstract,
        "year": paper_year,
        "is_influential": False,
        "citations": paper_citations,
        "cluster": 0,
        "references": [],
        "authors": []
    }
    return paper

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
