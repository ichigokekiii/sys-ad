"""Lookup results a caller can see. The stand-in for get never opens a socket."""

import pytest

from ipinfo import current_mode, lookup, parse_forwarded, resolve_query_ip

PARTIAL_NOTICE = (
    "The location lookup is taking a break. The address below is still yours."
)
EMPTY_NOTICE = (
    "We could not find a public address right now. Refresh in a moment."
)


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


def scripted_get(routes):
    def get(url, timeout=None, headers=None):
        for fragment, payload in routes:
            if fragment in str(url):
                return FakeResponse(payload)
        return FakeResponse({}, status_code=599)

    return get


def test_ipwho_payload_fills_card_fields():
    payload = {
        "ip": "203.0.113.42",
        "success": True,
        "country": "Philippines",
        "country_code": "PH",
        "city": "Manila",
        "latitude": 14.5995,
        "longitude": 120.9842,
        "connection": {"isp": "PLDT", "asn": 9299},
    }
    result = lookup("203.0.113.42", get=scripted_get([("ipwho.is", payload)]))
    assert result.isp == "PLDT"
    assert result.asn == "AS9299"
    assert result.country_code == "PH"
    assert result.city == "Manila"
    assert result.latitude == 14.5995
    assert result.longitude == 120.9842
    assert result.source == "ipwho.is"


def test_ipapi_payload_is_used_when_ipwho_says_no():
    ipapi = {
        "ip": "1.1.1.1",
        "country": "US",
        "country_name": "United States",
        "city": "Los Angeles",
        "asn": "AS13335",
        "org": "Cloudflare, Inc.",
    }
    result = lookup(
        "1.1.1.1",
        get=scripted_get(
            [
                ("ipwho.is", {"success": False}),
                ("ipapi.co", ipapi),
            ]
        ),
    )
    assert result.source == "ipapi.co"
    assert result.country_code == "US"
    assert result.country == "United States"
    assert result.asn == "AS13335"


def test_ipify_supplies_address_and_partial_notice_only_without_an_ip():
    routes = [
        ("ipwho.is", {"success": False}),
        ("ipapi.co", {"error": True}),
        ("api.ipify.org", {"ip": "198.51.100.20"}),
    ]
    missed = lookup(None, get=scripted_get(routes))
    assert missed.query_ip == "198.51.100.20"
    assert missed.source == "ipify"
    assert missed.notice == PARTIAL_NOTICE
    assert missed.isp is None
    assert missed.asn is None
    assert missed.country_code is None
    assert missed.country is None
    assert missed.city is None
    assert missed.latitude is None
    assert missed.longitude is None

    kept = lookup(
        "203.0.113.42",
        get=scripted_get(
            [
                ("ipwho.is", {"success": False}),
                ("ipapi.co", {"success": False}),
                ("api.ipify.org", {"ip": "198.51.100.99"}),
            ]
        ),
    )
    assert kept.query_ip == "203.0.113.42"
    assert kept.source == "unavailable"
    assert kept.notice == PARTIAL_NOTICE


def test_parse_forwarded_keeps_the_client_address():
    assert parse_forwarded("203.0.113.5") == "203.0.113.5"
    assert parse_forwarded("203.0.113.5, 10.0.0.1") == "203.0.113.5"
    assert parse_forwarded(None) is None
    assert parse_forwarded("") is None
    assert parse_forwarded("   ") is None
    assert parse_forwarded("203.0.113.5:443") == "203.0.113.5"
    assert parse_forwarded("2001:db8:1::10") == "2001:db8:1::10"


def test_current_mode_defaults_and_render_hint():
    assert current_mode({}) == "direct"
    assert current_mode({"RENDER": "true"}) == "forwarded"
    assert current_mode({"LOOKUP_MODE": "direct", "RENDER": "true"}) == "direct"


def test_resolve_query_ip_follows_the_mode():
    header = "203.0.113.5, 10.0.0.1"
    assert resolve_query_ip("direct", header, "192.0.2.10") is None
    assert resolve_query_ip("forwarded", header, "192.0.2.10") == "203.0.113.5"
    assert resolve_query_ip("forwarded", None, "192.0.2.10") == "192.0.2.10"


@pytest.mark.parametrize(
    "error",
    [TimeoutError("timed out"), RuntimeError("lookup failed")],
)
def test_passed_ip_survives_a_timeout_or_an_exception(error):
    def get(url, timeout=None, headers=None):
        raise error

    result = lookup("203.0.113.42", get=get)
    assert result.query_ip == "203.0.113.42"
    assert result.source == "unavailable"
    assert result.notice == PARTIAL_NOTICE


def test_total_miss_without_an_ip_uses_the_empty_notice():
    def get(url, timeout=None, headers=None):
        raise RuntimeError("lookup failed")

    result = lookup(None, get=get)
    assert result.query_ip is None
    assert result.source == "unavailable"
    assert result.notice == EMPTY_NOTICE
