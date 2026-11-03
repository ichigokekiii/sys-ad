# Address Card demo

A 10 to 15 minute talk for a phone and a laptop. Speak from the page that is actually running. The repository is https://github.com/ichigokekiii/sys-ad. Render is still `[Render live link to be added]`. `REFLECTION.md` is a draft, so rewrite it before you read it aloud.

## Minutes

1. Why this option, about 2 minutes.
2. The four features, about 2 minutes.
3. The files, about 2 minutes.
4. Live demo on the laptop and the phone, about 5 minutes.
5. LAN backup, about 1 minute.
6. Backlog and the reflection draft, about 2 minutes.
7. Questions, about 2 minutes.

## Why this option

Say that this is DEVASC Project Activity 3, Option 2. The class asked for a prototype that shows public IP addressing to network technicians. A new app can show IPv4, IPv6, the ISP, the ASN, and the country code. Option 1 would have added features to a directions script. This class needs the address story more than another route table.

The four picks are the ones that demo well, need no API key, and still work when one provider is down.

## Features

Walk through the four features on the live page. The map fills the viewport. The card is a modal on that map.

1. The profile card. The front is the credential. The back is the roast, the coordinates, and the quiz.
2. The map pin. MapLibre and the OpenFreeMap Liberty style fill the screen. The map stays flat, because this app is not using Mapbox. The visitor can drag and zoom. One pin marks the lookup. A click on that pin opens the card. No API key is required. The page does not use an OpenStreetMap iframe. The pin is often the ISP equipment, not the house.
3. The IPv6 row. It shows an address, or "No IPv6 yet". The IPv4 row says "None on this lookup" when the lookup has no IPv4 address. MAC says "Not available".
4. One roast line and one ISP question. The roast is about the network. The quiz is on the back of the card.

## Files to open

Open these files and say one job for each.

- `app.py` serves `GET /` and `POST /quiz`. Gunicorn loads `app:app`.
- `ipinfo.py` parses `X-Forwarded-For` and calls the providers.
- `fun.py` builds the roast, the quiz, the grade, and `map_embed`. `map_embed` still returns an OpenStreetMap URL. `tests/test_fun.py` checks that helper. The page does not load it.
- `templates/index.html` is the page. The script in that file fetches `https://api6.ipify.org?format=json`.
- `static/map.js` starts the flat MapLibre map and opens the card from the pin.
- `static/card.js` opens the card, flips it, and closes it. The X sits outside the card.

## Live demo

Open `[Render live link to be added]` a few minutes early. The free instance sleeps.

On the laptop, load the page. MapLibre and the OpenFreeMap Liberty style fill the screen. The map stays flat. Drag the map and zoom it. One pin marks the lookup. The page does not use an OpenStreetMap iframe.

Click the pin. The card opens in the center. A gray layer covers the map. The X sits on that gray, outside the card. Read IPv4, IPv6, the ISP, the ASN, the place, and the MAC line. MAC says "Not available".

The IPv6 row starts as "Checking IPv6". The page fetches `https://api6.ipify.org?format=json`. The server does not make that call. If the call fails, the row says "No IPv6 yet".

Click the card. The back shows the roast, the coordinates, and the quiz. Submit the real ISP. The page says "That's the one."

Click the X. The card closes and the map is usable again. Click the pin to open the card again.

On the phone, open the same URL. Tap the pin. The same centered card opens. Tap the card to flip it. Tap the X to close it.

For the hosted demo, `LOOKUP_MODE` is `forwarded`, or `RENDER` is true and `LOOKUP_MODE` is unset. The server then sees the forwarded address. That address is the first `X-Forwarded-For` entry. A missing header uses `request.remote_addr`.

## LAN backup

If Render is asleep or the phone cannot reach it, start the app on the demo PC.

```bash
LOOKUP_MODE=direct flask run --host 0.0.0.0 --port 5000
```

Join the phone to the same Wi-Fi and open `http://<pc-lan-ip>:5000`. Direct mode ignores the forwarding header. The provider sees the PC. On this backup, that address is the home public address.

## Backlog

Say these wait until after this demo.

- Look up an address a technician types.
- Show the raw JSON for class discussion.
- Compare two addresses.
- Save a lookup to a CSV file.
- More roast lines written by the class.
- Server-side IPv6 when the host itself has IPv6.

## Reflection

Open `REFLECTION.md`. Tell the class it is a draft the team still has to rewrite. Stick to that page. Do not add a story that is not written there.

## Questions

Leave about 2 minutes. These are the questions the design already raises.

- Why is the pin often a building the visitor has not been in?
- Why does the page fetch `https://api6.ipify.org?format=json` while the server reads the forwarded address?
- What changes when `LOOKUP_MODE` is `direct` on the LAN backup?
