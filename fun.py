"""Roast, quiz, and map URL for Address Card.

These functions are pure. The same ISP rebuilds the same quiz with no
session and no database, and nothing here opens a socket.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

# One sentence, shared by the empty quiz and by grading, so the page and
# the score cannot drift apart.
NO_PROVIDER = "The provider did not come back, so there is no guess this round."

# Longer fragments are checked first so a short name cannot steal a longer one.
_FRAGMENTS = (
    (
        "starlink",
        "Starlink drops this address at a ground station. The sky path and the pin are far apart.",
    ),
    (
        "cloudflare",
        "Cloudflare sits in front of many sites. The pin is an anycast node on that network.",
    ),
    (
        "converge",
        "Converge fiber reaches this network through a local node. The pin marks that equipment.",
    ),
    (
        "google",
        "Google answers from its own network. The pin is a data center on that network.",
    ),
    (
        "globe",
        "Globe handed this address to a cell site. The pin sits on that network gear.",
    ),
    (
        "pldt",
        "PLDT brought you here the long way around. The pin is probably a building you have never visited.",
    ),
    (
        "dito",
        "DITO is still building its own routes. The pin is a tower or a handoff on that network.",
    ),
    (
        "sky",
        "Sky parks this address on a regional headend. The pin follows the cable plant.",
    ),
)

_PH_LINE = (
    "This address is announced in the Philippines. The pin is often the provider's equipment."
)
_GENERIC_LINE = (
    "The pin marks where this network announces the address. It follows the provider's equipment."
)

_DECOYS = (
    "PLDT",
    "Globe",
    "Converge",
    "DITO",
    "Starlink",
    "Sky Cable",
    "Google",
    "Cloudflare",
    "Amazon",
    "Akamai",
)


@dataclass(frozen=True)
class Quiz:
    prompt: str
    choices: tuple[str, ...]
    answer: str | None


def roast(isp, country_code) -> str:
    lowered = "" if isp is None else str(isp).lower()
    ordered = sorted(_FRAGMENTS, key=lambda item: len(item[0]), reverse=True)
    for fragment, line in ordered:
        if fragment in lowered:
            return line
    if str(country_code or "").strip().upper() == "PH":
        return _PH_LINE
    return _GENERIC_LINE


def quiz_for(isp) -> Quiz:
    if isp is None or not str(isp).strip():
        return Quiz(NO_PROVIDER, (), None)
    real = str(isp).strip()
    # Built-in hash changes every process. sha256 of the lowered name keeps
    # the same three choices after a refresh, which is how grading works
    # with no saved session.
    key = real.lower()
    pool = [name for name in _DECOYS if name != real]
    picked = sorted(pool, key=lambda name: _digest(key, name))[:2]
    choices = _shuffle((real, picked[0], picked[1]), key)
    return Quiz("Which network is this?", choices, real)


def grade(quiz, choice) -> str:
    if quiz.answer is None:
        return NO_PROVIDER
    if choice == quiz.answer:
        return "Correct."
    return f"Close. This network is {quiz.answer}."


def map_embed(lat, lon):
    if lat is None or lon is None:
        return None
    try:
        latitude = float(lat)
        longitude = float(lon)
    except (TypeError, ValueError):
        return None
    if latitude != latitude or longitude != longitude:
        return None
    # OSM wants west, south, east, north. 0.05 degrees frames the pin
    # without a map library. Commas are encoded so the query stays one value.
    west = longitude - 0.05
    south = latitude - 0.05
    east = longitude + 0.05
    north = latitude + 0.05
    bbox = "%2C".join(f"{number:.6f}" for number in (west, south, east, north))
    marker = "%2C".join(f"{number:.6f}" for number in (latitude, longitude))
    return (
        "https://www.openstreetmap.org/export/embed.html"
        f"?bbox={bbox}&layer=mapnik&marker={marker}"
    )


def _digest(key, name) -> str:
    return hashlib.sha256(f"{key}\n{name}".encode("utf-8")).hexdigest()


def _shuffle(items, key) -> tuple[str, ...]:
    bag = list(items)
    for index in range(len(bag) - 1, 0, -1):
        digest = hashlib.sha256(f"{key}\n{index}".encode("utf-8")).digest()
        swap = int.from_bytes(digest[:8], "big") % (index + 1)
        bag[index], bag[swap] = bag[swap], bag[index]
    return tuple(bag)
