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
        "recommend": "/api/v1/recommend/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


@recommend.app.route("/api/v1/titles/")
def get_titles():
    context = {
        "titles": [title for title in recommend.api.c.id_name.values()]
    }
    return flask.jsonify(**context)


@recommend.app.route("/api/v1/recommend/")
def get_hits():
    """Return a list of recommended movies."""
    query = flask.request.args.get('q', None)
    if query is None or query == '':
        return flask.Response(status=400)

    fp_w = int(flask.request.args.get('fp_w', 3))
    if fp_w is None:
        return flask.Response(status=400)

    s_w = int(flask.request.args.get('s_w', 3))
    if s_w is None:
        return flask.Response(status=400)
    
    d_w = int(flask.request.args.get('d_w', 3))
    if d_w is None:
        return flask.Response(status=400)
    
    c_w = int(flask.request.args.get('c_w', 3))
    if c_w is None:
        return flask.Response(status=400)
    
    y_w = int(flask.request.args.get('y_w', 3))
    if y_w is None:
        return flask.Response(status=400)

    g_w = int(flask.request.args.get('g_w', 3))
    if g_w is None:
        return flask.Response(status=400)
    
    l_w = int(flask.request.args.get('l_w', 3))
    if l_w is None:
        return flask.Response(status=400)
    
    context = {
                "recommend": []
            }
    
    this_c = recommend.api.c
    this_c.currLev = {"fp_w": fp_w, "s_w": s_w, "d_w": d_w, "c_w": c_w, "y_w": y_w, "g_w": g_w, "l_w": l_w}
    this_c.updateWeights()
    if not this_c.findId(query):
        return flask.response(status=400)
    
    recommended_movies = this_c.calculateScore()

    for movie, _ in recommended_movies:
        context["recommend"].append({
            "name": this_c.id_name[movie],
            "year": this_c.id_year[movie],
            "language": this_c.origin_language[movie][0],
            "genres": ", ".join([genre.capitalize() for genre in this_c.id_genres[movie]]),
            "summary": this_c.id_summary[movie]
        })
    print(context)

    return flask.jsonify(**context)
    
