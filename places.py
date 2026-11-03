"""Place search for the map. Metro Manila only.

A searched place has a name and coordinates. It does not have one public
IP, so this module never invents an address, an ISP, or an ASN.
"""

from __future__ import annotations

import requests

from ipinfo import USER_AGENT

# West, south, east, north. The box covers the Metro Manila cities and
# stops at the province line, so a hit in Laguna or Rizal does not land.
WEST = 120.90
SOUTH = 14.35
EAST = 121.16
NORTH = 14.78


def in_metro(latitude: float, longitude: float) -> bool:
    return SOUTH <= latitude <= NORTH and WEST <= longitude <= EAST


def search_places(query: str, fetch=None) -> list[dict]:
    text = " ".join((query or "").split())
    if len(text) < 2:
        return []
    fetch = fetch or _nominatim
    try:
        rows = fetch(text)
    except (requests.RequestException, OSError, ValueError, TypeError):
        return []
    if not isinstance(rows, list):
        return []
    places = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        try:
            latitude = float(row.get("lat"))
            longitude = float(row.get("lon"))
        except (TypeError, ValueError):
            continue
        if not in_metro(latitude, longitude):
            continue
        display = row.get("display_name") or ""
        name = row.get("name") or display.split(",")[0].strip() or "Unnamed place"
        places.append(
            {
                "name": name,
                "address": display or name,
                "latitude": latitude,
                "longitude": longitude,
            }
        )
        if len(places) == 5:
            break
    return places


def _nominatim(query: str):
    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={
            "q": query,
            "format": "jsonv2",
            "limit": 5,
            "countrycodes": "ph",
            "viewbox": f"{WEST},{NORTH},{EAST},{SOUTH}",
            "bounded": 1,
        },
        headers={"User-Agent": USER_AGENT},
        timeout=4,
    )
    response.raise_for_status()
    return response.json()
