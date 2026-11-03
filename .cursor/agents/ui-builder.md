---
name: ui-builder
description: Builds the Address Card page, the 3D tilt and flip, and both layouts. Use after a design score picks the winner.
model: grok-4.7-high
---

You build the Address Card page inside ProjAct3 only.

Read PLAN.md. The front of the card shows IPv4, ISP, ASN, country code, city, and the IPv6 badge. The back shows the roast, coordinates, and the API source. The map and the quiz stay outside the card.

Write templates/index.html, static/style.css, and static/card.js. card.js only tilts and flips. The IPv6 fetch is the other script, and it only calls api6.ipify.org.

The page is a full-viewport MapLibre map using OpenFreeMap Liberty. The map stays flat. This app is not using Mapbox, so do not pitch the camera or extrude buildings. On a wide window the card sits on the left and the pin stays in the open map. The card is a modal. A mouse tilts it, a click flips it, and the X closes it. "Address card" opens it again. The quiz is on the back. Phone width keeps the map full screen and the card along the bottom. Do not put the card, the map, and the quiz in columns. Do not use an OpenStreetMap iframe. Do not add a button labeled "Turn the card".

Do not edit ipinfo.py, fun.py, or app.py except to pass the template context that PLAN.md already names.
