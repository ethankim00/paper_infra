import json
import urllib.request


from papers.arxiv.search_arxiv import search_arxiv


def invoke(request):
    requestJson = json.dumps(request).encode("utf-8")
    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request("http://localhost:8765", requestJson)
        )
    )
    print(response)


def paper_to_anki(paper):
    print(paper)

    request = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "Abstracts",
                "modelName": "Abstracts",
                "fields": {
                    "Title": paper.title,
                    "Abstract": paper.summary,
                    "Authors": ", ".join([str(author) for author in paper.authors]),
                    "Date": str(paper.published),
                },
                "options": {
                    "allowDuplicate": False,
                    "duplicateScope": "deck",
                    "duplicateScopeOptions": {
                        "deckName": "Default",
                        "checkChildren": False,
                        "checkAllModels": False,
                    },
                },
                "tags": [
                    "machinelearning::papers::{}".format("".join(paper.title.split())),
                    "machinelearning::arxiv",
                ],
            }
        },
    }
    return request


if __name__ == "__main__":

    papers = search_arxiv("information retrieval", "cs.CL")

    for paper in papers:
        query = paper_to_anki(paper)
        invoke(query)
