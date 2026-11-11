# Fetch real routes from OSRM for each leg of the itinerary and write them as JSON.
import json, sys, time, urllib.request
OUT = sys.argv[1]
P = {
  "airport": (26.2065, 127.6522), "rent": (26.2381309, 127.6821694), "ramen": (26.248095, 127.701195),
  "parco": (26.2603, 127.6985), "goen": (26.228853, 127.70179), "hotel1": (26.295218, 127.759262),
  "aqua": (26.6943689, 127.8780380), "dolphin": (26.6927844, 127.8758809), "kouri": (26.6863, 128.0171),
  "ufuya": (26.6210197, 127.9636378), "amvil": (26.3160, 127.7575), "rycom": (26.3142262, 127.7959208),
  "fish": (26.2436487, 127.6802982), "hotel2": (26.204695, 127.683556), "kokusai": (26.2150, 127.6860),
  "donki": (26.2158634, 127.6878077),
}
# (day, from, to, mode)  drive = self-drive, ride = driven by others (rental shuttle / taxi), walk = on foot
LEGS = [
  (1, "airport", "rent", "ride"), (1, "rent", "ramen", "drive"), (1, "ramen", "parco", "drive"),
  (1, "parco", "goen", "drive"), (1, "goen", "hotel1", "drive"),
  (2, "hotel1", "aqua", "drive"), (2, "aqua", "ufuya", "drive"), (2, "ufuya", "kouri", "drive"), (2, "kouri", "amvil", "drive"),
  (3, "hotel1", "rycom", "drive"), (3, "rycom", "fish", "drive"), (3, "fish", "rent", "drive"),
  (3, "rent", "hotel2", "ride"), (3, "hotel2", "kokusai", "walk"), (3, "kokusai", "donki", "walk"),
  (4, "hotel2", "airport", "ride"),
]
BASE = {"drive": "https://router.project-osrm.org/route/v1/driving/",
        "ride": "https://router.project-osrm.org/route/v1/driving/",
        "walk": "https://routing.openstreetmap.de/routed-foot/route/v1/driving/"}
out = []
for day, a, b, mode in LEGS:
    (la, na), (lb, nb) = P[a], P[b]
    url = f"{BASE[mode]}{na},{la};{nb},{lb}?overview=full&geometries=polyline"
    req = urllib.request.Request(url, headers={"User-Agent": "okinawa-itinerary-build/1.0"})
    r = json.load(urllib.request.urlopen(req, timeout=30))
    assert r["code"] == "Ok", (a, b, r.get("code"))
    rt = r["routes"][0]
    out.append({"day": day, "from": a, "to": b, "mode": mode, "min": round(rt["duration"] / 60),
                "km": round(rt["distance"] / 1000, 1), "poly": rt["geometry"]})
    print(day, a, "->", b, mode, out[-1]["min"], "min", out[-1]["km"], "km", len(rt["geometry"]), "chars")
    time.sleep(1.1)
json.dump({"pins": {k: [round(v[0], 6), round(v[1], 6)] for k, v in P.items()}, "legs": out}, open(OUT, "w"), ensure_ascii=False)
print("total poly chars", sum(len(l["poly"]) for l in out))
