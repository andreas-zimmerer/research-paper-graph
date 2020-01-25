#!/usr/bin/python

import json
import requests 

start_paper = '0796f6cd7f0403a854d67d525e9b32af3b277331'

paper_stack = [start_paper]
paper_count = 0


while paper_count < 25:
    try:
        paper_id = paper_stack.pop(0)
        json_data = requests.get(url='http://api.semanticscholar.org/v1/paper/' + paper_id).json()
        
        id = json_data['paperId']
        title = json_data['title']
        abstract = json_data['abstract']
        year = json_data['year']
        references = json_data['references']
        citations = json_data['citations']

        paper = {
            "id": id,
            "title": title[:255],
            "abstract": abstract[:255],
            "year": year
        }

        refs = []
        for r in references:
            paper_stack.append(r["paperId"])
            refs.append({
                "from_paper": id,
                "to_paper": r["paperId"]
            })

        r = requests.post(url = "http://localhost:5000/paper/", json = paper)
        
        for c in refs:
            requests.post(url = "http://localhost:5000/reference/", json = c)
        
        paper_count += 1
    except:
        print("Error")
