import arxiv
import argparse
import json
import urllib.request
from arxiv import Search
from datetime import datetime
import logging


def search_arxiv(query: str, category: str = "cs.CL", max_results: int = 200):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    current_date = datetime.now().date()
    papers = []
    for result in search.results():
        if category in result.categories and result.published == current_date:
            papers.append(result)
    print(len(papers))
    return papers


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str)
    parser.add_argument("--cateogory", type=str)


if __name__ == "__main__":
    args = parse()
    search_arxiv(args.query, args.category)
