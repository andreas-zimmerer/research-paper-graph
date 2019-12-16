"""Database service for relatives"""
from app.main import db
from collections import defaultdict


def get_all_relatives(title):
    """GET paper relatives by paper title"""
    query = "with recursive family(from_paper, title, abstract, year, to_paper) as (" \
            "select p.*, r.to_paper " \
            "from paper p, reference r " \
            "where p.id == r.from_paper and p.title == '" + title + "' " \
            "" \
            "UNION ALL " \
            "" \
            "select f.to_paper as from_paper, p.title, p.abstract, p.year, r.to_paper " \
            "from family f, reference r, paper p " \
            "where f.to_paper == r.from_paper and p.id == f.to_paper) " \
            "" \
            "select * " \
            "from family "

    result = db.engine.execute(query)

    dictionary = defaultdict(list)
    for row in result:
        id = row['from_paper']
        if id in dictionary:
            dictionary[id]['dependents'].append(row['to_paper'])
        else:
            dictionary[id] = {
                "id": id,
                "title": row['title'],
                "abstract": row['abstract'],
                "year": row['year'],
                "dependents": [row['to_paper']]
            }

    relatives = []
    for key in dictionary:
        relatives.append(dictionary[key])
    return relatives
