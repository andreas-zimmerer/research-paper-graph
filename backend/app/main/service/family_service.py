"""Family Service"""
from collections import defaultdict
from app.main import db

def get(relative, distance, year, citations):
    """List all relatives of a paper."""
    distance = int(distance)
    distance = max(1, distance)
    distance = min(3, distance)

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
            "select f.*, r.relevance " \
            "from family f inner join " \
                "(select to_paper, count(to_paper) as relevance " \
                "from family " \
                "group by to_paper) r " \
            "on f.to_paper = r.to_paper " \
            "where r.relevance > " + str(citations) + " "

    connectionsA = db.engine.execute(query)
    connectionsB = db.engine.execute(query)

    dictionary = defaultdict(list)
    for connection in connectionsA:
        from_paper = connection['from_paper']
        to_paper = connection['to_paper']
        dictionary[from_paper] = {
            "id": from_paper,
            "title": connection['from_title'],
            "abstract": connection['from_abstract'],
            "year": connection['from_year'],
            "citations": [],
            "authors": [],
        }
        dictionary[to_paper] = {
            "id": to_paper,
            "title": connection['to_title'],
            "abstract": connection['to_abstract'],
            "year": connection['to_year'],
            "citations": [],
            "authors": []
        }

    for connection in connectionsB:
        from_paper = connection['from_paper']
        dictionary[from_paper]['citations'].append(connection['to_paper'])

    family = []
    for key in dictionary:
        family.append(dictionary[key])
    family = sorted(family, key=lambda paper: paper['year'])
    return family
