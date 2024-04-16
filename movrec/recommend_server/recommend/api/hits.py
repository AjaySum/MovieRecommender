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


@recommend.app.route("/api/v1/recommend/")
def get_hits():
    """Return a list of recommended movies."""
    query = flask.request.args.get('q', None)
    print(query)
    if query is None or query == '':
        return flask.Response(status=400)
    
    print(query)
    context = {
                "recommend": []
            }
    
    this_c = recommend.api.c
    if not this_c.findId(query):
        return flask.response(status=400)
    
    context["recommend"] = this_c.calculateScore()
    print(context)

    return flask.jsonify(**context)
    
