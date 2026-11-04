# Address Card plan

DEVASC Project Activity 3, Option 2. One Flask page for a phone and a laptop demo. The page shows a visitor's public IP story as a 3D profile card.

This file is the design. App code comes after it.

## Why this option

The engineering request is a prototype that shows public IP addressing to network technicians. Option 2 is a new app, so the team can shape the page around IPv4, IPv6, ISP, ASN, and country code. Option 1 would have been extra features on a directions script. This class needs the address story more than another route table.

## What ships

One screen. Four features.

1. A 3D profile card. Front is the credential. Back is the roast and the coordinates.
2. A map pin of where the internet thinks you are. The pin is often the ISP's equipment, not the house. The caption says so.
3. An IPv6 badge. The address, or the words "No IPv6 yet".
4. One friendly roast line and one ISP question.

The any-IP form, the header lesson, and a classmate compare wait on the backlog. They are real Activity 4 work. They are not needed to demo the page tomorrow.

## Ideas considered

1. Internet ID card.
2. Map pin.
3. Guess-the-ISP quiz.
4. Friendly roast from the ISP or the country. Never about the person.
5. IPv6 badge.
6. A form to look up any IP.
7. "How far is this pin from me" using browser location.
8. A panel that compares X-Forwarded-For with the API result.
9. A side-by-side classmate compare.
10. A race of the three APIs.

The four picks won because they demo well, they can be built today, they need no API key, and they still work when one provider is down. The form, the header panel, and the compare are useful later. Browser location and a map library need more JavaScript than this page should carry. A latency race is flaky on stage.

## The 3D card

The motion comes from public card studies, not from a portfolio skin.

- Dribbble 3D flip cards use two faces and a rotateY turn. On a phone, hover never fires, so a tap has to turn the card.
- Awwwards tilt studies lean the card toward the pointer. That is the laptop move.
- The lean stays near 10 degrees. A soft glare follows the pointer. Reduced motion turns the lean off.
- No sparkles, no avatar ring, no "PRO" badge. This object is a network credential.

Interaction:

- The page is the map. The card floats on it and does not cover the whole screen.
- Laptop. The card tilts toward the pointer. A click on the card turns it over. The X closes it. Address card brings it back.
- Phone. No drag tilt. A tap turns the card. The X is at least 44px.
- The map stays draggable while the card is open.
- Reduced motion, or no script. The card stays flat. Both faces are in the HTML.

Front, readable before anyone flips. Public IPv4, ISP, ASN, country code, city, IPv6 stamp or the empty badge.

Back. The roast, latitude and longitude, and which API answered.

The quiz sits on the back of the card. The map is the page behind the card.

Scripts:

- A few lines in the page fetch `https://api6.ipify.org?format=json`. Failure sets the badge to "No IPv6 yet".
- `static/map.js` starts a flat MapLibre map from OpenFreeMap Liberty. It pans and zooms. It does not pitch, because this app is not using Mapbox. The card is what leans.
- `static/card.js` tilts, flips, and closes the card. No extra network call.

## Data shape

`LookupResult` is frozen. Missing fields stay empty. The page still renders.

- `query_ip`
- `ipv4` when the address is IPv4, else empty
- `isp`
- `asn` displayed like `AS15169`
- `country_code`
- `country`
- `city`
- `latitude`
- `longitude`
- `source` is `ipwho.is`, `ipapi.co`, `ipify`, or `unavailable`
- `notice` is a friendly sentence or empty

`Quiz` is frozen.

- `prompt`
- `choices`, exactly three strings, or none when the ISP is unknown
- `answer` is not written into the HTML

The same ISP always rebuilds the same three choices. Grading needs no session and no database.

Template context:

- `card`
- `roast`
- `quiz`
- `quiz_result`
- `map_src`
- `notice`

IPv6 is not in that context.

## Lookup rules

Every HTTP call times out after 4 seconds. Any error becomes a notice. The route still returns 200.

Order:

1. `https://ipwho.is/` or `https://ipwho.is/<ip>`
2. `https://ipapi.co/json/` or `https://ipapi.co/<ip>/json/`
3. If the visitor IP is already known, show that IP and a notice that city and ISP could not be loaded.
4. In direct mode, if no IP is known yet, `https://api.ipify.org?format=json` supplies the IPv4 only.

`LOOKUP_MODE=forwarded` reads the first `X-Forwarded-For` entry, then looks that IP up. A missing header uses `request.remote_addr`.

`LOOKUP_MODE=direct` ignores the forwarding header and asks ipwho.is who the server is. That is the home public IP. Same code.

If `LOOKUP_MODE` is unset, `RENDER` selects forwarded. Otherwise the mode is direct, so the LAN backup needs no extra flag.

The map is a flat MapLibre view with the OpenFreeMap Liberty style. On a desktop the pin sits to the right of the card. No coordinates means a wide view and no pin. The old embed URL helper stays for tests.

Notices, exact sentences:

- Partial. `The location lookup is taking a break. The address below is still yours.`
- Nothing. `We could not find a public address right now. Refresh in a moment.`

## Modules

- `app.py` is the thin Flask shell. `GET /` and `POST /quiz`. Gunicorn loads `app:app`.
- `ipinfo.py` parses headers and provider JSON. It owns timeouts and fallbacks.
- `fun.py` owns the roast table, the quiz, grading, and the map URL. Pure functions.

Public functions tests may call:

- `parse_forwarded(header) -> str or None`
- `current_mode(env) -> "forwarded" or "direct"`
- `resolve_query_ip(mode, forwarded_header, remote_addr) -> str or None`
- `lookup(ip, timeout=4, get=requests.get) -> LookupResult`
- `roast(isp, country_code) -> str`
- `quiz_for(isp) -> Quiz`
- `grade(quiz, choice) -> str`
- `map_embed(lat, lon) -> str or None`

`parse_forwarded` rules:

- Missing or blank returns None.
- `"203.0.113.5"` returns that address.
- `"203.0.113.5, 10.0.0.1"` returns `203.0.113.5`.
- A trailing port on an IPv4 address is removed. An IPv6 address is kept.

Roast lines are about the network. They never describe the person.

Quiz grading:

- Right choice. `That's the one.`
- Wrong choice, ISP known. `Close. This network is {isp}.`
- No ISP. No form. The prompt says the provider did not come back.

## Layout

- The map fills the viewport at every width.
- 390px. The card sits along the bottom. The reopen control sits there too once the card is closed.
- 1280px and up. The card floats on the left so the pin stays visible.
- Keyboard focus visible. Text contrast meets WCAG AA. Escape closes the card.
- `prefers-reduced-motion` leaves the card flat.

## Hosting

Main path. Render, free, Flask plus gunicorn. Open the URL a few minutes before the demo. The free instance sleeps.

Backup path. On John's PC:

```bash
LOOKUP_MODE=direct flask run --host 0.0.0.0 --port 5000
```

The phone joins the same Wi-Fi and opens `http://<pc-lan-ip>:5000`.

## Docs and git

One repo. Branches `emanuel/api`, `john/ui`, `luis/tests`, `john/paper`. Each change merges through a pull request with one reviewer.

- Emanuel builds the API layer and lookup.
- John builds the UI and reviews pull requests.
- Luis writes the pytest tests and reviews the README.

Until `gh` is logged in, the paper says `[GitHub repository link]`. Luis is `lg-araneta`. Emanuel is `Leunewashere`.

Until Render answers with a URL, the paper says `[Render live link to be added]`.

Reflection text is a draft. It does not invent a team incident.

## Backlog

- Look up an address a technician types.
- Show the raw JSON for class discussion.
- Compare two addresses.
- Save a lookup to a CSV file.
- More roast lines written by the class.
- Server-side IPv6 when the host itself has IPv6.

## Sample content for the page design

Use these values while designing. The rebuild swaps them for the template fields.

- IPv4 `203.0.113.42`
- ISP `PLDT`
- ASN `AS9299`
- Country code `PH`
- City `Manila`
- Latitude `14.5995`
- Longitude `120.9842`
- Source `ipwho.is`
- Roast `PLDT brought you here the long way around. The pin is probably a building you have never visited.`
- Quiz prompt `Which network is this?`
- Choices `PLDT`, `Globe`, `Converge`
- Notice empty
- IPv6 badge starts as `Checking IPv6`, then the script fills it
