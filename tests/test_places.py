"""Metro Manila place search. No network."""

from places import search_places


def test_short_query_skips_the_lookup():
    assert search_places(" ") == []
    assert search_places("a", fetch=lambda query: [_hit("Cebu", 10.3, 123.9)]) == []


def test_drops_places_outside_metro_manila():
    rows = [
        _hit("Cebu", 10.3, 123.9),
        _hit("Quiapo", 14.599, 120.984),
    ]
    places = search_places("Quiapo", fetch=lambda query: rows)
    assert [place["name"] for place in places] == ["Quiapo"]
    assert places[0]["address"] == "Quiapo, Manila, Metro Manila"


def test_a_failed_lookup_returns_nothing():
    def fetch(query):
        raise OSError("down")

    assert search_places("Quiapo", fetch=fetch) == []


def _hit(name, latitude, longitude):
    return {
        "name": name,
        "display_name": f"{name}, Manila, Metro Manila",
        "lat": str(latitude),
        "lon": str(longitude),
    }
