# Address Card

DEVASC Project Activity 3. This repository is the Option 2 app, a phone and laptop demo of one public address card.

The remote is `[GitHub repository link]` until the repository exists. The live page is `[Render live link to be added]`.

## Option 2

Option 2 is the choice. The class asked for a prototype that shows public IP addressing to network technicians. Option 2 is a new app, so the page can be built around IPv4, IPv6, the ISP, the ASN, and the country code. Option 1 would have added features to a directions script. This class needs the address story more than another route table.

The demo has four objectives.

1. Show a profile card. The front is the credential. The back is the roast, the coordinates, and the quiz.
2. Show a map pin of where the internet thinks the visitor is. The pin is often the ISP equipment, not the house.
3. Show an IPv6 badge. The badge shows the address, or the words "No IPv6 yet".
4. Show one friendly roast line and one ISP question.

The roast is about the network. Branch names and review rules are in `CONTRIBUTING.md`.

## What the page does

`GET /` asks for one lookup and renders `templates/index.html`.

MapLibre and the OpenFreeMap Liberty style fill the viewport. The map stays flat. This app is not using Mapbox, so the visitor can drag and zoom, and the view does not pitch. On a wide window the card sits on the left and the pin stays in the open map. A marker sits on the lookup coordinates. The style needs no API key. The page does not use an OpenStreetMap iframe. When the lookup has no coordinates, the map opens on a wide view and draws no marker.

The card is a modal on that map. On a laptop, a mouse tilts the card. A click flips it. The X closes it. **Address card** opens it again. The quiz is on the back. There is no control labeled "Turn the card".

On a phone, a tap flips the card. A tap on the X closes it. The card sits along the bottom. Dragging does not tilt the card.

`POST /quiz` looks the address up again, rebuilds the quiz from the ISP name, and grades the posted choice. The same ISP always rebuilds the same three choices. There is no session and no database. The quiz answer is not written into the HTML as a hidden field.

The server tries providers in this order.

1. `https://ipwho.is/` when no address is known yet, or `https://ipwho.is/<ip>` when one is known.
2. `https://ipapi.co/json/` or `https://ipapi.co/<ip>/json/`.
3. When the visitor address is already known, the page keeps that address and shows a notice.
4. When no address is known yet, `https://api.ipify.org?format=json` supplies the IPv4 address only.

Each call times out after 4 seconds. A provider can return HTTP 200 and still count as a miss when `success` is false or `error` is set. The route still returns 200.

When an address was known and the location lookup fails, the notice is "The location lookup is taking a break. The address below is still yours." When no public address can be found, the notice is "We could not find a public address right now. Refresh in a moment."

The right quiz choice grades as "That's the one." A wrong choice grades as "Close. This network is {isp}." When the ISP is missing, the prompt is "The provider did not come back, so there is no guess this round."

The page fetches `https://api6.ipify.org?format=json` for the IPv6 badge. That call stays in the browser. The badge starts as "Checking IPv6". If the call fails, the badge says "No IPv6 yet". The server does not put IPv6 in the template context.

Server lookups send the header `User-Agent: AddressCard/1.0 (DEVASC class project)`.

## Set up a local copy

From the project folder, create a virtual environment and install the requirements.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` installs Flask, requests, gunicorn, and pytest.

## Run the app on this computer

From the project folder, start Flask.

```bash
flask --app app run
```

Open the URL Flask prints. The page shows the address card, or a notice when every provider is down.

Run the tests from the same folder.

```bash
pytest
```

## Run the LAN backup

Use this path when the phone and the laptop are on the same Wi-Fi. From the project folder, bind every interface on port 5000 and ignore the forwarding header.

```bash
LOOKUP_MODE=direct flask run --host 0.0.0.0 --port 5000
```

On the phone, open `http://<pc-lan-ip>:5000`. Direct mode ignores `X-Forwarded-For`. The provider then sees the computer that is running the app. On this backup, that address is the home public address.

## Deploy to Render

`Procfile` starts gunicorn.

```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

The free tier sleeps. Open `[Render live link to be added]` a few minutes before the demo.

On Render, set `LOOKUP_MODE` to `forwarded`, or leave it unset and let `RENDER=true` select forwarded mode. Render sets `RENDER`. `LOOKUP_MODE=direct` is still direct when `RENDER` is true, so do not set `direct` on the hosted demo.

## Configuration

`LOOKUP_MODE` is either `direct` or `forwarded`.

- `direct` ignores `X-Forwarded-For`. This is the default, and it is the LAN backup.
- `forwarded` uses the first `X-Forwarded-For` entry. A missing header uses `request.remote_addr`.

If `LOOKUP_MODE` is unset, `RENDER` set to `true` or `1` selects `forwarded`. Every other case is `direct`. `LOOKUP_MODE=direct` stays direct even when `RENDER` is true.

## Project structure

- `app.py` is the Flask shell. It serves `GET /` and `POST /quiz`. Gunicorn loads `app:app`.
- `ipinfo.py` parses headers and provider JSON. It owns the timeout and the fallbacks.
- `fun.py` owns the roast, the quiz, grading, and `map_embed`. `map_embed` still returns an OpenStreetMap URL. `tests/test_fun.py` checks that helper. The page does not load the URL.
- `templates/index.html` is the page. The IPv6 fetch is in that file.
- `static/map.js` starts the MapLibre map with the OpenFreeMap Liberty style.
- `static/card.js` tilts the card on a laptop, flips it, and closes it.
- `static/style.css` places the full-viewport map and the card.
- `Procfile` starts gunicorn on Render.
- `requirements.txt` lists the Python packages.
- `PLAN.md` is the design.
- `tests/test_ipinfo.py`, `tests/test_fun.py`, and `tests/test_app.py` are the pytest files.

## APIs the page calls

No API key is required.

- ipwho.is is the first lookup.
- ipapi.co is the second lookup.
- api.ipify.org supplies an IPv4 address only when the server does not already know one.
- The page fetches `https://api6.ipify.org?format=json` for the IPv6 badge.
- MapLibre loads the OpenFreeMap Liberty style in the browser. The HTML does not contain an OpenStreetMap iframe.

## Known limits

- The free Render instance sleeps until someone opens it.
- The map pin is often the provider equipment, not the house.
- In forwarded mode the server sees the forwarded address. In direct mode the provider sees the server.
- IPv6 is a fetch in the page. The server lookup does not store it.
- If MapLibre does not load, the page says "The map did not load. The card still has the address."
- The typed-address form, the header lesson, and a classmate compare are not in this demo.

## Backlog

- Look up an address a technician types.
- Show the raw JSON for class discussion.
- Compare two addresses.
- Save a lookup to a CSV file.
- More roast lines written by the class.
- Server-side IPv6 when the host itself has IPv6.

## Screenshots

The desktop image will be at `screenshots/desktop.png`.

The phone image will be at `screenshots/mobile.png`.
