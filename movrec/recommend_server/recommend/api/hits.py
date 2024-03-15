"""REST API for recommend."""
import math
import re
import flask
import recommend
import requests

@recommend.app.route("/api/v1/")
def get_api():
    """Return a list of services available."""
    context = {
        "hits": "/api/v1/recommend/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


@recommend.app.route("/api/v1/recommend/")
def get_hits():
    """Return a list of recommended movies."""
    query = flask.request.args.get('q', None)
    if query is None or query == '':
        return flask.Response(status=400)
    
    print(query)
    context = {
                "recommend": ["Harry Potter", "The Lord of the Rings", "Top Gun", "Star Wars", "Moana", "Glee Club", "The Matrix", "The Godfather", "The Shawshank Redemption", "The Dark Knight"]
            }

    # Clean the query.
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = query.casefold().split()

    print(flask.jsonify(**context))
    return flask.jsonify(**context)

    # Get term count in query and store in dictionary.
    # Then get all of the tf*idf values of each term in the query.
    # This is the query vector.
    # Finally, calculate the normalization value of the query vector

    document_ids = set()
    # First get all the documents that contain all of the terms.

    for count, term in enumerate(query_terms.keys()):
        term_document_ids = set()
        documents = recommend.api.main.inv_index[term]["doc_attrs"]
        for document in documents.keys():
            term_document_ids.add(document)
        if count == 0:
            document_ids = term_document_ids.copy()
        else:
            document_ids = document_ids.intersection(term_document_ids)
        # If the initialization/intersection produces no documents at any point,
        # then it means the query will never have a result. Return empty dict of hits.
        if len(document_ids) == 0:
            context = {
                "hits": [],
            }
            return flask.jsonify(**context)

    # If hits exist, populate hits.
    hits = populate_hits(document_ids,query_terms,query_normalization,query_vector,weight)

    # Sort hits by score.
    sorted_hits = sorted(hits, key=lambda x: -x['score'])

    context = {
        "hits": sorted_hits,
    }
    return flask.jsonify(**context)

def get_query_information(query):
    """Get query information: norm, terms, tfidf of terms."""
    query_terms = {}
    term = None
    for term in query:
        query_terms[term] = query_terms.get(term, 0) + 1

    # Then get all of the tf*idf values of each term in the query.
    # This is the query vector.
    query_vector = []
    term = None
    tfreq = None
    for term, tfreq in query_terms.items():
        query_vector.append(tfreq * recommend.api.main.inv_index[term]["idf"])

    # Finally, calculate the normalization value of the query vector
    query_normalization = 0
    tf_idf = None
    for tf_idf in query_vector:
        query_normalization += tf_idf * tf_idf
    query_normalization = math.sqrt(query_normalization)

    return query_terms, query_vector, query_normalization

def populate_hits(document_ids,query_terms,query_normalization,query_vector,weight):
    """Populate hits from index with docid and score."""
    hits = []
    for document in document_ids:
        # Get all of the tf*idf values of each query term in the documents.
        # This is the document vector.
        document_vector = []
        term = None
        for term in query_terms:
            # print(index.api.main.inv_index[term])
            document_vector.append(
                recommend.api.main.inv_index[term]["doc_attrs"][document]["term_freq"]
                * recommend.api.main.inv_index[term]["idf"]
            )

        # Get the document normalization factor from the inverted index.
        document_normalization = math.sqrt(
            recommend.api.main.inv_index[term]["doc_attrs"][document]["norm_fact"]
        )

        # Calculate the tfidf(q, d) value.
        tfidf = 0
        for query_term, document_term in zip(query_vector, document_vector):
            tfidf += query_term * document_term

        tfidf /= query_normalization * document_normalization

        # Calculate the Score(q, d, w)
        score =float(weight)*recommend.api.main.page_rank[document]+(1-float(weight))*float(tfidf)
        # Write to hits
        hits.append({"docid": document, "score": score})
    return hits
