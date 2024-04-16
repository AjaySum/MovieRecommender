"""
Search index (main) view.

URLs include:
/
"""
import threading
import heapq
import time
import flask
import front
import requests


@front.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""
    # Extract the query and weight (weight is default 0.5) from search
    searchq = flask.request.args.get('q')
    if searchq is None:
        searchq = ""

    # connect to db
    context = {"q": searchq, "noresults": False}

    # Create a thread for each index server
    threads = []
    films = []
    for api_url in front.app.config['SEARCH_INDEX_SEGMENT_API_URLS']:
        thread = threading.Thread(target=request_index, args=(films, api_url, searchq, ))
        thread.start()
        threads.append(thread)
    # pass execution to the request_index function for a second
    # otherwise hits will not get populated
    time.sleep(0.1)
    for thread in threads:
        thread.join()
    context["recommend"] = films if films else []
    print(context)
    return flask.render_template("index.html", **context)

def request_index(films, api_url, searchq):
    """Send get requests to index servers and append results."""
    response = requests.get(api_url, params={"q": searchq}, timeout=None)
    # append dictionary to hits
    if response.status_code == 200:
        films.append(response.json()["recommend"])
