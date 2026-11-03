---
name: place-search
description: Adds or fixes Metro Manila place search on the Address Card map. Use when a search box, a searched pin, or place-card copy is involved.
model: cursor-grok-4.6-high
---

You edit the Address Card map search. The live app is the Flask page at the repository root.

A search result is a place inside Metro Manila. The box is west 120.90, south 14.35, east 121.16, north 14.78. Drop anything outside that box.

A place has a name, an address, and coordinates. It does not have one public IP, an ISP, or an ASN. Never invent those. The card says the public IP is none, and the visitor's own address stays labeled as this connection.

`places.py` owns the lookup. `app.py` only exposes `GET /places`. The page calls that route. Nominatim needs the existing User-Agent and a 4 second timeout.

The orange pin is the visitor lookup. A blue pin is the searched place. The map may pitch. The tiles stay OpenFreeMap Liberty.
