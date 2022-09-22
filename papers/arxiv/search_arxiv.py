import arxiv
import argparse
import json
import urllib.request
from arxiv import Search
import datetime
import logging


def search_arxiv(query: str, category: str = "cs.CL", max_results: int = 200):
    logging.info(
        "Searching arxiv for papers with query {} in category {}".format(
            query, category
        )
    )
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    current_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
    logging.info("Searching for papers on date: {}".format(current_date))
    papers = []
    for result in search.results():
        if (
            category in result.categories
        ):  # " #and result.published.date() == current_date:
            print(result.title)
            papers.append(result)
    logging.info("{} papers found".format(len(papers)))
    return papers


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str)
    parser.add_argument("--category", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse()
    search_arxiv(args.query, args.category)
