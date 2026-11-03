# Reflection

DRAFT. The team rewrites this before it goes in the paper. The notes below follow `PLAN.md` and the page in the repository. They do not record a team incident.

## What went well

Option 2 is a new app, so the page can show the address story. Option 1 would have added features to a directions script. The four features are a profile card, a map pin, an IPv6 badge, and one roast with one ISP question. Those four won because they demo on a phone and a laptop. They need no API key. The page still works when one provider is down.

MapLibre and the OpenFreeMap Liberty style fill the viewport. The map stays flat, because this app is not using Mapbox. The visitor can drag and zoom. On a wide window the card sits on the left and the pin stays in the open map. A marker sits on the lookup coordinates. The page does not use an OpenStreetMap iframe. `map_embed` in `fun.py` still returns an OpenStreetMap URL. `tests/test_fun.py` checks that helper. The page does not load the URL.

The card is a modal. On a laptop, a mouse tilts the card. A click flips it. The X closes it. **Address card** opens it again. The quiz is on the back. There is no control labeled "Turn the card". On a phone, a tap flips the card. A tap on the X closes it. The card sits along the bottom. Dragging does not tilt the card.

The quiz needs no session and no database. The same ISP rebuilds the same three choices. The roast is about the network.

## What was hard

`PLAN.md` names these constraints.

- A phone does not fire hover. A tap flips the card. A tap on the X closes it. The card sits along the bottom. Dragging does not tilt the card.
- The Render free instance sleeps. The demo URL has to be opened a few minutes early.
- Direct mode and forwarded mode answer different questions. Direct mode ignores `X-Forwarded-For`. Forwarded mode reads the first entry.
- The map pin is often the provider equipment, not the house. The page has to say so.
- The map stays flat. This app is not using Mapbox, so the view does not pitch. The card is the piece that leans. The page uses MapLibre with the OpenFreeMap Liberty style, and that style needs no API key.

## What we learned about REST APIs

The lookup calls three providers in order. First is ipwho.is. Second is ipapi.co. Third is api.ipify.org, and only when no address is known yet. Each call times out after 4 seconds. A provider can answer HTTP 200 and still be a miss when success is false or an error is set. The next provider is then tried. No API key is required.

When an address was already known and the location lookup fails, the notice is "The location lookup is taking a break. The address below is still yours." When no public address can be found, the notice is "We could not find a public address right now. Refresh in a moment." The route still returns 200.

## What we learned about IPv4 and IPv6

The server lookup is the IPv4 path. In forwarded mode the server sees the forwarded address. That is the first `X-Forwarded-For` entry, or `request.remote_addr` when the header is missing. In direct mode the header is ignored and the provider sees the server. That is the home public address on the LAN backup.

The page fetches `https://api6.ipify.org?format=json`. Failure sets the badge to "No IPv6 yet". IPv6 is not in the template context. Server-side IPv6 stays on the backlog, for a host that has IPv6.

## What we would do next

The backlog in `PLAN.md` is the next work.

- Look up an address a technician types.
- Show the raw JSON for class discussion.
- Compare two addresses.
- Save a lookup to a CSV file.
- More roast lines written by the class.
- Server-side IPv6 when the host itself has IPv6.
