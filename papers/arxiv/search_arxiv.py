import arxiv
import argparse
import json
import urllib.request
from arxiv import Search
import datetime
import logging


def search_arxiv(query: str, category: str = "cs.CL", max_results: int = 200):
    print(query)
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    current_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
    print(current_date)
    papers = []
    for result in search.results():
        print(result.published)
        if category in result.categories and result.published.date() == current_date:
            papers.append(result)
    print(len(papers))
    return papers


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str)
    parser.add_argument("--category", type=str)


if __name__ == "__main__":
    args = parse()
    search_arxiv(args.query, args.category)
