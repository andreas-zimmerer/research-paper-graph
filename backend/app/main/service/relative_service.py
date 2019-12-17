"""Database service for relatives"""
from app.main import db
from collections import defaultdict


def get_all_relatives(title):
    """GET paper relatives by paper title"""
    query = "with recursive family(from_paper, from_title, from_abstract, from_year, to_paper, to_title, to_abstract, to_year) as (" \
            "select pf.id, pf.title, pf.abstract, pf.year, pt.id, pt.title, pt.abstract, pt.year " \
            "from paper pf, reference r, paper pt " \
            "where pf.id == r.from_paper and pf.title == '" + title + "' and pt.id == r.to_paper " \
            "" \
            "UNION ALL " \
            "" \
            "select f.to_paper as from_paper, f.to_title as from_title, f.to_abstract as from_abstract, f.to_year as from_year, pt.id as to_paper, pt.title as to_title, pt.abstract as to_abstract, pt.year as to_year " \
            "from family f, reference r, paper pt " \
            "where f.to_paper == r.from_paper and pt.id == r.to_paper) " \
            "" \
            "select * " \
            "from family "

    resultNode = db.engine.execute(query)
    resultLink = db.engine.execute(query)

    dictionary = defaultdict(list)
    for row in resultNode:
        from_paper = row['from_paper']
        to_paper = row['to_paper']
        dictionary[from_paper] = {
            "id": from_paper,
            "title": row['from_title'],
            "abstract": row['from_abstract'],
            "year": row['from_year'],
            "citations": [],
            "authors": [],
        }
        dictionary[to_paper] = {
            "id": to_paper,
            "title": row['to_title'],
            "abstract": row['to_abstract'],
            "year": row['to_year'],
            "citations": [],
            "authors": []
        }

    for row in resultLink:
        from_paper = row['from_paper']
        dictionary[from_paper]['citations'].append(row['to_paper'])

    relatives = []
    for key in dictionary:
        relatives.append(dictionary[key])
    return relatives
