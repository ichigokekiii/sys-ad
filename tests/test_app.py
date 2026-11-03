"""What the browser receives from GET / and POST /quiz."""

import re
from html import unescape

import requests

import app as server
from fun import quiz_for
from ipinfo import LookupResult

ADDRESS = "203.0.113.42"


def _card():
    return LookupResult(
        query_ip=ADDRESS,
        ipv4=ADDRESS,
        isp="PLDT",
        asn="AS9299",
        country_code="PH",
        country="Philippines",
        city="Manila",
        latitude=14.5995,
        longitude=120.9842,
        source="ipwho.is",
        notice=None,
    )


def _hidden_values(html):
    values = []
    for tag in re.findall(r"<input\b[^>]*>", html, flags=re.IGNORECASE):
        if not re.search(
            r"""\btype\s*=\s*["']hidden["']""",
            tag,
            flags=re.IGNORECASE,
        ):
            continue
        found = re.search(
            r"""\bvalue\s*=\s*["']([^"']*)["']""",
            tag,
            flags=re.IGNORECASE,
        )
        if found:
            values.append(found.group(1))
    return values


def _client(monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError("this test does not use live HTTP")

    monkeypatch.setattr(requests, "get", blocked)
    monkeypatch.setattr(server, "lookup", lambda ip, timeout=4, get=None: _card())
    server.app.config.update(TESTING=True)
    return server.app.test_client()


def test_get_shows_the_address_and_not_a_hidden_answer(monkeypatch):
    response = _client(monkeypatch).get("/")
    assert response.status_code == 200
    raw = response.get_data(as_text=True)
    body = unescape(raw)
    assert ADDRESS in body
    assert "api6.ipify.org" in body
    answer = quiz_for("PLDT").answer
    assert answer
    assert answer not in _hidden_values(raw)


def test_post_quiz_with_the_right_choice_shows_the_grade(monkeypatch):
    response = _client(monkeypatch).post("/quiz", data={"choice": "PLDT"})
    assert response.status_code == 200
    assert "That's the one." in unescape(response.get_data(as_text=True))
