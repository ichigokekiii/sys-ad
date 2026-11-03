"""Thin Flask shell for Address Card.

Gunicorn loads app:app. Lookup, roast, and grading live in the other
modules so this file only reads the request and fills the template.
"""

import os

from flask import Flask, jsonify, render_template, request

from fun import grade, map_embed, quiz_for, roast
from ipinfo import current_mode, lookup, resolve_query_ip
from places import search_places

app = Flask(__name__)


def _card_and_quiz():
    mode = current_mode(os.environ)
    query_ip = resolve_query_ip(
        mode,
        request.headers.get("X-Forwarded-For"),
        request.remote_addr,
    )
    card = lookup(query_ip)
    return card, quiz_for(card.isp)


def _render(card, quiz, quiz_result):
    # The template keys stay in one place so GET and POST cannot diverge.
    return render_template(
        "index.html",
        card=card,
        roast=roast(card.isp, card.country_code),
        quiz=quiz,
        quiz_result=quiz_result,
        map_src=map_embed(card.latitude, card.longitude),
        notice=card.notice,
    )


@app.get("/")
def index():
    card, quiz = _card_and_quiz()
    return _render(card, quiz, None)


@app.get("/places")
def places():
    return jsonify(search_places(request.args.get("q", "")))


@app.post("/quiz")
def quiz_post():
    # No session stores the answer. Look up again, rebuild the same quiz
    # from the ISP, and grade the posted choice on this request.
    card, quiz = _card_and_quiz()
    return _render(card, quiz, grade(quiz, request.form.get("choice")))
