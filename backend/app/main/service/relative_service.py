"""Database service for relatives"""
from app.main import db


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

    connection = db.engine.connect()
    result = connection.execute(query)
    for row in result:
        print("username:", row)
    result = connection.execute(query)
    return result.first();
