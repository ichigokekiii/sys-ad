"""Public address lookup for Address Card.

Header rules and provider JSON stay in this module. The route only asks
for a finished LookupResult, so a stalled provider cannot take down the page.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote

# These two sentences are the copy the page shows. They stay exact so the
# demo does not drift between a timeout and a total miss.
PARTIAL_NOTICE = (
    "The location lookup is taking a break. The address below is still yours."
)
EMPTY_NOTICE = (
    "We could not find a public address right now. Refresh in a moment."
)
USER_AGENT = "AddressCard/1.0 (DEVASC class project)"


@dataclass(frozen=True)
class LookupResult:
    query_ip: str | None
    ipv4: str | None
    isp: str | None
    asn: str | None
    country_code: str | None
    country: str | None
    city: str | None
    latitude: float | None
    longitude: float | None
    source: str
    notice: str | None


def parse_forwarded(header: str | None) -> str | None:
    # Proxies append themselves after the client, so only the first entry
    # is the visitor. A single colon on IPv4 is a port. IPv6 uses colons
    # as part of the address, so that form stays intact.
    if not isinstance(header, str):
        return None
    if not header.strip():
        return None
    first = header.split(",", 1)[0].strip()
    if not first:
        return None
    if first.count(":") == 1:
        host, port = first.split(":", 1)
        host = host.strip()
        if port.strip().isdigit() and host.count(".") == 3:
            return host
    return first


def current_mode(env) -> str:
    # LOOKUP_MODE is the demo switch. Render only sets RENDER, so that hint
    # applies when the laptop has not chosen a mode of its own.
    chosen = str(env.get("LOOKUP_MODE") or "").strip().lower()
    if chosen in ("forwarded", "direct"):
        return chosen
    render = str(env.get("RENDER") or "").strip().lower()
    if render in ("true", "1"):
        return "forwarded"
    return "direct"


def resolve_query_ip(mode, forwarded_header, remote_addr) -> str | None:
    # Direct mode must ignore the client. The provider then sees the server,
    # which is the home public address on the LAN backup.
    if mode != "forwarded":
        return None
    parsed = parse_forwarded(forwarded_header)
    if parsed:
        return parsed
    if remote_addr is None:
        return None
    text = str(remote_addr).strip()
    return text or None


def lookup(ip, timeout=4, get=None):
    # Import requests only when this process will open a socket. The header
    # helpers stay usable in a check that never installs the HTTP library.
    if get is None:
        import requests # pyright: ignore[reportMissingModuleSource]

        get = requests.get

    who = _call(get, _ipwho_url(ip), timeout)
    if who is not None:
        return _from_ipwho(who)

    api = _call(get, _ipapi_url(ip), timeout)
    if api is not None:
        return _from_ipapi(api)

    # The caller already knows the address. Keep it and skip ipify.
    if ip is not None:
        return _bare(ip, "unavailable", PARTIAL_NOTICE)

    found = _call(get, "https://api.ipify.org?format=json", timeout)
    if found is not None:
        parsed = _from_ipify(found)
        if parsed is not None:
            return parsed

    return _bare(None, "unavailable", EMPTY_NOTICE)


def _ipwho_url(ip) -> str:
    if ip is None:
        return "https://ipwho.is/"
    # The address is one path segment. Quoting stops a bad header from
    # adding another slash while leaving IPv6 colons readable.
    return "https://ipwho.is/" + quote(str(ip), safe=":")


def _ipapi_url(ip) -> str:
    if ip is None:
        return "https://ipapi.co/json/"
    return "https://ipapi.co/" + quote(str(ip), safe=":") + "/json/"


def _call(get, url, timeout):
    try:
        response = get(
            url,
            timeout=timeout,
            headers={"User-Agent": USER_AGENT},
        )
        if getattr(response, "status_code", None) != 200:
            return None
        payload = response.json()
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None
    # These providers answer HTTP 200 for a logical failure. success false
    # and a truthy error key both mean try the next one.
    if payload.get("success") is False or payload.get("error"):
        return None
    return payload


def _from_ipwho(payload) -> LookupResult:
    connection = payload.get("connection")
    if not isinstance(connection, dict):
        connection = {}
    # isp is often blank while org is filled. The page needs one network name.
    isp = _text(connection.get("isp")) or _text(connection.get("org"))
    return _result(
        payload.get("ip"),
        isp,
        _asn(connection.get("asn")),
        payload.get("country_code"),
        payload.get("country"),
        payload.get("city"),
        _coord(payload.get("latitude")),
        _coord(payload.get("longitude")),
        "ipwho.is",
        None,
    )


def _from_ipapi(payload) -> LookupResult:
    org = _text(payload.get("org"))
    asn = _asn(payload.get("asn"))
    if asn is None:
        asn = _leading_as(org)
    # ipapi puts the country code in country and the name in country_name.
    return _result(
        payload.get("ip"),
        org,
        asn,
        payload.get("country"),
        payload.get("country_name"),
        payload.get("city"),
        _coord(payload.get("latitude")),
        _coord(payload.get("longitude")),
        "ipapi.co",
        None,
    )


def _from_ipify(payload):
    address = _text(payload.get("ip"))
    if address is None:
        return None
    return _bare(address, "ipify", PARTIAL_NOTICE)


def _bare(ip, source, notice) -> LookupResult:
    return _result(ip, None, None, None, None, None, None, None, source, notice)


def _result(
    address,
    isp,
    asn,
    country_code,
    country,
    city,
    latitude,
    longitude,
    source,
    notice,
) -> LookupResult:
    text = _text(address)
    return LookupResult(
        query_ip=text,
        ipv4=_as_ipv4(text),
        isp=_text(isp),
        asn=_text(asn),
        country_code=_text(country_code),
        country=_text(country),
        city=_text(city),
        latitude=latitude,
        longitude=longitude,
        source=source,
        notice=notice,
    )


def _as_ipv4(address):
    # Three dots and no colon is the whole IPv4 test this page uses.
    # An IPv6 address stays in query_ip so the card does not mislabel it.
    if address is None:
        return None
    if address.count(".") == 3 and ":" not in address:
        return address
    return None


def _asn(value):
    # ipwho sends a bare integer. The card shows the registry form.
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, int):
        return f"AS{value}"
    if isinstance(value, float):
        if value != value or not value.is_integer():
            return None
        return f"AS{int(value)}"
    text = _text(value)
    if text is None:
        return None
    token = text.split()[0]
    if token.upper().startswith("AS"):
        rest = token[2:]
        if rest.isdigit():
            return f"AS{rest}"
        return None
    if token.isdigit():
        return f"AS{token}"
    return None


def _leading_as(org):
    if org is None:
        return None
    token = org.split()[0]
    if token.upper().startswith("AS") and token[2:].isdigit():
        return f"AS{token[2:]}"
    return None


def _text(value):
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        if isinstance(value, float) and value != value:
            return None
        return str(value)
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


def _coord(value):
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, str) and not value.strip():
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number != number:
        return None
    return number
