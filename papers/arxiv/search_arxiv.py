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

    current_date = datetime.datetime.now().date() - datetime.timedelta(days=3)
    logging.info("Searching for papers on ate: {}".format(current_date))
    papers = []
    for result in search.results():
        print(result.published)
        if category in result.categories and result.published.date() == current_date:
            papers.append(result)
    logging.info("{} papers found".format(len(papers)))
    return papers


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str)
    parser.add_argument("--category", type=str)


if __name__ == "__main__":
    args = parse()
    search_arxiv(args.query, args.category)
