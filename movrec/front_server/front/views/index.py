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

    fp_w = flask.request.args.get('fp_w')
    if fp_w is None:
        fp_w = 3
    
    s_w = flask.request.args.get('s_w')
    if s_w is None:
        s_w = 3

    d_w = flask.request.args.get('d_w')
    if d_w is None:
        d_w = 3

    c_w = flask.request.args.get('c_w')
    if c_w is None:
        c_w = 3

    y_w = flask.request.args.get('y_w')
    if y_w is None:
        y_w = 3
    
    g_w = flask.request.args.get('g_w')
    if g_w is None:
        g_w = 3
    

    # connect to db
    context = {"q": searchq, "fp_w": fp_w, "s_w": s_w, "d_w": d_w, "c_w": c_w, "y_w": y_w, "g_w": g_w, "noresults": False}

    # Create a thread for each index server
    threads = []
    films = []
    for api_url in front.app.config['SEARCH_INDEX_SEGMENT_API_URLS']:
        thread = threading.Thread(target=request_index, args=(films, api_url, searchq, fp_w, s_w, d_w, c_w, y_w, g_w,))
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

def request_index(films, api_url, searchq, fp_w, s_w, d_w, c_w, y_w, g_w):
    """Send get requests to index servers and append results."""
    response = requests.get(api_url, params={"q": searchq, "fp_w": fp_w, "s_w": s_w, "d_w": d_w, "c_w": c_w, "y_w": y_w, "g_w": g_w}, timeout=None)
    # append dictionary to hits
    if response.status_code == 200:
        films.append(response.json()["recommend"])
