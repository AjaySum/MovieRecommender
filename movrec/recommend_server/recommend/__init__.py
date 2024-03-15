"""Index package initializer."""
import os
import flask

app = flask.Flask(__name__)  # pylint: disable=invalid-name

import recommend.api  # noqa: E402  pylint: disable=wrong-import-position
