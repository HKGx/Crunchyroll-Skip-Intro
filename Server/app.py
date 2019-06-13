import logging
import time
from logging.handlers import RotatingFileHandler

from colors import color
from flask import Flask, g, request, Response
from flask_cors import CORS, cross_origin
from pony.flask import Pony

from db import Episode

IP = "localhost:5000"

app = Flask(__name__)
CORS(app)
Pony(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.before_request
def start_timer():
    g.start = time.time()


@app.after_request
def log_request(response: Response):
    now = time.time()
    duration = round(now - g.start, 2)

    log_params = [
        ('method', request.method, 'blue'),
        ('path', request.path, 'blue'),
        ('status', response.status_code, 'yellow'),
        ('duration', duration, 'green'),
        ('params', dict(request.args), 'blue')
    ]
    parts = []
    for name, value, c in log_params:
        part = color(f"{name}={value}", fg=c)
        parts.append(part)
    line = " ".join(parts)

    app.logger.info(line)
    return response


@app.route('/skipper/<int:episode>')
@cross_origin()
def get_skip(episode: int):
    episode = Episode.get(id=episode)
    if not episode:
        return (-1.0).__str__()
    return episode.intro_end.__str__()


if __name__ == '__main__':
    handler = RotatingFileHandler("logs.log", maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host=IP)
